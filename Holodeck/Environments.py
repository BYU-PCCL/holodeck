import subprocess
import atexit
import os
import numpy as np
from copy import copy

from .Exceptions import HolodeckException
from .ShmemClient import ShmemClient
from .Sensors import Sensors


class AgentDefinition(object):
    def __init__(self, agent_name, agent_type, sensors=list()):
        super(AgentDefinition, self).__init__()
        self.name = agent_name
        self.type = agent_type
        self.sensors = sensors


class HolodeckEnvironment(object):
    def __init__(self, agent_definitions, binary_path=None, task_key=None, height=512, width=512,
                 start_world=True, uuid="", gl_version=4):
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

        # Set up the agents
        agent_definitions = [agent_definitions] if type(agent_definitions) != list else agent_definitions
        self._client = ShmemClient(self._uuid)
        self._all_agents = self._prepare_agents(agent_definitions)
        self._agent = self._all_agents[0]
        self._agent_dict = {x.name: x for x in self._all_agents}
        self._sensor_map = dict()

        # Set the default state function
        self.num_agents = len(self._all_agents)
        self._default_state_fn = self._get_single_state if self.num_agents == 1 else self._get_full_state

        # Subscribe settings
        self._reset_ptr = self._client.subscribe_setting("RESET", [1], np.bool)
        self._reset_ptr[0] = False

        # Subscribe sensors
        for agent in agent_definitions:
            self.add_state_sensors(agent.name, [Sensors.TERMINAL, Sensors.REWARD])
            self.add_state_sensors(agent.name, agent.sensors)

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
        return self._default_state_fn()

    def render(self):
        pass

    def step(self, action):
        self._agent.act(action)

        self._client.release()
        self._client.acquire()

        return self._get_single_state()

    def act(self, agent_name, action):
        self._agent_dict[agent_name].act(action)

    def tick(self):
        self._client.release()
        self._client.acquire()
        return self._get_full_state()

    def _get_single_state(self):
        reward = None
        terminal = None
        for sensor in self._sensor_map[self._agent.name]:
            if sensor == Sensors.REWARD:
                reward = self._sensor_map[self._agent.name][sensor][0]
            elif sensor == Sensors.TERMINAL:
                terminal = self._sensor_map[self._agent.name][sensor][0]

        return copy(self._sensor_map[self._agent.name]), reward, terminal, None

    def _get_full_state(self):
        return copy(self._sensor_map)

    def add_state_sensors(self, agent_name, sensors):
        if type(sensors) == list:
            for sensor in sensors:
                self.add_state_sensors(agent_name, sensor)
        else:
            self._client.subscribe_sensor(agent_name,
                                          Sensors.name(sensors),
                                          Sensors.shape(sensors),
                                          Sensors.dtype(sensors))
            if agent_name not in self._sensor_map:
                self._sensor_map[agent_name] = dict()
            self._sensor_map[agent_name][sensors] = self._client.get_sensor(agent_name, Sensors.name(sensors))

    def _prepare_agents(self, agent_definitions):
        if type(agent_definitions) == list:
            return [self._prepare_agents(x)[0] for x in agent_definitions]
        return [agent_definitions.type(client=self._client, name=agent_definitions.name)]
