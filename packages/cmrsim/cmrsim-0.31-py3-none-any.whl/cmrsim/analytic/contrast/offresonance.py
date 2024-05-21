__all__ = ["OffResonanceProperty", ]

from typing import Union, TYPE_CHECKING

import tensorflow as tf

from cmrsim.analytic.contrast.base import BaseSignalModel

if TYPE_CHECKING:
    import numpy as np


class OffResonanceProperty(BaseSignalModel):
    """ Initializes a module to calculate the phase contribution of an offresonance according to:

    .. math::

        M_{xy}^{i, \\prime} = M_{xy}^{i} exp(-j\gamma \\Delta B \\delta t),

    where :math:`\\delta t` is the duration from the RF-excitation center for GRE sequences
    while it is the temporal distance to the echo-center for SE sequences.

    .. note::
        This module does not expand the repetition axis, but it always broad-casts the internal
        calculations to work for all #repetions > 0

    :param sampling_times: timing of acquisition (ADC) events in milliseconds
                            of shape (#reps, #k-space-points)
    :param gamma: Gyromagnetic ratio in rad/ms/mT
    """
    #: Tuple of names specifying the input quantities that must be passed as keyword-arguments to
    #: the __call__ method of the operator instance.
    required_quantities = ('deltaB0', )

    #: timing of acquisition (ADC) events in milliseconds
    #: Assumes the duration from the RF-excitation center for GRE sequences and the temporal
    #: distance to the echo-center for SE sequences.
    sampling_times: tf.Variable

    def __init__(self, sampling_times: Union[tf.Tensor, 'np.ndarray'], gamma: float, 
                 expand_repetitions: bool, **kwargs):
        """
        :param sampling_times: timing of acquisition (ADC) events in milliseconds 
                                of shape (#reps, #k-space-points) 
        :param gamma: Gyromagnetic ratio in rad/ms/mT
        """

        super().__init__(expand_repetitions=expand_repetitions, name="offres", **kwargs)

        if not(len(sampling_times.shape) == 1 or len(sampling_times.shape) == 2):
            raise ValueError("Invalid shape for specified sampling_times. "
                             "Must either be only (#k-space-points) or "
                             f"(#repetitions, #k-space-points), but is: {sampling_times.shape}")
        if len(sampling_times.shape) == 1:
            sampling_times = tf.reshape(sampling_times, [1, -1])

        with tf.device(self.device):
            self.gamma = tf.constant(gamma, dtype=tf.float32)
            self.sampling_times = tf.Variable(tf.constant(sampling_times, tf.float32),
                                              shape=(None, None), dtype=tf.float32)
            self.expansion_factor = sampling_times.shape[0]

    def update(self):
        super().update()
        self.expansion_factor == tf.shape(self.sampling_times.read_value())[0]

    # pylint: disable=signature-differs
    @tf.function(jit_compile=True)
    def __call__(self, signal_tensor: tf.Tensor, deltaB0: tf.Tensor,  **kwargs):
        """ Evaluates the off-resonance operator under the assumption

        :param signal_tensor: (#voxel, #repetitions, #k-space-samples)
                            #repetitions and #k-space-samples can be1
        :param deltaB0: tf.Tensor (#voxel, 1, 1) in mT. 
        :param segment_index: int, if k-space is segmented for Memory reasons. defaults to 0
        :return: signal_tensor (#voxel, #repetition, #k-space-samples) with #k-space-samples > 1
        """
        with tf.device(self.device):
            input_shape = tf.shape(signal_tensor)
            n_samples = tf.shape(self.sampling_times)[-1]

            tf.Assert(tf.shape(deltaB0)[1] == 1 or tf.shape(deltaB0)[1] == self.expansion_factor,
                      ["Shape missmatch for input argument T2star, repetitions axis assumed to be 1 or ",
                       self.expansion_factor, "but revceived ",  tf.shape(deltaB0)])
            tf.Assert(input_shape[2] == 1 or input_shape[2] == n_samples, 
                      ["Shape missmatch for input argument signal_tensor and self.sampling_times", 
                       input_shape, tf.shape(self.sampling_times)])
            
            off_res_phase = self.sampling_times * deltaB0 * self.gamma
            phase_factor = tf.exp(-tf.complex(0., off_res_phase))  # (p, self.exp, k)

            if self.expand_repetitions or self.expansion_factor == 1:
                result = signal_tensor[:, :, tf.newaxis, :] * phase_factor[:, tf.newaxis, :, :]
                new_shape = tf.stack([input_shape[0], input_shape[1] * self.expansion_factor,
                                       n_samples], axis=0)
                result = tf.reshape(result, new_shape)
            else:
                tf.Assert(input_shape[1] == self.expansion_factor,
                          ["Shape missmatch for input argument signal_tensor for case no-expand"])
                result = signal_tensor * phase_factor
            return result



