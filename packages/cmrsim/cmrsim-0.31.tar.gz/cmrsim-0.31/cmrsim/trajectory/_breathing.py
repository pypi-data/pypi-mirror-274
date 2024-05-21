__all__ = ["SimpleBreathingMotionModule"]

from typing import Dict

from pint import Quantity
import tensorflow as tf
import numpy as np

from cmrsim.trajectory import BaseTrajectoryModule


class SimpleBreathingMotionModule(BaseTrajectoryModule):
    """Trajectory module wrapping another trajectory module with a global
    pure translational breathing motion. Arbitrary 3D breathing curves can
    be specified on a regular time grid. This curve is linearly interpolated
    on calling the module.

    The wrapped trajectory module is assumed to gracefully handle potential
    out-of bound time-points (e.g. by assuming periodicity)

    :param sub_trajectory: Instance of a BaseTrajectoryModule-subclass
    :param breathing_curve: (t, 3) Tensor containing the 3D points of the
                breathing trajectory assumed to be on a uniform temporal grid
    :param breathing_cycle_duration: Duration of the given breathing trajectory
                in milliseconds
    """
    #: Reference to the wrapped trajectory module
    sub_trajectory: BaseTrajectoryModule
    #: Duration of the given breathing trajectory in milliseconds
    breathing_cycle_duration: tf.Tensor
    #: (t, 3) Tensor containing the 3D points of the breathing
    #: trajectory assumed to be on a uniform temporal grid
    breathing_curve: tf.Tensor
    #: Keeps track of the current timing when increment_particles is called.
    current_time_ms: tf.Variable

    def __init__(self, sub_trajectory: BaseTrajectoryModule,
                 breathing_curve: tf.Tensor, breathing_cycle_duration: tf.Tensor):
        """
        :param sub_trajectory: Trajectory module able to gracefully handle out-of bound time-points
                               (e.g. by assuming periodicity)
        :param breathing_curve: (t, 3)
        :param breathing_cycle_duration: (t, )
        """
        self.sub_trajectory = sub_trajectory
        self.breathing_cycle_duration = tf.constant(breathing_cycle_duration, dtype=tf.float32)
        self.breathing_curve = tf.constant(breathing_curve, dtype=tf.float32)
        self.current_time_ms = tf.Variable(0., dtype=tf.float32, shape=(), trainable=False)

    def __call__(self, initial_positions: tf.Tensor, timing: tf.Tensor,
                 **kwargs) -> (tf.Tensor, Dict):
        """Evaluates the contained trajectory module and adds the breathing displacement
        :param initial_positions: passed into the submodule
        :param timing: passed into submodule and is used to calculate breathing displacement
        :param kwargs: passed to submodule
        """
        positional_offset = self._interpolate_breathing_curve(timing)
        sub_trajectory_r, additional_fields = self.sub_trajectory(initial_positions=initial_positions,
                                                                  timing=timing, **kwargs)
        return positional_offset[tf.newaxis] + sub_trajectory_r, additional_fields

    def increment_particles(self, particle_positions: tf.Tensor, dt: tf.Tensor, **kwargs) -> (tf.Tensor, Dict):
        """Evaluates the contained trajectory module and adds the breathing displacement
        :param initial_positions: passed into the submodule
        :param timing: passed into submodule and is used to calculate breathing displacement
        :param kwargs: passed to submodule
        """
        prev_positional_offset = self._interpolate_breathing_curve(self.current_time_ms)
        particle_positions = particle_positions - prev_positional_offset
        _t = tf.reshape(self.current_time_ms.assign_add(dt), [1, ])
        positional_offset = self._interpolate_breathing_curve(_t)
        sub_trajectory_r, additional_fields = self.sub_trajectory.increment_particles(particle_positions, dt, **kwargs)
        return positional_offset + sub_trajectory_r, additional_fields

    def _interpolate_breathing_curve(self, timing: tf.Tensor):
        """ Assumes Regular grid definition in time of the breathing curve
        :param timing: (#batch, ) in ms
        """
        timing = tf.math.floormod(timing, self.breathing_cycle_duration)
        n_refpoints, channels = tf.unstack(tf.shape(self.breathing_curve), axis=0)
        mint = tf.constant(0, dtype=tf.float32)

        interval_width = (self.breathing_cycle_duration - mint) / tf.cast(n_refpoints - 1, tf.float32)

        t_norm = (timing - mint) / interval_width
        t_lref = tf.stop_gradient(tf.math.floor(t_norm))
        interp_weights = (1. - (t_norm - t_lref))[..., tf.newaxis]
        t_rref = t_lref + 1

        y_lref = tf.gather(self.breathing_curve, tf.cast(t_lref, tf.int32), batch_dims=0)
        y_rref = tf.gather(self.breathing_curve, tf.cast(t_rref, tf.int32), batch_dims=0)
        return y_lref * interp_weights + y_rref * (1 - interp_weights)

    def current_offset(self):
        """Returns the positional breathing offset for the current time"""
        return self._interpolate_breathing_curve(self.current_time_ms)

    @classmethod
    def from_sinosoidal_motion(cls, sub_trajectory: BaseTrajectoryModule,
                               breathing_period: Quantity, breathing_direction: np.ndarray,
                               breathing_amplitude: Quantity):
        """Instantiates a SimpleBreathingMotionModule from a sinusodial breathing curve"""

        breathing_period = tf.constant(breathing_period.m_as("ms"), dtype=tf.float32, shape=())
        motion_vector = tf.constant(breathing_direction / np.linalg.norm(breathing_direction), dtype=tf.float32,
                                    shape=(3,))
        motion_amplitude = tf.constant(breathing_amplitude.m_as("m"), dtype=tf.float32, shape=())
        normalized_timing = tf.cast(tf.linspace(0, 1, 200), tf.float32)

        sin_arg = normalized_timing * 2. * tf.constant(np.pi, dtype=tf.float32)
        breathing_trajectory = tf.reshape(motion_amplitude * motion_vector, [1, 3]) * tf.reshape(tf.math.sin(sin_arg),
                                                                                                 [-1, 1])
        return cls(sub_trajectory, breathing_curve=breathing_trajectory,
                   breathing_cycle_duration=breathing_period)
