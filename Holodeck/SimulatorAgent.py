from gym import spaces
import json
import threading
from collections import defaultdict
import time
import numpy as np


class SimulatorAgent(object):
    class TimeoutError(Exception):
        pass

    def __init__(self, hostname="localhost", port=8989, name="DefaultAgent", height=256, width=256,
                 grayscale=False):
        self.resolution = [height, width, 1 if grayscale else 3]

        self.state_locks = {}
        self.state = {}
        self.last_receive_error = None
        self.name = name

    def send_command(self, type, command):
        raise NotImplementedError()

    def subscribe(self, type, function):
        raise NotImplementedError()

    def unsubscribe(self, type, function):
        raise NotImplementedError()

    def act(self, action, sensors):
        print "Act not implemented"
        # raise NotImplementedError()

    @property
    def action_space(self):
        raise NotImplementedError()

    def __act__(self, action):
        raise NotImplementedError()


class UAVAgent(SimulatorAgent):
    @property
    def action_space(self):
        return spaces.Box(-1, 3.5, shape=[4])

    def __act__(self, action):
        self.send_command('UAVCommand', {
            "Roll": str(action[0]),
            "Pitch": str(action[1]),
            "YawRate": str(action[2]),
            "Altitude": str(action[3])
        })


class ContinuousSphereAgent(SimulatorAgent):
    @property
    def action_space(self):
        # return spaces.Box(-1, 1, shape=[2])
        return spaces.Box(np.array([-1, -.25]), np.array([1, .25]))

    def __act__(self, action):
        self.send_command('SphereRobotCommand', {
            "Forward": str(action[0]),
            "Right": str(action[1])
        })


class DiscreteSphereAgent(SimulatorAgent):
    @property
    def action_space(self):
        return spaces.Discrete(4)

    def __act__(self, action):
        actions = [(10, 0), (-10, 0), (0, 90), (0, -90)]
        to_act = None
        # for i, j in enumerate(action):
        #     if j == 1:
        #         to_act = actions[i]
        to_act = actions[action]

        if to_act is None:
            raise RuntimeError("Action must be one-hot")

        self.send_command('SphereRobotCommand', {
            "Forward": str(to_act[0]),
            "Right": str(to_act[1])
        })


class AndroidAgent(SimulatorAgent):
    @property
    def action_space(self):
        return spaces.Box(-1000, 1000, shape=[127])

    def __act__(self, action):
        action = map(str, action)
        self.send_command('AndroidCommand', {
            "ConstraintVector": action
        })
