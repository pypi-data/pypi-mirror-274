""" This module contains the generic implementation of encoding modules using sequence
 definitions from cmrseq """

__all__ = ["GenericEncoding"]

import warnings
from typing import Union, Iterable

import numpy as np
import tensorflow as tf

from cmrsim.analytic.encoding.base import BaseSampling

# pylint: disable=abstract-method
class GenericEncoding(BaseSampling):
    """"Encoding module that allowing to directly define the k-space sampling events

    :param name: Name of the module
    :param k_space_vectors: List or single instance of a numpy array containing the all sampled
                            k-space vectors, each with shape (N_i, 3)
    :param sampling_times: List or single instance of numpy array containing corresponding
                            sampling times, each with shape (N_i, ).
    :param absolute_noise_std: Noise standard deviation
    :param k_space_segments: If not specified, the number of sequences is used.
    :param device: Name of device that the operation is placed on
    """
    #: (N, 3) - Tensor containing all sampled k-space vectors
    _kspace_vectors: tf.Tensor
    #: (N, ) - Tensor containing the timing, corresponding to the kspace vectors
    _sampling_times: tf.Tensor

    def __init__(self, name: str,
                 k_space_vectors: Iterable[np.ndarray],
                 sampling_times: Iterable[np.ndarray],
                 absolute_noise_std: Union[float, Iterable[float]],
                 k_space_segments: int = None,
                 device: str = None):
        """
        :param name: Name of the module
        :param k_space_vectors: List or single instance of a numpy array containing the all sampled
                                k-space vectors, each with shape (N_i, 3)
        :param sampling_times: List or single instance of numpy array containing corresponding
                                sampling times, each with shape (N_i, ).
        :param absolute_noise_std: Noise standard deviation
        :param k_space_segments: If not specified, the number of sequences is used.
        :param device: Name of device that the operation is placed on
        """

        self._kspace_vectors = tf.constant(np.concatenate(k_space_vectors, axis=0), dtype=tf.float32)
        self._sampling_times = tf.constant(np.concatenate(sampling_times), dtype=tf.float32)

        super().__init__(absolute_noise_std, name, device=device,
                         k_space_segments=tf.constant(k_space_segments, dtype=tf.int32))

    def _calculate_trajectory(self) -> (tf.Tensor, tf.Tensor):
        """ Trivial return of stored arrays
        :return:  kspace-vectors, timing
        """
        return self._kspace_vectors, self._sampling_times

    @classmethod
    def from_cmrseq(cls, name: str, sequence: Union['cmrseq.Sequence', Iterable['cmrseq.Sequence']],
                    absolute_noise_std: Union[float, Iterable[float]],
                    k_space_segments: int = None,
                    device: str = None):
        """ Creates an analytic encoding module from a list of CMRseq sequence objects

        :param name: Name of the module
        :param sequence: List or single instance of cmrseq.Sequence that implements the
                            calculate_kspace() function
        :param absolute_noise_std: Noise standard deviation
        :param k_space_segments: If not specified, the number of sequences is used.
        :param device: Name of device that the operation is placed on
        :return:
        """
        try:
            import cmrseq
        except ImportError:
            raise ImportError("CMRsim: The package cmrseq is not installed, therefore the"
                              "GenericEncoding class cannot be instantiated.")

        if isinstance(sequence, cmrseq.Sequence):
            sequence = [sequence, ]

        if k_space_segments is None:
            k_space_segments = len(sequence)

        # Calculate sampling times and kspace vectors
        k_space, timings = [], []
        for seq in sequence:
            _, k_adc, t_adc = seq.calculate_kspace()
            k_space.append(k_adc.T)
            timings.append(t_adc)
        k_space = np.concatenate(k_space, axis=0, dtype=np.float32)
        timings = np.concatenate(timings, axis=0, dtype=np.float32)
        # # pylint: disable=no-value-for-parameter, unexpected-keyword-arg
        # k_space = tf.cast(tf.concat(k_space, axis=0), tf.float32)
        # # pylint: disable=no-value-for-parameter, unexpected-keyword-arg
        # timings = tf.cast(tf.concat(timings, axis=0), tf.float32)
        return cls(name, [k_space, ], [timings, ], absolute_noise_std, k_space_segments, device)

    def from_pulseq(self):
        raise NotImplementedError("Pulseq interface not yet implemented")