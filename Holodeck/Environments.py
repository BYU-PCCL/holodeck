from __future__ import print_function

import subprocess
import atexit
import os
import time
import numpy as np

from .ShmemClient import ShmemClient
from .Sensors import Sensors


class HolodeckMaps:
    MAZE_WORLD_SPHERE = 1

    def __init__(self):
        print("No point in instantiating an object.")


class HolodeckEnvironment(object):
    def __init__(self, agent_type, agent_name, task_key=None, height=512, width=512, start_world=True, sensors=None,
                 uuid=""):
        self._state_sensors = []
        self._height = height
        self._width = width
        self._uuid = uuid

        if start_world:
            if os.name == "posix":
                self.__linux_start_process__(task_key)
            elif os.name == "nt":
                self.__windows_start_process__(task_key)
            else:
                print("Unknown platform:", os.name)
                raise NotImplementedError()

        # TODO(joshgreaves) - Send a message to show the world is ready
        time.sleep(10)
        self._client = ShmemClient(self._uuid)
        self._agent = agent_type(client=self._client, name=agent_name)
        self._sensor_map = dict()

        # Subscribe settings
        self._reset_ptr = self._client.subscribe_setting("RESET", [1], np.bool)
        self._reset_ptr[0] = False

        # Subscribe sensors
        self.add_state_sensors([Sensors.TERMINAL, Sensors.REWARD])
        if sensors is not None:
            self.add_state_sensors(sensors)

        self._client.acquire()

    def __linux_start_process__(self, task_key):
        task_map = {
            HolodeckMaps.MAZE_WORLD_SPHERE:
                "./worlds/MazeWorld_sphere_v1.00/Holodeck/Binaries/Linux/Holodeck",
        }

        self._world_process = subprocess.Popen([task_map[task_key], '-opengl4', '-SILENT', '-LOG=HolodeckLog.txt',
                                                '-ResX=' + str(self._width), "-ResY=" + str(self._height),
                                                "--HolodeckUUID=" + self._uuid],
                                               stdout=open(os.devnull, 'w'),
                                               stderr=open(os.devnull, 'w'))
        atexit.register(self.__on_exit__)

    def __windows_start_process__(self, task_key):
        task_map = {
            HolodeckMaps.MAZE_WORLD_SPHERE:
                "..\\build\\WindowsNoEditor\\Holodeck\\Binaries\\Win64\\Holodeck.exe",
        }

        self._world_process = subprocess.Popen([task_map[task_key], '-SILENT', '-LOG=HolodeckLog.txt',
                                                '-ResX=' + str(self._width), " -ResY=" + str(self._height),
                                                "--HolodeckUUID=" + self._uuid],
                                               stdout=open(os.devnull, 'w'),
                                               stderr=open(os.devnull, 'w'))
        atexit.register(self.__on_exit__)

    def __on_exit__(self):
        if hasattr(self, '_world_process'):
            self._world_process.kill()
        self._client.unlink()

    @property
    def action_space(self):
        return self._agent.action_space

    @property
    def observation_space(self):
        # TODO(joshgreaves) : Implement this
        raise NotImplementedError()

    def reset(self):
        self._reset_ptr[0] = True
        self._client.release()
        self._client.acquire()
        return self._get_state()

    def render(self):
        pass

    def step(self, action):
        # note: this assert currently doesn't work with discrete sphere robot because it's a one hot vector
        # assert action.shape == self.action_space.sample().shape, (action.shape, self.action_space.sample().shape)
        # self.frames += 1

        self._agent.act(action)

        self._client.release()
        self._client.acquire()

        return self._get_state()

    def _get_state(self):
        result = []
        reward = None
        terminal = None
        for sensor in self._state_sensors:
            if sensor == Sensors.REWARD:
                reward = self._sensor_map[sensor]
            elif sensor == Sensors.TERMINAL:
                terminal = self._sensor_map[sensor]
            else:
                result.append(self._sensor_map[sensor])

        return result, reward, terminal, None

    def add_state_sensors(self, sensors):
        if type(sensors) == list:
            for sensor in sensors:
                self.add_state_sensors(sensor)
        else:
            self._client.subscribe_sensor(self._agent.name,
                                          Sensors.name(sensors),
                                          Sensors.shape(sensors),
                                          Sensors.dtype(sensors))
            self._state_sensors.append(sensors)
            self._sensor_map[sensors] = self._client.get_sensor(self._agent.name, Sensors.name(sensors))
