import Holodeck.HolodeckAgents
from gym import spaces
from multiprocessing import Process
import subprocess
import atexit
import os
import time
import numpy as np

from HolodeckClient import HolodeckClient
from HolodeckSensors import HolodeckSensor


class HolodeckEnvironment(object):
    def __init__(self, agent_type, agent_name, task_key=None, height=256, width=256, start_world=True):
        self._state_sensors = []
        self._height = height
        self._width = width
        self._client = HolodeckClient()
        self._agent = agent_type(client=self._client, name=agent_name)
        self._sensor_map = dict()

        if start_world:
            if os.name == "posix":
                self.__linux_start_process__(task_key)
            elif os.name == "nt":
                self.__windows_start_process__(task_key)
            else:
                print "Unknown platform:", os.name
                raise NotImplementedError()

        # Subscribe settings
        self._reset_ptr = self._client.subscribe_setting("RESET", [1], np.bool)
        self._reset_ptr[0] = False

        # Subscribe sensors
        self.add_state_sensors([HolodeckSensor.TERMINAL, HolodeckSensor.REWARD])

        # TODO: Make sure this waits for the Holodeck binary to start up...
        time.sleep(1)

    def __linux_start_process__(self, task_key):
        task_map = {
            "TrainStation_UAV": "./worlds/TrainStation_UAV_v1.02/LinuxNoEditor/Holodeck/Binaries/Linux/Holodeck",
            "MazeWorld_UAV": "./worlds/MazeWorld_UAV_v1.00/LinuxNoEditor/Holodeck/Binaries/Linux/Holodeck",
            "ForestWorld_UAV": "./worlds/ForestWorld_UAV_v1.00/LinuxNoEditor/Holodeck/Binaries/Linux/Holodeck",
            "MazeWorld_sphere": "./worlds/MazeWorld_sphere_v1.00/LinuxNoEditor/Holodeck/Binaries/Linux/Holodeck",
            "ExampleWorld_android": ("./worlds/ExampleWorld_android_v1.00/LinuxNoEditor/Holodeck/"
                                     "Binaries/Linux/Holodeck")
        }

        self._world_process = subprocess.Popen([task_map[task_key], '-opengl4', '-SILENT', '-LOG=MyLog.txt',
                                                '-ResX=' + str(self._width), " -ResY=" + str(self._height)],
                                               stdout=open(os.devnull, 'w'),
                                               stderr=open(os.devnull, 'w'))
        atexit.register(self.__on_exit__)

    def __windows_start_process__(self, task_key):
        task_map = {
            "TrainStation_UAV": "./worlds/TrainStation_UAV_v1.02/WindowsNoEditor/Holodeck/Binaries/Win64/Holodeck",
            "MazeWorld_UAV": "./worlds/MazeWorld_UAV_v1.00/WindowsNoEditor/Holodeck/Binaries/Win64/Holodeck",
            "ForestWorld_UAV": "./worlds/ForestWorld_UAV_v1.00/WindowsNoEditor/Holodeck/Binaries/Linux/Holodeck",
            "MazeWorld_sphere": "./worlds/MazeWorld_sphere_v1.00/WindowsNoEditor/Holodeck/Binaries/Linux/Holodeck",
            "ExampleWorld_android": ("./worlds/ExampleWorld_android_v1.00/WindowsNoEditor/Holodeck/"
                                     "Binaries/Win64/Holodeck.exe")
        }

        self._world_process = subprocess.Popen([task_map[task_key], '-SILENT', '-LOG=MyLog.txt',
                                                '-ResX=' + str(self._width), " -ResY=" + str(self._height)],
                                               stdout=open(os.devnull, 'w'),
                                               stderr=open(os.devnull, 'w'))
        atexit.register(self.__on_exit__)

    def __on_exit__(self):
        if hasattr(self, '_world_process'):
            self._world_process.kill()

    @property
    def action_space(self):
        return self._agent.action_space

    @property
    def observation_space(self):
        # TODO(joshgreaves) : Implement this
        raise NotImplementedError()

    def reset(self):
        self._client.acquire()
        self._reset_ptr[0] = True
        self._client.release()

    def render(self):
        pass

    def step(self, action):
        # note: this assert currently doesn't work with discrete sphere robot because it's a one hot vector
        # assert action.shape == self.action_space.sample().shape, (action.shape, self.action_space.sample().shape)
        # self.frames += 1
        self._client.acquire()

        self._agent.act(action)

        result = []
        reward = None
        terminal = None
        for sensor in self._state_sensors:
            if sensor == HolodeckSensor.REWARD:
                reward = self._sensor_map[sensor]
            elif sensor == HolodeckSensor.TERMINAL:
                terminal = self._sensor_map[sensor]
            else:
                result.append(self._sensor_map[sensor])

        self._client.release()
        return result, reward, terminal, None

    def add_state_sensors(self, sensors):
        if type(sensors) == list:
            for sensor in sensors:
                self.add_state_sensors(sensor)
        else:
            self._client.subscribe_sensor(self._agent.name,
                                          HolodeckSensor.name(sensors),
                                          HolodeckSensor.shape(sensors),
                                          HolodeckSensor.dtype(sensors))
            self._state_sensors.append(sensors)
            self._sensor_map[sensors] = self._client.get_sensor(self._agent.name, HolodeckSensor.name(sensors))
