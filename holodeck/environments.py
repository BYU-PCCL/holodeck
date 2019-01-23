"""Module containing the environment interface for Holodeck.
An environment contains all elements required to communicate with a world binary or HolodeckCore editor.
It specifies an environment, which contains a number of agents, and the interface for communicating with the agents.
"""
import atexit
import os
import subprocess
import sys
from copy import copy

from holodeck.command import *
from holodeck.exceptions import HolodeckException
from holodeck.sensors import Sensors
from holodeck.holodeckclient import HolodeckClient


class AgentDefinition(object):
    """A class for declaring what agents are expected in a particular holodeck Environment.

    Args:
        agent_name (str): The name of the agent to control.
        agent_type (str or type): The type of HolodeckAgent to control, string or class reference.
        sensors (list of (str or type)): A list of HolodeckSensors to read from this agent. Defaults to None.
    """
    __agent_keys__ = {"DiscreteSphereAgent": DiscreteSphereAgent,
                      "ContinuousSphereAgent": ContinuousSphereAgent,
                      "UavAgent": UavAgent,
                      "AndroidAgent": AndroidAgent,
                      "NavAgent": NavAgent,
                      DiscreteSphereAgent: DiscreteSphereAgent,
                      ContinuousSphereAgent: ContinuousSphereAgent,
                      UavAgent: UavAgent,
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
        super(AgentDefinition, self).__init__()
        sensors = sensors or list()
        self.name = agent_name
        self.type = AgentDefinition.__agent_keys__[agent_type]
        self.sensors = AgentDefinition.__convert_sensors(sensors)


class HolodeckEnvironment(object):
    """The high level interface for interacting with a Holodeck world.
    Most users will want an environment created for them via `holodeck.make`.

    Args:
        agent_definitions (list of :obj:`AgentDefinition`): Which agents to expect in the environment.
        binary_path (str, optional): The path to the binary to load the world from. Defaults to None.
        task_key (str, optional): The name of the map within the binary to load. Defaults to None.
        window_height (int, optional): The height to load the binary at. Defaults to 512.
        window_width (int, optional): The width to load the binary at. Defaults to 512.
        camera_height (int, optional): The height of all pixel camera sensors. Defaults to 256.
        camera_width (int, optional): The width of all pixel camera sensors. Defaults to 256.
        start_world (bool, optional): Whether to load a binary or not. Defaults to True.
        uuid (str): A unique identifier, used when running multiple instances of holodeck. Defaults to "".
        gl_version (int, optional): The version of OpenGL to use for Linux. Defaults to 4.
        show_viewport (bool, optional) If the viewport should be shown (Linux only) Defaults to True.
        ticks_per_sec (int, optional) Number of frame ticks per unreal second. Defaults to 30.
        copy_state (bool, optional) If the state should be copied or returned as a reference. Defaults to True.

    Returns:
        HolodeckEnvironment: A holodeck environment object.
    """

    def __init__(self, agent_definitions, binary_path=None, task_key=None, window_height=512, window_width=512,
                 camera_height=256, camera_width=256, start_world=True, uuid="", gl_version=4, verbose=False,
                 pre_start_steps=2, show_viewport=True, ticks_per_sec=30, copy_state=True):

        self._window_height = window_height
        self._window_width = window_width
        self._camera_height = camera_height
        self._camera_width = camera_width
        self._uuid = uuid
        self._pre_start_steps = pre_start_steps
        self._copy_state = copy_state
        self._ticks_per_sec = ticks_per_sec

        Sensors.set_primary_cam_size(window_height, window_width)
        Sensors.set_pixel_cam_size(camera_height, camera_width)

        if start_world:
            if os.name == "posix":
                self.__linux_start_process__(binary_path, task_key, gl_version, verbose=verbose, show_viewport=show_viewport)
            elif os.name == "nt":
                self.__windows_start_process__(binary_path, task_key, verbose=verbose)
            else:
                raise HolodeckException("Unknown platform: " + os.name)

        # Set up and add the agents
        self._client = HolodeckClient(self._uuid)
        self._sensor_map = dict()
        self._all_agents = list()
        self.agents = dict()
        self._hyperparameters_map = dict()
        self._add_agents(agent_definitions)
        self._agent = self._all_agents[0]

        # Set the default state function
        self.num_agents = len(self._all_agents)
        self._default_state_fn = self._get_single_state if self.num_agents == 1 else self._get_full_state

        # Subscribe settings
        self._reset_ptr = self._client.malloc("RESET", [1], np.bool)
        self._reset_ptr[0] = False
        self._command_bool_ptr = self._client.malloc("command_bool", [1], np.bool)
        megabyte = 1048576  # This is the size of the command buffer that Holodeck expects/will read.
        self._command_buffer_ptr = self._client.malloc("command_buffer", [megabyte], np.byte)

        # self._commands holds commands that are queued up to write to the command buffer on tick.
        self._commands = CommandsGroup()
        self._should_write_to_command_buffer = False

        self._client.acquire()
        
        # Flag indicates if the user has called .reset() before .tick() and .step()
        self._initial_reset = False

    @property
    def action_space(self):
        """Gives the action space for the main agent.

        Returns:
            ActionSpace: The action space for the main agent.
        """
        return self._agent.action_space

    def info(self):
        """Returns a string with specific information about the environment.
        This information includes which agents are in the environment and which sensors they have.

        Returns:
            str: The information in a string format.
        """
        result = list()
        result.append("Agents:\n")
        for agent in self._all_agents:
            result.append("\tName: ")
            result.append(agent.name)
            result.append("\n\tType: ")
            result.append(type(agent).__name__)
            result.append("\n\t")
            result.append("Sensors:\n")
            for sensor in self._sensor_map[agent.name].keys():
                result.append("\t\t")
                result.append(Sensors.name(sensor))
                result.append("\n")
        return "".join(result)

    def reset(self):
        """Resets the environment, and returns the state.
        If it is a single agent environment, it returns that state for that agent. Otherwise, it returns a dict from
        agent name to state.

        Returns:
            tuple or dict: For single agent environment, returns the same as `step`.
                For multi-agent environment, returns the same as `tick`.
        """
        self._initial_reset = True
        self._reset_ptr[0] = True
        self._commands.clear()

        for _ in range(self._pre_start_steps + 1):
            self.tick()

        for agent in self.agents:
            self.set_ticks_per_capture(agent, self.agents[agent].get_ticks_per_capture())

        return self._default_state_fn()

    def step(self, action):
        """Supplies an action to the main agent and tells the environment to tick once.
        Primary mode of interaction for single agent environments.

        Args:
            action (np.ndarray): An action for the main agent to carry out on the next tick.

        Returns:
            tuple: The (state, reward, terminal, info) tuple for the agent. State is a dictionary
            from sensor enum (see :obj:`holodeck.sensors.Sensors`) to np.ndarray.
            Reward is the float reward returned by the environment.
            Terminal is the bool terminal signal returned by the environment.
            Info is any additional info, depending on the world. Defaults to None.
        """
        if not self._initial_reset:
            raise HolodeckException("You must call .reset() before .step()")

        self._agent.act(action)

        self._handle_command_buffer()

        self._client.release()
        self._client.acquire()

        return self._get_single_state()

    def teleport(self, agent_name, location=None, rotation=None):
        """Teleports the target agent to any given location, and applies a specific rotation.

        Args:
            agent_name (str): The name of the agent to teleport.
            location (np.ndarray or list): XYZ coordinates (in meters) for the agent to be teleported to.
                If no location is given, it isn't teleported, but may still be rotated. Defaults to None.
            rotation (np.ndarray or list): A new rotation target for the agent.
                If no rotation is given, it isn't rotated, but may still be teleported. Defaults to None.
        """
        self.agents[agent_name].teleport(location, rotation)
        self.tick()

    def set_state(self, agent_name, location, rotation, velocity, angular_velocity):
        """Sets a new state for any agent given a location, rotation and linear and angular velocity. Will sweep and be
        blocked by objects in it's way however

        Args:
            agent_name (str): The name of the agent to teleport.
            location (np.ndarray or list): XYZ coordinates (in meters) for the agent to be teleported to.
            rotation (np.ndarray or list): A new rotation target for the agent.
            velocity (np.ndarray or list): A new velocity for the agent.
            angular velocity (np.ndarray or list): A new angular velocity for the agent.
        """
        self.agents[agent_name].set_state(location, rotation, velocity, angular_velocity)
        return self.tick()

    def act(self, agent_name, action):
        """Supplies an action to a particular agent, but doesn't tick the environment.
        Primary mode of interaction for multi-agent environments. After all agent commands are supplied,
        they can be applied with a call to `tick`.

        Args:
            agent_name (str): The name of the agent to supply an action for.
            action (np.ndarray or list): The action to apply to the agent. This action will be applied every
                time `tick` is called, until a new action is supplied with another call to act.
        """
        self.agents[agent_name].act(action)

    def tick(self):
        """Ticks the environment once. Normally used for multi-agent environments.

        Returns:
            dict: A dictionary from agent name to its full state. The full state is another dictionary
            from :obj:`holodeck.sensors.Sensors` enum to np.ndarray, containing the sensors information
            for each sensor. The sensors always include the reward and terminal sensors.
        """
        if not self._initial_reset:
            raise HolodeckException("You must call .reset() before .tick()")

        self._handle_command_buffer()
        self._client.release()
        self._client.acquire()
        return self._get_full_state()

    def add_state_sensors(self, agent_name, sensors):
        """Adds a sensor to a particular agent. This only works if the world you are running also includes
        that particular sensor on the agent.

        Args:
            agent_name (str): The name of the agent to add the sensor to.
            sensors (:obj:`HolodeckSensor` or list of :obj:`HolodeckSensor`): Sensors to add to the agent.
                Should be objects that inherit from :obj:`HolodeckSensor`.
        """
        if isinstance(sensors, list):
            for sensor in sensors:
                self.add_state_sensors(agent_name, sensor)
        else:
            if agent_name not in self._sensor_map:
                self._sensor_map[agent_name] = dict()

            self._sensor_map[agent_name][sensors] = self._client.malloc(agent_name + "_" + Sensors.name(sensors),
                                                                        Sensors.shape(sensors),
                                                                        Sensors.dtype(sensors))

    def _enqueue_command(self, command_to_send):
        self._should_write_to_command_buffer = True
        self._commands.add_command(command_to_send)

    def spawn_agent(self, agent_definition, location):
        """Queues a spawn agent command. It will be applied when `tick` or `step` is called next.
        The agent won't be able to be used until the next frame.

        Args:
            agent_definition (:obj:`AgentDefinition`): The definition of the agent to spawn.
            location (np.ndarray or list): The position to spawn the agent in the world, in XYZ coordinates (in meters).
        """
        self._add_agents(agent_definition)
        self._enqueue_command(SpawnAgentCommand(location, agent_definition.name, agent_definition.type))

    def set_ticks_per_capture(self, agent_name, ticks_per_capture):
        """Queues a rgb camera rate command. It will be applied when `tick` or `step` is called next.
        The specified agent's rgb camera will capture images every specified number of ticks.
        The sensor's image will remain unchanged between captures.
        This method must be called after every call to env.reset.

        Args:
            agent_name (str): The name of the agent whose rgb camera should be modified.
            ticks_per_capture (int): The amount of ticks to wait between camera captures.
        """
        if not isinstance(ticks_per_capture, int) or ticks_per_capture < 1:
            print("Ticks per capture value " + str(ticks_per_capture) + " invalid")
        elif agent_name not in self.agents:
            print("No such agent %s" % agent_name)
        else:
            self.agents[agent_name].set_ticks_per_capture(ticks_per_capture)
            self._should_write_to_command_buffer = True
            command_to_send = RGBCameraRateCommand(agent_name, ticks_per_capture)
            self._commands.add_command(command_to_send)

    def set_fog_density(self, density):
        """Queue up a change fog density command. It will be applied when `tick` or `step` is called next.
        By the next tick, the exponential height fog in the world will have the new density. If there is no fog in the
        world, it will be automatically created with the given density.

        Args:
            density (float): The new density value, between 0 and 1. The command will not be sent if the given
        density is invalid.
        """
        if density < 0 or density > 1:
            raise HolodeckException("Fog density should be between 0 and 1")

        self._enqueue_command(ChangeFogDensityCommand(density))

    def draw_line(self, start, end, color=None, thickness=10.0):
        """Draws a debug line in the world

        Args:
            start (list of 3 floats): The start location of the line
            end (list of 3 floats): The end location of the line
            color (list of 3 floats): RGB values for the color
            thickness (float): thickness of the line
        """
        color = [255, 0, 0] if color is None else color
        self._should_write_to_command_buffer = True
        command_to_send = DebugDrawCommand(0, start, end, color, thickness)
        self._commands.add_command(command_to_send)

    def draw_arrow(self, start, end, color=None, thickness=10.0):
        """Draws a debug arrow in the world

        Args:
            start (list of 3 floats): The start location of the arrow
            end (list of 3 floats): The end location of the arrow
            color (list of 3 floats): RGB values for the color
            thickness (float): thickness of the arrow
        """
        color = [255, 0, 0] if color is None else color
        self._should_write_to_command_buffer = True
        command_to_send = DebugDrawCommand(1, start, end, color, thickness)
        self._commands.add_command(command_to_send)

    def draw_box(self, center, extent, color=None, thickness=10.0):
        """Draws a debug box in the world

        Args:
            center (list of 3 floats): The start location of the box
            extent (list of 3 floats): The extent of the box
            color (list of 3 floats): RGB values for the color
            thickness (float): thickness of the lines
        """
        color = [255, 0, 0] if color is None else color
        self._should_write_to_command_buffer = True
        command_to_send = DebugDrawCommand(2, center, extent, color, thickness)
        self._commands.add_command(command_to_send)

    def draw_point(self, loc, color=None, thickness=10.0):
        """Draws a debug point in the world

        Args:
            loc (list of 3 floats): The location of the point
            color (list of 3 floats): RGB values for the color
            thickness (float): thickness of the point
        """
        color = [255, 0, 0] if color is None else color
        self._should_write_to_command_buffer = True
        command_to_send = DebugDrawCommand(3, loc, [0, 0, 0], color, thickness)
        self._commands.add_command(command_to_send)

    def set_day_time(self, hour):
        """Queue up a change day time command. It will be applied when `tick` or `step` is called next.
        By the next tick, the lighting and the skysphere will be updated with the new hour. If there is no skysphere
        or directional light in the world, the command will not function properly but will not cause a crash.

        Args:
            hour (int): The hour in military time, between 0 and 23 inclusive.
        """
        self._enqueue_command(DayTimeCommand(hour % 24))

    def start_day_cycle(self, day_length):
        """Queue up a day cycle command to start the day cycle. It will be applied when `tick` or `step` is called next.
        The sky sphere will now update each tick with an updated sun angle as it moves about the sky. The length of a
        day will be roughly equivalent to the number of minutes given.

        Args:
            day_length (int): The number of minutes each day will be.
        """
        if day_length <= 0:
            raise HolodeckException("The given day length should be between above 0!")

        command_to_send = DayCycleCommand(True)
        command_to_send.set_day_length(day_length)
        self._enqueue_command(command_to_send)

    def stop_day_cycle(self):
        """Queue up a day cycle command to stop the day cycle. It will be applied when `tick` or `step` is called next.
        By the next tick, day cycle will stop where it is.
        """
        self._enqueue_command(DayCycleCommand(False))

    def teleport_camera(self, location, rotation):
        """Queue up a teleport camera command to stop the day cycle.
        By the next tick, the camera's location and rotation will be updated
        """
        self._enqueue_command(TeleportCameraCommand(location, rotation))

    def should_render_viewport(self, render_viewport):
        """Controls whether the viewport is rendered or not
        Args:
            render_viewport (boolean): If the viewport should be rendered
        """
        self._enqueue_command(RenderViewportCommand(render_viewport))

    def set_render_quality(self, render_quality):
        """Adjusts the rendering quality of Holodeck. 
        Args:
            render_quality (int): An integer between 0 and 3. 
                                    0 = low
                                    1 = medium
                                    2 = high
                                    3 = epic
        """
        self._enqueue_command(RenderQualityCommand(render_quality))

    def set_weather(self, weather_type):
        """Queue up a set weather command. It will be applied when `tick` or `step` is called next.
        By the next tick, the lighting, skysphere, fog, and relevant particle systems will be updated and/or spawned
        to the given weather. If there is no skysphere or directional light in the world, the command may not function
        properly but will not cause a crash.

        NOTE: Because this command can effect the fog density, any changes made by a change_fog_density command before
        a set_weather command called will be undone. It is recommended to call change_fog_density after calling set
        weather.

        Args:
            weather_type (str): The type of weather, which can be 'Rain' or 'Cloudy'. In all downloadable worlds,
            the weather is clear by default. If the given type string is not available, the command will not be sent.

        """
        if not SetWeatherCommand.has_type(weather_type.lower()):
            raise HolodeckException("Invalid weather type " + weather_type)

        self._enqueue_command(SetWeatherCommand(weather_type.lower()))

    def set_control_scheme(self, agent_name, control_scheme):
        """Set the control scheme for a specific agent.

        Args:
            agent_name (str): The name of the agent to set the control scheme for.
            control_scheme (int): A control scheme value (see :obj:`holodeck.agents.ControlSchemes`)
        """
        if agent_name not in self.agents:
            print("No such agent %s" % agent_name)
        else:
            self.agents[agent_name].set_control_scheme(control_scheme)

    def set_sensor_enabled(self, agent_name, sensor_name, enabled):
        """Enable or disable a sensor for an agent.

        Args:
            agent_name (str): The name of the agent whose sensor will be switched
            sensor_name (str): The name of the sensor to be switched
            enabled (bool): Boolean representing whether to enable or disable the sensor
        """
        if agent_name not in self._sensor_map:
            print("No such agent %s" % agent_name)
        else: 
            self._should_write_to_command_buffer = True
            command_to_send = SetSensorEnabledCommand(agent_name, sensor_name, enabled)
            self._commands.add_command(command_to_send)

    def __linux_start_process__(self, binary_path, task_key, gl_version, verbose, show_viewport=True):
        import posix_ipc
        out_stream = sys.stdout if verbose else open(os.devnull, 'w')
        loading_semaphore = posix_ipc.Semaphore('/HOLODECK_LOADING_SEM' + self._uuid, os.O_CREAT | os.O_EXCL,
                                                initial_value=0)
        # Copy the environment variables to remove the DISPLAY variable if we shouldn't show the viewport
        # see https://answers.unrealengine.com/questions/815764/in-the-release-notes-it-says-the-engine-can-now-cr.html?sort=oldest
        environment = dict(copy(os.environ))
        if not show_viewport:
            del environment['DISPLAY']

        self._world_process = subprocess.Popen([binary_path, task_key, '-HolodeckOn', '-opengl' + str(gl_version),
                                                '-LOG=HolodeckLog.txt', '-ResX=' + str(self._window_width),
                                                '-ResY=' + str(self._window_height),'-CamResX=' + str(self._camera_width),
                                                '-CamResY=' + str(self._camera_height), '--HolodeckUUID=' + self._uuid,
                                               '-TicksPerSec=' + str(self._ticks_per_sec)],
                                               stdout=out_stream,
                                               stderr=out_stream,
                                               env=environment)

        atexit.register(self.__on_exit__)

        try:
            loading_semaphore.acquire(100)
        except posix_ipc.BusyError:
            raise HolodeckException("Timed out waiting for binary to load. Ensure that holodeck is not being run with root priveleges.")
        loading_semaphore.unlink()

    def __windows_start_process__(self, binary_path, task_key, verbose):
        import win32event
        out_stream = sys.stdout if verbose else open(os.devnull, 'w')
        loading_semaphore = win32event.CreateSemaphore(None, 0, 1, "Global\\HOLODECK_LOADING_SEM" + self._uuid)
        self._world_process = subprocess.Popen([binary_path, task_key, '-HolodeckOn', '-LOG=HolodeckLog.txt',
                                                '-ResX=' + str(self._window_width), "-ResY=" + str(self._window_height),
                                                '-CamResX=' + str(self._camera_width),
                                                '-CamResY=' + str(self._camera_height), "--HolodeckUUID=" + self._uuid,
                                                '-TicksPerSec=' + str(self._ticks_per_sec)],
                                               stdout=out_stream, stderr=out_stream)
        atexit.register(self.__on_exit__)
        response = win32event.WaitForSingleObject(loading_semaphore, 100000)  # 100 second timeout
        if response == win32event.WAIT_TIMEOUT:
            raise HolodeckException("Timed out waiting for binary to load")

    def __on_exit__(self):
        if hasattr(self, '_world_process'):
            self._world_process.kill()
            self._world_process.wait(5)
        self._client.unlink()

    # Context manager APIs, allows `with` statement to be used
    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        # TODO: Surpress exceptions?
        self.__on_exit__()

    def _get_single_state(self):
        reward = None
        terminal = None
        for sensor in self._sensor_map[self._agent.name]:
            if sensor == Sensors.REWARD:
                reward = self._sensor_map[self._agent.name][sensor][0]
            elif sensor == Sensors.TERMINAL:
                terminal = self._sensor_map[self._agent.name][sensor][0]

        state = self._create_copy(self._sensor_map[self._agent.name]) if self._copy_state \
            else self._sensor_map[self._agent.name]
        return state, reward, terminal, None

    def _get_full_state(self):
        return self._create_copy(self._sensor_map) if self._copy_state else self._sensor_map

    def _create_copy(self, obj):
        if isinstance(obj, dict):  # Deep copy dictionary
            cp = dict()
            for k, v in obj.items():
                if isinstance(v, dict):
                    cp[k] = self._create_copy(v)
                else:
                    cp[k] = np.copy(v)
            return cp
        return None  # Not implemented for other types

    def _handle_command_buffer(self):
        """Checks if we should write to the command buffer, writes all of the queued commands to the buffer, and then
        clears the contents of the self._commands list"""
        if self._should_write_to_command_buffer:
            self._write_to_command_buffer(self._commands.to_json())
            self._should_write_to_command_buffer = False
            self._commands.clear()

    def _prepare_agents(self, agent_definitions):
        if isinstance(agent_definitions, list):
            return [self._prepare_agents(x)[0] for x in agent_definitions]
        return [agent_definitions.type(client=self._client, name=agent_definitions.name)]

    def _add_agents(self, agent_definitions):
        """Add specified agents to the client. Set up their shared memory and sensor linkages.
        Does not spawn an agent in the Holodeck, this is only for documenting and accessing already existing agents.
        This is an internal function.
        Positional Arguments:
        agent_definitions -- The agent(s) to add.
        """
        if not isinstance(agent_definitions, list):
            agent_definitions = [agent_definitions]
        prepared_agents = self._prepare_agents(agent_definitions)
        self._all_agents.extend(prepared_agents)
        for agent in prepared_agents:
            self.agents[agent.name] = agent
        for agent in agent_definitions:
            self.add_state_sensors(agent.name, [Sensors.TERMINAL, Sensors.REWARD])
            self.add_state_sensors(agent.name, agent.sensors)

    def _write_to_command_buffer(self, to_write):
        """Write input to the command buffer.  Reformat input string to the correct format.

        Args:
            to_write (str): The string to write to the command buffer.
        """
        # TODO(mitch): Handle the edge case of writing too much data to the buffer.
        np.copyto(self._command_bool_ptr, True)
        to_write += '0'  # The gason JSON parser in holodeck expects a 0 at the end of the file.
        input_bytes = str.encode(to_write)
        for index, val in enumerate(input_bytes):
            self._command_buffer_ptr[index] = val
