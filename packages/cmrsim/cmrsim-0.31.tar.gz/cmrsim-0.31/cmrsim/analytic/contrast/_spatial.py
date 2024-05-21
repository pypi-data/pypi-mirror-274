__all__ = ["SliceProfile", "LocalLookREST"]

from typing import Union, Tuple, Sequence

import tensorflow as tf
import numpy as np

from cmrsim.analytic.contrast.base import BaseSignalModel


class SliceProfile(BaseSignalModel):
    """Simplified slice-selection module, computing a weighting from 0 to 1 depending on through-slice position.

    .. note::

        To modify the actual slice-profile you can implement a subclass of this class that implements a different
        'slice_profile' method.

    .. dropdown:: Example Images

        .. image:: _static/api/analytic/contrast_slice_profile.png

    .. dropdown:: Example Usage

        .. code::

            uniform_mesh = pyvista.UniformGrid(spacing=(0.001, 0.001, 0.001), dimensions=(100, 100, 100),
                                               origin=(-0.05, -0.05, -0.05))
            r_vectors = tf.constant(uniform_mesh.points, dtype=tf.float32)
            slice_normal = np.array([[0, 1, 1], [0, 0, 1], [1, 2, 0]], dtype=np.float64)
            slice_normal /= np.linalg.norm(slice_normal, keepdims=True, axis=-1)
            slice_position = Quantity([[0, 1, 1], [1, 0, 0], [0, 1, 0]], "cm").m_as("m")
            slice_thickness = Quantity([2, 4, 0.5], "cm").m_as("m")

            slice_mod = cmrsim.analytic.contrast.SliceProfile(expand_repetitions=True, slice_normal=slice_normal,
                                                              slice_position=slice_position,
                                                              slice_thickness=slice_thickness)
            r_vectors_excitation = tf.reshape(r_vectors, [-1, 1, 1, 3])
            signal_start = tf.ones(r_vectors_excitation.shape[:-1], dtype=tf.complex64)


            signal_out = slice_mod(signal_tensor=signal_start, r_vectors_excitation=r_vectors_excitation).numpy()
            for i in range(signal_out.shape[1]):
                uniform_mesh[f"signal_out{i}"] = np.abs(signal_out)[:, i, 0]


    :param expand_repetitions: if True, expands repetition axes with the factor determined by the first axes of the
                                following input arguments
    :param slice_normal: (expansion_factor, 3) vector defining the slice normal of the excitation slice
    :param slice_position: (expansion_factor, 3) vector determining the slice-center-point
    :param slice_thickness: (expansion_factor, ) scalar in meter, determining the slice thickness
    :param device: name of the device to place this operation on
    """
    #: Additional mandatory keyword arguments for call
    required_quantities = ('r_vectors_excitation', )
    #: (expansion_factor, 3) vector defining the slice normal of the excitation slice
    slice_normal: tf.Variable = None
    #: (expansion_factor, 3) vector determining the slice-center-point
    slice_position: tf.Variable = None
    #: (expansion_factor, ) scalar in meter, determining the slice thickness
    slice_thickness: tf.Variable = None

    def __init__(self, expand_repetitions: bool, slice_normal: Sequence[Union[float, Sequence[float]]],
                 slice_position: Sequence[Union[float, Sequence[float]]],
                 slice_thickness: Union[float, Sequence[float]], device: str = None):

        slice_normal = tf.reshape(tf.constant(slice_normal, dtype=tf.float32), (-1, 3))
        slice_position = tf.reshape(tf.constant(slice_position, dtype=tf.float32), (-1, 3))
        slice_thickness = tf.reshape(tf.constant(slice_thickness, dtype=tf.float32), (-1))
        self._validate_shapes(slice_normal, slice_position, slice_thickness)

        super(SliceProfile, self).__init__(name="slice_excitation", expand_repetitions=expand_repetitions,
                                           device=device)

        self.slice_normal = tf.Variable(slice_normal, shape=(None, 3), dtype=tf.float32)
        self.slice_position = tf.Variable(slice_position, shape=(None, 3), dtype=tf.float32)
        self.slice_thickness = tf.Variable(slice_thickness, shape=(None,), dtype=tf.float32)
        self.update()

    @staticmethod
    def _validate_shapes(slice_normal, slice_position, slice_thickness):
        """Checks if the number of normals/positions/thickness is the same
        :raises: Value error if len(...) of all input arguments are not equal
        """
        if not ((len(slice_normal) == len(slice_position)) and (len(slice_normal) == len(slice_thickness))):
            raise ValueError("Must specify the same number of slice normals/positions/thickness but got: "
                             f"{[len(s) for s in (slice_normal, slice_position, slice_thickness)]}")

    def update(self):
        self._validate_shapes(self.slice_normal.read_value(), self.slice_position.read_value(),
                              self.slice_thickness.read_value())
        self.expansion_factor.assign(tf.shape(self.slice_normal.read_value())[0])

    def __call__(self, signal_tensor: tf.Tensor, r_vectors_excitation: tf.Tensor, **kwargs):  # noqa
        """ Call function for analytice slice-profile weighting

        :raises: AssertionError - r_vectors_excitation.shape[1] not equal to 1 or self.expansion_factor
                                - r_vectors_excitation.shape[2] is not equal to 1 (k-samples not supported here)
        :param signal_tensor: (#batch, [#repetitions, 1], #ksamples)
        :param r_vectors_excitation: (#batch, [#repetition, 1], 1, 3)

        :return: signal_tensor weighted by slice selective excitation
        """

        with tf.device(self.device):
            # All Cases --> repetitions-axis of argument r_vectors must be either 1 or equal to self.expansion_factor
            tf.Assert(tf.shape(r_vectors_excitation)[1] == 1 or
                      tf.shape(r_vectors_excitation)[1] == self.expansion_factor,
                      ["Shape missmatch for input argument r_vectors_excitation in SliceProfile!"
                       " Repetions axis must match expansion factor or 1, but got", tf.shape(r_vectors_excitation),
                       self.expansion_factor])
            tf.Assert(tf.shape(r_vectors_excitation)[2] == 1,
                      ["Shape missmatch for input argument r_vectors_excitation in SliceProfile!"
                       " k-space sample axis must be equal to 1, but got: ", tf.shape(r_vectors_excitation)])
            input_shape = tf.shape(signal_tensor)

            relative_coords = r_vectors_excitation - tf.reshape(self.slice_position, [1, -1, 1, 3])
            s_coords = tf.einsum("vrki, ri -> vrk", relative_coords, self.slice_normal)
            profile_factors = self.slice_profile(s_coords)
            profile_factors = tf.complex(profile_factors, tf.zeros_like(profile_factors))

            # Case 1: expand-dimensions
            if self.expand_repetitions or self.expansion_factor == 1:
                temp = tf.einsum('vrk, vek -> vrek', signal_tensor, profile_factors)
                result = tf.reshape(temp, (input_shape[0], -1, input_shape[2]))
            else:  # Case 2: repetition-axis of signal_tensor must match self.expansion_factor
                tf.Assert(input_shape[1] == self.expansion_factor,
                          ["Shape missmatch for input argument signal_tensor for case no-expand in SliceProfile! "
                           "Expected repetitions axis == self.expansion factor but got: ", input_shape, " | ",
                           self.expansion_factor])
                result = tf.einsum('vrk, vrk -> vrk', signal_tensor, profile_factors)
            return result

    def slice_profile(self, s_coord: tf.Tensor) -> tf.Tensor:
        """ Computes the slice profile weighting factor for each through-slice position passed in. 
        
        This method can be overwritten by a subclass to implement a more sophisticated slice-profile.

        :param s_coord: arbitrary shaped tensor containing the values for
                        through-slice coordinate relative to slice position
        :return: factor between 0, 1 for each position (of stame shape as s_coord)
        """
        return tf.where(tf.abs(s_coord) < tf.reshape(self.slice_thickness, [1, -1, 1]) / 2,
                        tf.ones_like(s_coord), tf.zeros_like(s_coord))


class LocalLookREST(BaseSignalModel):
    """Simplified Local Look with REST slabs module, computing a weighting from 0 to 1 depending on
    MPS position (Box-selective excitation).

    .. note::

        To modify the actual profile per M/P/S direction you can create a subclass of this class that
         implements a different 'box_profile' method.

    .. dropdown:: Example Images

        .. image:: _static/api/analytic/contrast_box_profile.png

    .. dropdown:: Example Usage

        uniform_mesh = pyvista.UniformGrid(spacing=(0.001, 0.001, 0.001), dimensions=(100, 100, 100), origin=(-0.05, -0.05, -0.05))
        r_vectors = tf.constant(uniform_mesh.points, dtype=tf.float32)
        slice_normal = np.eye(3, 3)
        readouts = np.roll(np.eye(3, 3), 1, axis=0)
        phase_encodes = np.roll(np.eye(3, 3), 2, axis=0)
        slice_position = Quantity([[0, 1, 1], [1, 0, 0], [0, 0, 1]], "cm").m_as("m")
        spatial_extends = Quantity([[3, 2, 0.5], [5, 10, 1], [8, 6, 2]], "cm").m_as("m") * 1.5


        rotation_matrices = tf.stack([readouts, phase_encodes, slice_normal], axis=1)

        lolo_mod = cmrsim.analytic.contrast.LocalLookREST(expand_repetitions=True, slice_normal=slice_normal,
                                                          readout_direction=readouts, phase_encoding_direction=phase_encodes,
                                                          slice_position=slice_position, spatial_extends=spatial_extends)


        r_vectors_excitation = tf.reshape(r_vectors, [-1, 1, 1, 3])
        signal_start = tf.ones(r_vectors_excitation.shape[:-1], dtype=tf.complex64)


        signal_out = lolo_mod(signal_tensor=signal_start, r_vectors_excitation=r_vectors_excitation).numpy()
        for i in range(signal_out.shape[1]):
            uniform_mesh[f"signal_out{i}"] = np.abs(signal_out)[:, i, 0]

    :param expand_repetitions: if True, expands repetition axes with the factor determined by the first axes of the
                                following input arguments
    :param slice_normal: (expansion_factor, 3) vector defining the slice normal of the excitation slice
    :param readout_direction: (expansion_factor, 3) vector defining the readout direction
    :param phase_encoding_direction: (expansion_factor, 3) vector defining the phase encoding direction
    :param slice_position: (expansion_factor, 3) vector determining the slice-center-point
    :param spatial_extends: (expansion_factor, 3) box-width per M-P-S direction around the slice-position
    :param device:
    """
    #: Additional mandatory keyword arguments for call
    required_quantities = ('r_vectors_excitation', )
    #: (expansion_factor, 4, 4) orientation matrix containing the transformation matrix from r_vectors into MPS
    #: coordinates. Is composed from slice_normal, phase_encoding and readout directions. matrix per repetition
    #: is guaranteed to be orthogonal
    orientation_matrix: tf.Variable
    #: (expansion_factor, 3) spatial extend per M-P-S directions (conceptually equivalent to slice-thickness)
    spatial_extend: tf.Variable
    #: (expansion_factor, 3) vector defining the slice normal of the excitation slice
    slice_normal: tf.Variable = None
    #: (expansion_factor, 3) vector determining the slice-center-point
    slice_position: tf.Variable = None

    def __init__(self, expand_repetitions: bool,
                 slice_normal: Sequence[Union[float, Sequence[float]]],
                 readout_direction: Sequence[Union[float, Sequence[float]]],
                 phase_encoding_direction: Sequence[Union[float, Sequence[float]]],
                 slice_position: Sequence[Union[float, Sequence[float]]],
                 spatial_extends: Sequence[Union[float, Sequence[float]]],
                 device: str = None):

        slice_normal = tf.reshape(tf.constant(slice_normal, dtype=tf.float32), (-1, 3))
        readout_direction = tf.reshape(tf.constant(readout_direction, dtype=tf.float32), (-1, 3))
        phase_encoding_direction = tf.reshape(tf.constant(phase_encoding_direction, dtype=tf.float32), (-1, 3))
        slice_position = tf.reshape(tf.constant(slice_position, dtype=tf.float32), (-1, 3))
        spatial_extends = tf.reshape(tf.constant(spatial_extends, dtype=tf.float32), (-1, 3))

        self._validate_shapes(slice_normal, readout_direction, phase_encoding_direction,
                              slice_position, spatial_extends)

        super(LocalLookREST, self).__init__(name="lolo_rest", expand_repetitions=expand_repetitions,
                                            device=device)

        transformation_matrices = np.zeros([len(slice_normal), 4, 4], dtype=np.float32)
        transformation_matrices[:, :3, :3] = np.stack([readout_direction, phase_encoding_direction,
                                                       slice_normal], axis=1)
        transformation_matrices[:, :3, 3] = slice_position
        transformation_matrices[:, 3, 3] = 1.
        self.orientation_matrix = tf.Variable(transformation_matrices, shape=(None, 4, 4), dtype=tf.float32)
        self.slice_position = tf.Variable(slice_position, shape=(None, 3), dtype=tf.float32)
        self.spatial_extend = tf.Variable(spatial_extends, shape=(None, 3), dtype=tf.float32)
        self.update()


    @staticmethod
    def _validate_shapes(slice_normal, readout_direction, phase_encoding_direction, slice_position, spatial_extends):
        """Checks if the number of normals/positions/thickness is the same
        :raises: ValueError - if len(...) of all input arguments are not equal
                            - if MPS directions are not orthonormal per repetition
        """
        expansion_factors = [len(arg) for arg in (slice_normal, readout_direction, phase_encoding_direction,
                                                  slice_position, spatial_extends)]
        if not all([e == expansion_factors[0] for e in expansion_factors]):
            raise ValueError("Must specify the same number of slice normals/readouts/phase encode/positions/thickness"
                             f" but got: {expansion_factors}")

        rotation_matrices = tf.stack([readout_direction, phase_encoding_direction, slice_normal], axis=1)
        orthonormality = tf.einsum("nij, njk -> nik", rotation_matrices, tf.transpose(rotation_matrices, [0, 2, 1]))
        orthonormality_bool = [np.allclose(mat, np.eye(3, 3), atol=1e-3) for mat in orthonormality]

        if not all(orthonormality_bool):
            raise ValueError("All encoding directions per repetitions must form an orthonormal basis: "
                             f"{orthonormality_bool} \n {orthonormality}")

    def update(self):
        self._validate_shapes(self.orientation_matrix.read_value()[:, 0, :3],
                              self.orientation_matrix.read_value()[:, 1, :3],
                              self.orientation_matrix.read_value()[:, 2, :3],
                              self.slice_position.read_value(),
                              self.spatial_extend.read_value())
        self.expansion_factor.assign(tf.shape(self.orientation_matrix.read_value())[0])


    def __call__(self, signal_tensor: tf.Tensor, r_vectors_excitation: tf.Tensor, **kwargs):  # noqa
        """ Call function for analytice local look with REST slabs weighting

        :raises: AssertionError - r_vectors_excitation.shape[1] not equal to 1 or self.expansion_factor
                                - r_vectors_excitation.shape[2] is not equal to 1 (k-samples not supported here)
        :param signal_tensor: (#batch, [#repetitions, 1], #ksamples)
        :param r_vectors_excitation: (#batch, [#repetition, 1], 1, 3)
        :return: signal_tensor weighted by box-selective excitation
        """

        with tf.device(self.device):
            # All Cases --> repetitions-axis of argument r_vectors must be either 1 or equal to self.expansion_factor
            tf.Assert(tf.shape(r_vectors_excitation)[1] == 1 or
                      tf.shape(r_vectors_excitation)[1] == self.expansion_factor,
                      ["Shape missmatch for input argument r_vectors_excitation in SliceProfile!"
                       " Repetions axis must match expansion factor or 1, but got", tf.shape(r_vectors_excitation),
                       self.expansion_factor])
            tf.Assert(tf.shape(r_vectors_excitation)[2] == 1,
                      ["Shape missmatch for input argument r_vectors_excitation in SliceProfile!"
                       " k-space sample axis must be equal to 1, but got: ", tf.shape(r_vectors_excitation)])
            input_shape = tf.shape(signal_tensor)

            relative_coords = r_vectors_excitation - tf.reshape(self.slice_position, [1, -1, 1, 3])
            augmented_coords = tf.concat([relative_coords, tf.ones_like(relative_coords[..., :1])], axis=-1)
            mps_coords = tf.einsum("rij, vrki-> vrkj", self.orientation_matrix, augmented_coords)
            profile_factors = self.box_profile(mps_coords)
            profile_factors = tf.complex(profile_factors, tf.zeros_like(profile_factors))

            # Case 1: expand-dimensions
            if self.expand_repetitions or self.expansion_factor == 1:
                temp = tf.einsum('vrk, vek -> vrek', signal_tensor, profile_factors)
                result = tf.reshape(temp, (input_shape[0], -1, input_shape[2]))
            else:  # Case 2: repetition-axis of signal_tensor must match self.expansion_factor
                tf.Assert(input_shape[1] == self.expansion_factor,
                          ["Shape missmatch for input argument signal_tensor for case no-expand in SliceProfile! "
                           "Expected repetitions axis == self.expansion factor but got: ", input_shape, " | ",
                           self.expansion_factor])
                result = tf.einsum('vrk, vrk -> vrk', signal_tensor, profile_factors)
            return result

    def box_profile(self, mps_coords: tf.Tensor) -> tf.Tensor:
        """ Computes the spatial weighting factor based on the 3D coordinate passed in as argument.
        This method can be overwritten by a subclass to implement a more sophisticated weighting.
        
        :param mps_coords: arbitrary shaped tensor containing the values for MPS coordinate relative to slice position
        :return: factor between 0, 1 for each position (of same shape as mps_coords[..., 0])
        """
        in_x = tf.abs(mps_coords[..., 0]) < tf.reshape(self.spatial_extend[..., 0], [1, -1, 1]) / 2
        in_y = tf.abs(mps_coords[..., 1]) < tf.reshape(self.spatial_extend[..., 1], [1, -1, 1]) / 2
        in_z = tf.abs(mps_coords[..., 2]) < tf.reshape(self.spatial_extend[..., 2], [1, -1, 1]) / 2
        binary_factors = tf.where(tf.reduce_prod(tf.cast(tf.stack([in_x, in_y, in_z], axis=0), tf.float32), axis=0)> 0.,
                                  tf.ones_like(mps_coords[..., 0]), tf.zeros_like(mps_coords[..., 0]))
        return binary_factors
