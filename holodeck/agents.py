import numpy as np
from functools import reduce

class HolodeckAgent(object):
    def __init__(self, client, name="DefaultAgent"):
        self.name = name
        self._client = client

        self._num_control_schemes = len(self.control_schemes)
        self._max_control_scheme_length = max(map(lambda x: reduce(lambda i, j: i * j, x[1]), self.control_schemes))

        self._action_buffer = self._client.malloc(name, [self._max_control_scheme_length], np.float32)
        # teleport flag: 0: do nothing, 1: teleport, 2: rotate, 3: teleport and rotate
        self._teleport_bool_buffer = self._client.malloc(name + "_teleport_flag", [1], np.uint8)
        self._teleport_buffer = self._client.malloc(name + "_teleport_command", [3], np.float32)
        self._rotation_buffer = self._client.malloc(name + "_rotation_command", [3], np.float32)
        self._control_scheme_buffer = self._client.malloc(name + "_control_scheme", [1],
                                                          np.uint8)
        self.set_control_scheme(0)

    def act(self, action):
        self.__act__(action)

    def set_control_scheme(self, index):
        self._control_scheme_buffer[0] = index % self._num_control_schemes

    def teleport(self, location, rotation):
        # The default teleport function is to copy the data to the buffer and set the bool to true
        # It can be overridden if needs be.
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
        raise NotImplementedError()

    @property
    def control_schemes(self):
        raise NotImplementedError()

    def __act__(self, action):
        # The default act function is to copy the data,
        # but if needed it can be overridden
        np.copyto(self._action_buffer, action)

    def __repr__(self):
        return self.name


class UavAgent(HolodeckAgent):
    @property
    def action_space(self):
        # TODO(joshgreaves) : Remove dependency on gym
        # return spaces.Box(-1, 3.5, shape=[4])
        return None

    @property
    def control_schemes(self):
        return [("[pitch_torque, roll_torque, yaw_torque, thrust]", [4]),
                ("[pitch_target, roll_target, yaw_rate_target, altitude_target", [4])]

    def __repr__(self):
        return "UavAgent " + self.name


class ContinuousSphereAgent(HolodeckAgent):
    @property
    def action_space(self):
        # TODO(joshgreaves) : Remove dependency on gym
        # return spaces.Box(np.array([-1, -.25]), np.array([1, .25]))
        return None

    @property
    def control_schemes(self):
        return [("[forward_movement, rotation]", [2])]

    def __action_space_shape__(self):
        return [2]

    def __repr__(self):
        return "ContinuousSphereAgent " + self.name


class DiscreteSphereAgent(HolodeckAgent):
    @property
    def action_space(self):
        # TODO(joshgreaves) : Remove dependency on gym
        # return spaces.Discrete(4)
        return None

    def control_schemes(self):
        return [("0: Move forward\n1: Move backward\n2: Turn right\n3: Turn left", [2])]

    def __act__(self, action):
        actions = np.array([[2, 0], [-2, 0], [0, 2], [0, -2]])
        to_act = np.array(actions[action, :])

        np.copyto(self._action_buffer, to_act)

    def __repr__(self):
        return "DiscreteSphereAgent " + self.name


class AndroidAgent(HolodeckAgent):
    @property
    def action_space(self):
        # TODO(joshgreaves) : Remove dependency on gym
        # return spaces.Box(-1000, 1000, shape=[94])
        return None

    @property
    def control_schemes(self):
        return [("[Bone torques * 94]", [94])]

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
    @property
    def action_space(self):
        # TODO(joshgreaves) : Remove dependency on gym
        # return spaces.Box(-10000, 10000, shape=[3])
        pass

    @property
    def control_schemes(self):
        return [("[x_target, y_target, z_target]", [3])]

    def __repr__(self):
        return "NavAgent " + self.name
