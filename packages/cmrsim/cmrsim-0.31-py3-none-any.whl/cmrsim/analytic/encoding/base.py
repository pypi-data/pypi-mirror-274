""" This module contains the base implementation of the encoding mechanism of the simulation"""
__all__ = ["BaseSampling",]

from typing import Union, Iterable, Tuple
import abc
import math

import tensorflow as tf
import numpy as np
from pint import Quantity


# pylint: disable=abstract-method
class BaseSampling(tf.Module):
    """Base Module for implementing a time-dependent sampling in k-space. Is meant to be inherited
    from when specifying standard trajectories.

    :param absolute_noise_std: if < 0, add_noise() will leave signal unchanged
    :param name: (str) defining the module name-scope
    :param k_space_segments: Number of segments in k-space. Total number of samples divided by
                                the number of segments must be an integer value
    :param device: str e.g. 'GPU:0'
     """
    # pylint: disable=too-many-instance-attributes
    #: Flat and unsegmented tensor of all sampling-event times.  Is set by a call of
    # abstract function self._calculate_trajectory. Expected shape: (-1, )
    sampling_times: tf.Variable
    #: Flat and unsegmented tensor of 3D k-space vectors corresponding to sampling-events.
    # Is set by a call of abstract function self._calculate_trajectory. Expected shape: (-1, 3)
    k_space_vectors: tf.Variable
    #: absolute values for the standard deviation of the sampled noise distributions added
    # to the k-space signal
    absolute_noise_std: tf.Variable
    #: Number of segments used to subdivide the simulation memory load
    k_space_segments: tf.Variable
    #: Number of k-space samples that are defined by the _calculate trajectory method
    number_of_samples: tf.Tensor
    #: Name of the device that the module is executed on (defaults to: GPU:0 - CPU:0)
    device: str
    #: Spatial acquisition offset (corresponds to frequency offset)
    acq_position: tf.Variable = tf.Variable(tf.zeros(3), dtype=tf.float32)
    #: Orientation matrix (3, 4) performing the transformation from slice to global coordinates
    ori_matrix: tf.Variable

    _segmented_sampling_times = None  # set in update
    _segmented_k_vectors = None  # set in update

    def __init__(self, absolute_noise_std: Union[float, Iterable[float]], name: str = None,
                 k_space_segments: int = 1, device: str = None,
                 orientation_matrix: np.ndarray = None):
        """

        :param absolute_noise_std: if < 0, add_noise() will leave signal unchanged
        :param name: (str) defining the module name-scope
        :param k_space_segments: int
        :param device: str e.g. 'GPU:0'
        """

        if device is None:
            if tf.config.get_visible_devices('GPU'):
                self.device = 'GPU:0'
            else:
                self.device = 'CPU:0'
        else:
            self.device = device

        super().__init__(name=name)
        if isinstance(absolute_noise_std, float):
            absolute_noise_std = [absolute_noise_std, ]

        with tf.device(self.device):
            self.absolute_noise_std = tf.Variable(tf.constant(absolute_noise_std), dtype=tf.float32,
                                                  trainable=False, shape=[None, ],
                                                  name='absolute_noise_std')
            self.k_space_segments = tf.Variable(tf.constant(k_space_segments), dtype=tf.int32,
                                                trainable=False)
            self.k_space_vectors = tf.Variable(tf.zeros((1, 3), tf.float32), shape=[None, 3],
                                               dtype=tf.float32, trainable=False,
                                               name='k_space_vectors')
            self.sampling_times = tf.Variable(tf.zeros((1,), tf.float32), shape=[None, ],
                                              dtype=tf.float32, trainable=False, name='sampling_times')
            self.update()
            self.ori_matrix = orientation_matrix

    def update(self):
        """ Assigns values to trajectory vectors. Should be used after modifying the parameters of
        the encoding module.
        :return:
        """
        k_space_vectors, sampling_times = self._calculate_trajectory()
        self.k_space_vectors.assign(k_space_vectors)
        self.sampling_times.assign(sampling_times)
        self.number_of_samples = tf.size(self.sampling_times.read_value())

        assert (self.number_of_samples % self.k_space_segments == 0)

        # Define segmented k-space trajectory for lower GPU memory requirements
        segment_size = tf.cast(tf.math.ceil(self.number_of_samples /
                                            self.k_space_segments.read_value()), tf.int32)
        total_element_count = self.k_space_segments.read_value() * segment_size
        difference = total_element_count - self.number_of_samples
        row_lengths = tf.constant([int(segment_size) for _ in
                                   tf.range(self.k_space_segments.read_value() - 1)] +
                                  [int(segment_size - difference), ], dtype=tf.int32)

        self._segmented_sampling_times = tf.RaggedTensor.from_row_lengths(
            self.sampling_times.read_value(), row_lengths)
        self._segmented_k_vectors = tf.RaggedTensor.from_row_lengths(
            self.k_space_vectors.read_value(), row_lengths)

    @tf.function(jit_compile=False)
    def __call__(self, m_transverse: tf.Tensor, r_vectors: tf.Tensor):
        """ Fourier transforms the handed batch of object points / isochromates,

        :param m_transverse:
        :param r_vectors:
        :return: tf.Tensor of shape (#repetitions, #k-space-samples)
        """
        with tf.device(self.device):
            # Allocate k-space-Tensor
            # s_of_k_segments = tf.TensorArray(dtype=tf.complex64, size=n_segments, dynamic_size=False)
            samples_per_segment = tf.cast(self.number_of_samples / self.k_space_segments, tf.int32)
            accumulator_shape = tf.stack([self.k_space_segments, tf.shape(m_transverse)[1], samples_per_segment], axis=0)
            s_of_k_segments = tf.zeros(accumulator_shape, dtype=tf.complex64)
            max_mtrans_index = tf.math.reduce_min(tf.stack([tf.shape(m_transverse)[-1], self.k_space_segments]))
            max_rvectrans_index = tf.math.reduce_min(tf.stack([tf.shape(r_vectors)[-2], self.k_space_segments]))

            # Loop over k-space segments, defined by k-space trajectory in self.encoding_module
            for segment_index in tf.range(self.k_space_segments):
                mseg_idx = tf.reduce_min(tf.stack([segment_index + 1, max_mtrans_index]))
                rseg_idx = tf.reduce_min(tf.stack([segment_index + 1, max_rvectrans_index]))
                m_segment = m_transverse[..., samples_per_segment * (mseg_idx - 1): samples_per_segment * mseg_idx]
                r_segment = r_vectors[..., samples_per_segment * (rseg_idx - 1):samples_per_segment*rseg_idx, :]
                k_space_segment = self.call_single_segment(m_segment, r_segment, segment_index=segment_index)
                s_of_k_segments = tf.tensor_scatter_nd_update(s_of_k_segments, [[segment_index], ],
                                                              k_space_segment[tf.newaxis])

            # Concat all segments and transpose axes to match needed format
            return tf.reshape(tf.transpose(s_of_k_segments, [1, 0, 2]), [accumulator_shape[1], -1])

    @tf.function(jit_compile=False)
    def call_single_segment(self, transverse_magnetization: tf.Tensor, r_vectors: tf.Tensor,
                            segment_index: Union[int, tf.Tensor] = 0, **kwargs) -> tf.Tensor:
        """Calculates fourier phases for given object-representation at r-vectors. For multiple
        different contrasts #repetitions is the representing axis.

        Motion during encoding is captured in the r_vectors input axis #k-space-samples. If
        this axis has size=1, this position is reused for all sampling ADC events.
        If #repetitions = 1 in r_vectors, the same trajectory/constant position is reused
        for all contrasts.

        :param transverse_magnetization: (#voxel, #repetitions, #k-space-samples) of
                                         type tf.complex; #repetitions, #k-space-samples can be 1
        :param r_vectors: (#voxel, #repetitions, #k-space-samples, 3), axis #repetitions
                            and #k-space-samples can be 1 to broadcast for coordinate reuse.
        :param segment_index: int
        :return: tf.Tensor (..., k-space-points in segment)
        """
        with tf.device(self.device):

            n_repetitions = tf.shape(transverse_magnetization)[1]
            fourier_factors = self._calculate_fourier_phases(r_vectors=r_vectors,
                                                             segment_index=segment_index)

            with tf.name_scope('shape_handling'):
                if tf.shape(fourier_factors)[1] < n_repetitions:
                    multiples = n_repetitions // tf.shape(fourier_factors)[1]
                    fourier_factors = tf.tile(fourier_factors, [1, multiples, 1])

                if tf.shape(transverse_magnetization)[2] == 1:
                    n_samples = tf.size(self._segmented_sampling_times[segment_index])
                    transverse_magnetization = tf.tile(transverse_magnetization,
                                                       [1, 1, n_samples])
            fourier_transform_batch = tf.einsum('vrk, vrk -> rk',
                                                transverse_magnetization, fourier_factors)
            return fourier_transform_batch

    def _calculate_fourier_phases(self, r_vectors: tf.Tensor, segment_index: tf.Tensor):
        # pylint: disable=anomalous-backslash-in-string
        """ Calculates the phase factor for encoding a static (during read-out) object for the
         k-space-trajectory defined by self.k_space_vectors

        .. math::

            f = e^{2 \pi j\ k_r(t) \cdot r(t) }

        :param r_vectors: (#batch, #repetition, #kspace, 3)
        :param segment_index: int
        :return:
        """
        with tf.name_scope('calculate_fourier_phase'):
            segment_batch_size = tf.size(self._segmented_sampling_times[segment_index])
            if self.ori_matrix is not None:
                # augment dummy entry (x,y,z,1)
                r_vectors = r_vectors - tf.reshape(self.ori_matrix[:, 3], [1, 1, 3])
                r_vectors = tf.einsum('ij, brkj -> brki', self.ori_matrix[:3, :3], r_vectors)

            if tf.shape(r_vectors)[2] == 1:  # tile if #kspace-samples is 1
                r_vectors = tf.tile(r_vectors, [1, 1, segment_batch_size, 1])
            elif tf.shape(r_vectors)[2] != segment_batch_size:
                start = segment_batch_size * segment_index
                r_vectors = r_vectors[..., start:start + segment_batch_size, :]

            r_vectors = r_vectors - tf.reshape(self.acq_position, [1, 1, 1, 3])
            fourier_phases = tf.einsum('vrkj, kj -> vrk', r_vectors,
                                       self._segmented_k_vectors[segment_index])
            fourier_phases = 1j * tf.cast(
                tf.scalar_mul(tf.constant(2. * math.pi, tf.float32), fourier_phases), tf.complex64)
            fourier_factors = tf.exp(-fourier_phases)
            return fourier_factors

    def add_noise(self, s_of_k: tf.Tensor, **kwargs):
        """ Adds noise to k-space-samples, expands the number of axis by one and appends the
        different noise instantiations as second last axis.

        :param s_of_k: Tensor containing all encoded k-space samples
        :return: tf.Tensor
        """
        with tf.name_scope('add_noise'):
            old_shape = tf.shape(s_of_k)
            s_of_k = tf.expand_dims(s_of_k, axis=-2)
            if tf.reduce_any(tf.math.greater(self.absolute_noise_std, tf.constant(0.))):
                seed = kwargs.get("seed", None)

                # Set values less that 0 to exactly zero to scales sampled noise vector correctly
                clean_noise_std = tf.where(
                    tf.math.greater(self.absolute_noise_std, tf.constant(0.)),
                    self.absolute_noise_std, tf.zeros_like(self.absolute_noise_std))
                noise_vector_shape = tf.concat(
                    ((2,), old_shape, (tf.size(self.absolute_noise_std),)), 0)
                noise_vector = tf.random.normal(noise_vector_shape, mean=0., stddev=1., seed=seed)

                # Transposition of last two axis on purpose for subsequent addition
                # Einsum indices: real/imag channel, image_batch, ...
                # ... repetitions, pixels, noise_instantiations
                n_half = tf.cast(tf.size(self.sampling_times), tf.float32) / 2.
                noise_vector = tf.einsum('crpn, n -> crnp', noise_vector,
                                         clean_noise_std * tf.sqrt(n_half))
                complex_noise_vector = tf.complex(noise_vector[0], noise_vector[1])
                s_of_k = s_of_k + complex_noise_vector
            return s_of_k

    @abc.abstractmethod
    def _calculate_trajectory(self):
        """ Calculates the k_space_trajectory with the given variables of the module. The
        trajectory is given as tensor of shape (#samples, 3). Additionally it should return a
        tensor of times corresponding to the samples
        (#samples, 1) in ms

        :return: k_space_vectors, sampling_times
        """
        raise NotImplementedError

    def get_sampling_times(self):
        """Getter for sampling times. Defines format that should be used for all Signal modules
        that need the timing of the sampling events.

        :return: - tf.RaggedTensor or numpy.ndarray
                 - sampling times as numpy.ndarray in case the trajectory is not segmented.
        """
        if int(self.k_space_segments) > 1:  # noqa
            return self._segmented_sampling_times

        return self.sampling_times.read_value()

    def set_orientation_matrix(self, slice_position: Quantity, slice_normal: np.ndarray,
                               readout_direction: np.ndarray) -> None:
        """Sets the 4x4 orientation matrix of the encoding module, by constructing the 
        transformation I -> MPS from the slice position, normal and readout direction.
        Phase encoding computed by cross product of slice normal and readout. 

        Modifies the attribute `self.ori_matrix`.

        :param slice_position: 3D coordinate of slice center in XYZ coordinates with shape (3, )
        :param slice_normal: Normal vector of slice in XYZ coordinates with shape (3, )
        :param readout_direction: Readout direction vector in XYZ coordinates with shape (3, )
        """
        from cmrsim.utils.coordinates import compute_orientation_matrix
        # Strip the last row to make it a (3, 4) matrix
        trafo_mat = compute_orientation_matrix(slice_normal, slice_position, readout_direction)[:3]
        
        if self.ori_matrix is None:
            self.ori_matrix = tf.Variable(trafo_mat.astype(np.float32), shape=(3, 4),
                                          dtype=tf.float32)
        else:
            self.ori_matrix.assign(trafo_mat.astype(np.float32))