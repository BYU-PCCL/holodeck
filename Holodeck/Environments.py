import subprocess
import atexit
import os
import numpy as np
from copy import copy

from .Exceptions import HolodeckException
from .ShmemClient import ShmemClient
from .Sensors import Sensors


class HolodeckEnvironment(object):
    def __init__(self, agent_type, agent_name, binary_path=None, task_key=None, height=512, width=512, start_world=True,
                 sensors=None, uuid="", gl_version=4):
        self._state_sensors = []
        self._height = height
        self._width = width
        self._uuid = uuid

        if start_world:
            if os.name == "posix":
                self.__linux_start_process__(binary_path, task_key, gl_version)
            elif os.name == "nt":
                self.__windows_start_process__(binary_path, task_key)
            else:
                raise HolodeckException("Unknown platform: " + os.name)

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

    def __linux_start_process__(self, binary_path, task_key, gl_version):
        import posix_ipc
        loading_semaphore = posix_ipc.Semaphore("/HOLODECK_LOADING_SEM" + self._uuid, os.O_CREAT | os.O_EXCL,
                                                initial_value=0)
        self._world_process = subprocess.Popen([binary_path, task_key, '-HolodeckOn', '-opengl' + str(gl_version),
                                                '-SILENT', '-LOG=HolodeckLog.txt','-ResX=' + str(self._width),
                                                "-ResY=" + str(self._height), "--HolodeckUUID=" + self._uuid],
                                               stdout=open(os.devnull, 'w'),
                                               stderr=open(os.devnull, 'w'))
        atexit.register(self.__on_exit__)
        try:
            loading_semaphore.acquire(100)
        except posix_ipc.BusyError:
            raise HolodeckException("Timed out waiting for binary to load")
        loading_semaphore.unlink()

    def __windows_start_process__(self, binary_path, task_key):
        import win32event
        loading_semaphore = win32event.CreateSemaphore(None, 0, 1, "Global\\HOLODECK_LOADING_SEM" + self._uuid)
        self._world_process = subprocess.Popen([binary_path, task_key, '-HolodeckOn', '-SILENT', '-LOG=HolodeckLog.txt',
                                                '-ResX=' + str(self._width), " -ResY=" + str(self._height),
                                                "--HolodeckUUID=" + self._uuid],
                                               stdout=open(os.devnull, 'w'),
                                               stderr=open(os.devnull, 'w'))
        atexit.register(self.__on_exit__)
        response = win32event.WaitForSingleObject(loading_semaphore, 100000)  # 100 second timeout
        if response == win32event.WAIT_TIMEOUT:
            raise HolodeckException("Timed out waiting for binary to load")

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
        self._agent.act(action)

        self._client.release()
        self._client.acquire()

        return self._get_state()

    def _get_state(self):
        reward = None
        terminal = None
        for sensor in self._state_sensors:
            if sensor == Sensors.REWARD:
                reward = self._sensor_map[sensor][0]
            elif sensor == Sensors.TERMINAL:
                terminal = self._sensor_map[sensor][0]

        return copy(self._sensor_map), reward, terminal, None

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
