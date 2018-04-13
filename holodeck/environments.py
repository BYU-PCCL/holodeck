"""Module containing the environment interface for Holodeck.
An environment contains all elements required to communicate with a world binary or HolodeckCore editor.
It specifies an environment, which contains a number of agents, and the interface for communicating with the agents.
"""
import atexit
import os
import subprocess
from copy import copy

from holodeck.hyperparameters import *
from holodeck.command import *
from holodeck.exceptions import HolodeckException
from holodeck.sensors import Sensors
from holodeck.shmemclient import ShmemClient


class AgentDefinition(object):
    """A class for declaring what agents are expected in a particular holodeck Environment."""
    __agent_keys__ = {"DiscreteSphereAgent": DiscreteSphereAgent,
                      "UAVAgent": UAVAgent,
                      "AndroidAgent": AndroidAgent,
                      "NavAgent": NavAgent,
                      DiscreteSphereAgent: DiscreteSphereAgent,
                      UAVAgent: UAVAgent,
                      AndroidAgent: AndroidAgent,
                      NavAgent: NavAgent}

    @staticmethod
    def __convert_sensors(sensors):
        result = []
        for sensor in sensors:
            if isinstance(sensor, str):
                result.append(Sensors.name_to_sensor(sensor))
            else:
                result.append(sensor)
        return result

    def __init__(self, agent_name, agent_type, sensors=None):
        """Constructor for AgentDefinition.

        Positional Arguments:
        agent_name -- The name of the agent to control
        agent_type -- The type of HolodeckAgent to control, string or class reference

        Keyword Arguments:
        sensors -- A list of HolodeckSensors to read from this agent, string or class reference (default empty)
        """
        super(AgentDefinition, self).__init__()
        sensors = sensors or list()
        self.name = agent_name
        self.type = AgentDefinition.__agent_keys__[agent_type]
        self.sensors = AgentDefinition.__convert_sensors(sensors)


class HolodeckEnvironment(object):
    """The high level interface for interacting with a Holodeck world"""

    def __init__(self, agent_definitions, binary_path=None, task_key=None, height=512, width=512,
                 start_world=True, uuid="", gl_version=4):
        """Constructor for HolodeckEnvironment.

        Positional arguments:
        agent_definitions -- A list of AgentDefinition objects for which agents to expect in the environment

        Keyword arguments:
        binary_path -- The path to the binary to load the world from (default None)
        task_key -- The name of the map within the binary to load (default None)
        height -- The height to load the binary at (default 512)
        width -- The width to load the binary at (default 512)
        start_world -- Whether to load a binary or not (default True)
        uuid -- A unique identifier, used when running multiple instances of holodeck (default "")
        gl_version -- The version of OpenGL to use for Linux (default 4)
        """
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

        # Set up and add the agents
        self._client = ShmemClient(self._uuid)
        self._sensor_map = dict()
        self._all_agents = list()
        self._agent_dict = dict()
        agent_definitions = [agent_definitions] if not isinstance(agent_definitions, list) else agent_definitions
        self._hyper_parameters_map = dict()
        self._add_agents(agent_definitions)
        self._agent = self._all_agents[0]

        # Set the default state function
        self.num_agents = len(self._all_agents)
        self._default_state_fn = self._get_single_state if self.num_agents == 1 else self._get_full_state

        # Subscribe settings
        self._reset_ptr = self._client.subscribe_setting("RESET", [1], np.bool)
        self._reset_ptr[0] = False
        self._command_bool_ptr = self._client.subscribe_setting("command_bool", [1], np.bool)
        megabyte = 1048576  # This is the size of the command buffer that Holodeck expects/will read.
        self._command_buffer_ptr = self._client.subscribe_setting("command_buffer", [megabyte], np.byte)

        # ._commands holds commands that are queued up to write to the command buffer on tick.
        self._commands = CommandsGroup()
        self._should_write_to_command_buffer = False

        self._client.acquire()

    @property
    def action_space(self):
        """Gives the action space for the main agent."""
        return self._agent.action_space

    @property
    def observation_space(self):
        """Gives the observation space for the main agent."""
        # TODO(joshgreaves) : Implement this
        raise NotImplementedError()

    def info(self):
        """Returns a string with specific information about the environment."""
        result = list()
        result.append("Agents:\n")
        for agent in self._agent_definitions:
            result.append("\tName: ")
            result.append(agent.name)
            result.append("\n\tType: ")
            result.append(agent.type.__name__)
            result.append("\n\t")
            result.append("Sensors:\n")
            for sensor in agent.sensors:
                result.append("\t\t")
                result.append(Sensors.name(sensor))
                result.append("\n")
        return "".join(result)

    def reset(self):
        """Resets the environment, and returns the state.
        If it is a single agent environment, it returns that state for that agent. Otherwise, it returns a dict from
        agent name to state.
        """
        self._reset_ptr[0] = True
        self._client.release()
        self._client.acquire()
        return self._default_state_fn()

    def render(self):
        """Renders the environment. Currently does nothing."""
        pass

    def step(self, action):
        """Supplies an action to the main agent and tells the environment to tick once.
        Returns the state, reward, terminal, info tuple for the agent.

        Positional arguments:
        action -- An action for the main agent to carry out on the next tick
        """
        self._agent.act(action)

        self._handle_command_buffer()

        self._client.release()
        self._client.acquire()

        return self._get_single_state()

    def teleport(self, agent_name, location):
        """Loads up a command to teleport the target agent to any given location.
        The teleport will occur the next time a step is taken. If no rotation is given, rotation will be set to the
        default value: 0,0,0.
        """
        self._agent_dict[agent_name].teleport(location)

    def _handle_command_buffer(self):
        """Checks if we should write to the command buffer, writes all of the queued commands to the buffer, and then
        clears the contents of the self._commands list"""
        if self._should_write_to_command_buffer:
            self.write_to_command_buffer(self._commands.to_json())
            self._should_write_to_command_buffer = False
            self._commands.clear()

    def act(self, agent_name, action):
        """Supplies an action to a particular agent, but doesn't tick the environment.

        Positional arguments:
        agent_name -- The name of the agent to give the command to
        action -- The action for the agent specified to carry out on the next tick
        """
        self._agent_dict[agent_name].act(action)

    def tick(self):
        """Ticks the environment once. Returns a dict from agent name to state."""
        self._handle_command_buffer()
        self._client.release()
        self._client.acquire()
        return self._get_full_state()

    def add_state_sensors(self, agent_name, sensors):
        """Adds a sensor to a particular agent.

        Positional arguments:
        agent_name -- The name of the agent to add the sensor to
        sensors -- A list of, or single sensor to add to the agent
        """
        if isinstance(sensors, list):
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

    def spawn_agent(self, agent_definition, location):
        """Queues up a spawn agent command to be written to the command buffer. It will open up the respective buffers
        needed for sending commands to and receiving data from the agent.

        Positional arguments:
        agent_definition -- This is the agent to spawn, its name, and the buffers to open for the sensors. Use the
        AgentDefinition class.
        location -- The position to spawn the agent in the world, in XYZ coordinates. Expects a list, and must be 3
        arguments.
        """
        self._should_write_to_command_buffer = True
        self._add_agents(agent_definition)
        command_to_send = SpawnAgentCommand(location, agent_definition.name, agent_definition.type)
        self._commands.add_command(command_to_send)

    def write_to_command_buffer(self, to_write):
        """Writes to the command buffer. It will handle converting the string to the correct format.

        Positional arguments:
        to_write -- The string to write to the command buffer."""
        # TODO(mitch): Handle the edge case of writing too much data to the buffer.
        np.copyto(self._command_bool_ptr, True)
        to_write += '0'  # The gason JSON parser in holodeck expects a 0 at the end of the file.
        input_bytes = str.encode(to_write)
        for index, val in enumerate(input_bytes):
            self._command_buffer_ptr[index] = val

    def set_hyper_parameter(self, agent_name, parameter_index, value):
        """Sets a specific hyper parameter on a specific agent.

        Positional Arguments:
        agent_name -- the name of the agent
        parameter_index -- The index of the parameter to set
        value -- The value to set the parameter to.
        """
        if agent_name not in self._hyper_parameters_map:
            print("Agent does not exist: ", agent_name)
            return
        if parameter_index >= self._hyper_parameters_map[agent_name][0]:
            print("Invalid index of hyper parameter: ", parameter_index)
            return
        if parameter_index == 0:
            print("Cannot change the number of elements in the hyper parameters list")
            return
        self._hyper_parameters_map[agent_name][parameter_index] = value

    def get_hyper_parameters(self, agent_name):
        """Gets the list of hyper parameters for a specific agent.

        Positional Arguments:
        agent_name -- The agent for which to get the hyper parameters.
        return -- A list of the hyper parameters for a specific agent, or none if DNE
        """
        if agent_name not in self._hyper_parameters_map:
            print(agent_name, " does not exist.")
            return None
        return self._hyper_parameters_map[agent_name]

    def __linux_start_process__(self, binary_path, task_key, gl_version):
        import posix_ipc
        loading_semaphore = posix_ipc.Semaphore("/HOLODECK_LOADING_SEM" + self._uuid, os.O_CREAT | os.O_EXCL,
                                                initial_value=0)
        self._world_process = subprocess.Popen([binary_path, task_key, '-HolodeckOn', '-opengl' + str(gl_version),
                                                '-SILENT', '-LOG=HolodeckLog.txt', '-ResX=' + str(self._width),
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

    def _prepare_agents(self, agent_definitions):
        if isinstance(agent_definitions, list):
            return [self._prepare_agents(x)[0] for x in agent_definitions]
        return [agent_definitions.type(client=self._client, name=agent_definitions.name)]

    def _add_agents(self, agent_definitions):
        """Adds agents to the client. This sets up their shared memory and sensor linkages.
        Does not spawn an agent in the Holodeck, this is only for documenting and accessing already existing agents

        Positional Arguments:
        agent_definitions -- The agent(s) to add.
        """
        if not isinstance(agent_definitions, list):
            self._add_agents([agent_definitions])
            return
        prepared_agents = self._prepare_agents(agent_definitions)
        self._all_agents.extend(prepared_agents)
        for agent in prepared_agents:
            self._agent_dict[agent.name] = agent
        for agent in agent_definitions:
            self.add_state_sensors(agent.name, [Sensors.TERMINAL, Sensors.REWARD])
            self.add_state_sensors(agent.name, agent.sensors)
            self._subscribe_hyper_parameters(agent)

    def _subscribe_hyper_parameters(self, agent_definition):
        """Sets up the linkages with holodeck to set and get the hyper parameters of an agent.

        agent_definition --  The definition of the agent to subscribe hyper parameters for.
        """
        if isinstance(agent_definition, list):
            for agent in agent_definition:
                self._subscribe_hyper_parameters(agent)
        else:
            setting_name = agent_definition.name + "_hyper_parameter"
            shape = HyperParameters.shape(agent_definition.type)
            self._hyper_parameters_map[agent_definition.name] = self._client.subscribe_setting(setting_name,
                                                                                               shape,
                                                                                               np.float32)
