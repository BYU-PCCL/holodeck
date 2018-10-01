"""Definitions for different agents that can be controlled from Holodeck"""
import numpy as np
from functools import reduce

from holodeck.spaces import ContinuousActionSpace, DiscreteActionSpace


class ControlSchemes(object):
    """All allowed control schemes.

    Attributes:
        ANDROID_TORQUES (int): Default Android control scheme. Specify a torque for each joint.
        CONTINUOUS_SPHERE_DEFAULT (int): Default ContinuousSphere control scheme. Takes two commands,
            [forward_delta, turn_delta].
        DISCRETE_SPHERE_DEFAULT (int): Default DiscreteSphere control scheme. Takes a value, 0-4, which corresponds
            with forward, backward, right, and left.
        NAV_TARGET_LOCATION (int): Default NavAgent control scheme. Takes a target xyz coordinate.
        UAV_TORQUES (int): Default UAV control scheme. Takes torques for roll, pitch, and yaw, as well as thrust.
        UAV_ROLL_PITCH_YAW_RATE_ALT (int): Control scheme for UAV. Takes roll, pitch, yaw rate, and altitude targets.
    """
    ANDROID_TORQUES = 0

    CONTINUOUS_SPHERE_DEFAULT = 0

    DISCRETE_SPHERE_DEFAULT = 0

    NAV_TARGET_LOCATION = 0

    UAV_TORQUES = 0
    UAV_ROLL_PITCH_YAW_RATE_ALT = 1


class HolodeckAgent(object):
    """Base class for HolodeckAgents.

    Args:
        client (:obj:`HolodeckClient`): The HolodeckClient that this agent belongs with.
        name (str, optional): The name of the agent. Must be unique from other agents in the same environment.

    Attributes:
        name (str): The name of the agent.
    """

    def __init__(self, client, name="DefaultAgent"):
        self.name = name
        self._client = client

        self._num_control_schemes = len(self.control_schemes)
        self._max_control_scheme_length = max(map(lambda x: reduce(lambda i, j: i * j, x[1].buffer_shape),
                                                  self.control_schemes))

        self._action_buffer = self._client.malloc(name, [self._max_control_scheme_length], np.float32)
        # Teleport flag: 0: do nothing, 1: teleport, 2: rotate, 3: teleport and rotate
        self._teleport_bool_buffer = self._client.malloc(name + "_teleport_flag", [1], np.uint8)
        self._teleport_buffer = self._client.malloc(name + "_teleport_command", [3], np.float32)
        self._rotation_buffer = self._client.malloc(name + "_rotation_command", [3], np.float32)
        self._control_scheme_buffer = self._client.malloc(name + "_control_scheme", [1],
                                                          np.uint8)
        self._current_control_scheme = 0
        self.set_control_scheme(0)

    def act(self, action):
        """Sets the command for the agent. Action depends on the current control scheme.

        Args:
            action(np.ndarray): The action to take.
        """
        self.__act__(action)

    def set_control_scheme(self, index):
        """Sets the control scheme for the agent. See :obj:`ControlSchemes`.

        Args:
            index (int): The control scheme to use. Should be set with an enum from :obj:`ControlSchemes`.
        """
        self._current_control_scheme = index % self._num_control_schemes
        self._control_scheme_buffer[0] = self._current_control_scheme

    def teleport(self, location=None, rotation=None):
        """Teleports the agent to a specific location, with a specific rotation.

        Args:
            location (np.ndarray, optional): An array with three elements specifying the target world coordinate in meters.
            If None, keeps the current location. Defaults to None.
            rotation (np.ndarray, optional): An array with three elements specifying the target rotation of the agent.
            If None, keeps the current rotation. Defaults to None.

        Returns:
            None
        """
        val = 0
        if location is not None:
            val += 1
            np.copyto(self._teleport_buffer, location)
        if rotation is not None:
            np.copyto(self._rotation_buffer, rotation)
            val += 2
        self._teleport_bool_buffer[0] = val

    @property
    def action_space(self):
        """Gets an :obj:ActionSpace object for the particular agent and control scheme.

        Returns:
            :obj:ActionSpace child object: The action space for this agent and control scheme."""
        return self.control_schemes[self._current_control_scheme][1]

    @property
    def control_schemes(self):
        """A list of all control schemes for the agent. Each list element is a 2-tuple, with the
        first element containing a short description of the control scheme, and the second
        element containing the :obj:`ActionSpace` for the control scheme.

        Returns:
            list of tuples: 2-tuples of short description and :obj:`ActionSpace`
        """
        raise NotImplementedError("Child class must implement this function")

    def __act__(self, action):
        # The default act function is to copy the data,
        # but if needed it can be overridden
        np.copyto(self._action_buffer, action)

    def __repr__(self):
        return self.name


class UavAgent(HolodeckAgent):
    """A UAV (quadcopter) agent that can be controlled with direct torques or roll, pitch, yaw rate
    and altitude targets.
    Inherits from :obj:`HolodeckAgent`."""
    @property
    def control_schemes(self):
        return [("[pitch_torque, roll_torque, yaw_torque, thrust]",
                 ContinuousActionSpace([4])),
                ("[pitch_target, roll_target, yaw_rate_target, altitude_target",
                 ContinuousActionSpace([4]))]

    def __repr__(self):
        return "UavAgent " + self.name


class ContinuousSphereAgent(HolodeckAgent):
    """A basic sphere robot that moves on a plane. Has a continuous action space.
    Inherits from :obj:`HolodeckAgent`."""
    @property
    def control_schemes(self):
        return [("[forward_movement, rotation]", ContinuousActionSpace([2]))]

    def __repr__(self):
        return "ContinuousSphereAgent " + self.name


class DiscreteSphereAgent(HolodeckAgent):
    """A basic sphere robot that moves on a plane. Has a discrete action space.
    Inherits from :obj:`HolodeckAgent`."""
    @property
    def control_schemes(self):
        return [("0: Move forward\n1: Move backward\n2: Turn right\n3: Turn left",
                 DiscreteActionSpace([1], 0, 4, buffer_shape=[2]))]

    def __act__(self, action):
        actions = np.array([[2, 0], [-2, 0], [0, 2], [0, -2]])
        to_act = np.array(actions[action, :])

        np.copyto(self._action_buffer, to_act)

    def __repr__(self):
        return "DiscreteSphereAgent " + self.name


class AndroidAgent(HolodeckAgent):
    """An android agent that can be controlled via torques supplied to its joints.
    Inherits from :obj:`HolodeckAgent`."""
    @property
    def control_schemes(self):
        return [("[Bone Torques] * 94", ContinuousActionSpace([94]))]

    def __repr__(self):
        return "AndroidAgent " + self.name

    @staticmethod
    def joint_ind(joint_name):
        return AndroidAgent._joint_indices[joint_name]

    _joint_indices = {
        # Head, Spine, and Arm joints. Each has[swing1, swing2, twist]
        "head": 0,
        "neck_01": 3,
        "spine_02": 6,
        "spine_01": 9,
        "upperarm_l": 12,
        "lowerarm_l": 15,
        "hand_l": 18,
        "upperarm_r": 21,
        "lowerarm_r": 24,
        "hand_r": 27,

        # Leg Joints. Each has[swing1, swing2, twist]
        "thigh_l": 30,
        "calf_l": 33,
        "foot_l": 36,
        "ball_l": 39,
        "thigh_r": 42,
        "calf_r": 45,
        "foot_r": 48,
        "ball_r": 51,

        # First joint of each finger. Has only [swing1, swing2]
        "thumb_01_l": 54,
        "index_01_l": 56,
        "middle_01_l": 58,
        "ring_01_l": 60,
        "pinky_01_l": 62,
        "thumb_01_r": 64,
        "index_01_r": 66,
        "middle_01_r": 68,
        "ring_01_r": 70,
        "pinky_01_r": 72,

        # Second joint of each finger.Has only[swing1]
        "thumb_02_l": 74,
        "index_02_l": 75,
        "middle_02_l": 76,
        "ring_02_l": 77,
        "pinky_02_l": 78,
        "thumb_02_r": 79,
        "index_02_r": 80,
        "middle_02_r": 81,
        "ring_02_r": 82,
        "pinky_02_r": 83,

        # Third joint of each finger.Has only[swing1]
        "thumb_03_l": 84,
        "index_03_l": 85,
        "middle_03_l": 86,
        "ring_03_l": 87,
        "pinky_03_l": 88,
        "thumb_03_r": 89,
        "index_03_r": 90,
        "middle_03_r": 91,
        "ring_03_r": 92,
        "pinky_03_r": 93
    }


class NavAgent(HolodeckAgent):
    """A simple navigating agent that can be controlled by target xyz coordinates.
    Inherits from :obj:`HolodeckAgent`."""
    @property
    def control_schemes(self):
        return [("[x_target, y_target, z_target]", ContinuousActionSpace([3]))]

    def __repr__(self):
        return "NavAgent " + self.name

    def __act__(self, action):
        np.copyto(self._action_buffer, np.array(action) * 100)
