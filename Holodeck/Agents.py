from gym import spaces
import numpy as np


class HolodeckAgent(object):
    def __init__(self, client, name="DefaultAgent"):
        self.name = name
        self._client = client
        self._action_buffer, self._teleport_bool_buffer, self._teleport_buffer = \
            self._client.subscribe_command(name, self.__action_space_shape__())
        settings_buffer_name = name + "_settings"
        self._settings_buffer = self._client.subscribe_setting(settings_buffer_name,
                                                               self.__setting_space_shape__(),
                                                               np.float32)

    def act(self, action):
        self.__act__(action)

    def teleport(self, location):
        # The default teleport function is to copy the data to the buffer and set the bool to true
        # It can be overridden if needs be.
        np.copyto(self._teleport_buffer, location)
        np.copyto(self._teleport_bool_buffer, True)

    def get_setting(self, setting_index):
        return self._settings_buffer[setting_index]

    @property
    def action_space(self):
        raise NotImplementedError()

    def __action_space_shape__(self):
        raise NotImplementedError()

    def __setting_space_shape__(self):
        """Total number of items in the agent settings
        It is to be implemented by every subclass.
        """
        raise NotImplementedError

    def __act__(self, action):
        # The default act function is to copy the data,
        # but if needed it can be overridden
        np.copyto(self._action_buffer, action)


class UAVAgent(HolodeckAgent):
    @property
    def action_space(self):
        return spaces.Box(-1, 3.5, shape=[4])

    def __action_space_shape__(self):
        return [4]

    def __setting_space_shape__(self):
        return [26]  # This is the total number of constants in the c++ code that get exported.


class ContinuousSphereAgent(HolodeckAgent):
    @property
    def action_space(self):
        # return spaces.Box(-1, 1, shape=[2])
        return spaces.Box(np.array([-1, -.25]), np.array([1, .25]))

    def __action_space_shape__(self):
        return [2]

    def __setting_space_shape__(self):
        return [0]


class DiscreteSphereAgent(HolodeckAgent):
    @property
    def action_space(self):
        return spaces.Discrete(4)

    def __action_space_shape__(self):
        return [2]

    def __act__(self, action):
        actions = np.array([[2, 0], [-2, 0], [0, 2], [0, -2]])
        to_act = np.array(actions[action, :])

        np.copyto(self._action_buffer, to_act)

    def __setting_space_shape__(self):
        return [0]


class AndroidAgent(HolodeckAgent):
    @property
    def action_space(self):
        return spaces.Box(-1000, 1000, shape=[127])

    def __action_space_shape__(self):
        return [127]

    def __setting_space_shape__(self):
        return [0]

class NavAgent(HolodeckAgent):
    @property
    def action_space(self):
        return spaces.Box(-10000, 10000, shape=[3])

    def __action_space_shape__(self):
        return [3]

    def __setting_space_shape__(self):
        return [0]
