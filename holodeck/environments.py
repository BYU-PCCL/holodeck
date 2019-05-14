"""Module containing the environment interface for Holodeck.
An environment contains all elements required to communicate with a world binary or HolodeckCore editor.
It specifies an environment, which contains a number of agents, and the interface for communicating with the agents.
"""
import atexit
import os
import subprocess
import sys
from copy import copy
import json

from holodeck.command import *
from holodeck.packagemanager import get_scenario, load_scenario_file
from holodeck.exceptions import HolodeckException
from holodeck.holodeckclient import HolodeckClient
from holodeck.agents import *
import holodeck.sensors

class HolodeckEnvironment(object):
    """Proxy for communicating with a Holodeck world

    Instantiate this object using :meth:`holodeck.holodeck.make`.

    Args:
        agent_definitions (:obj:`list` of :class:ntDefinition`):
            Which agents to expect in the environment.

        binary_path (:obj:`str`, optional):
            The path to the binary to load the world from. Defaults to None.

        task_key (:obj:`str`, optional):
            The name of the map within the binary to load. Defaults to None.

        window_height (:obj:`int`, optional):
            The height to load the game window at. Defaults to 512.

        window_width (:obj:`int`, optional):
            The width to load the game window at. Defaults to 512.

        start_world (:obj:`bool`, optional):
            Whether to load a binary or not. Defaults to True.

        uuid (:obj:`str`):
            A unique identifier, used when running multiple instances of holodeck. Defaults to "".

        gl_version (:obj:`int`, optional):
            The version of OpenGL to use for Linux. Defaults to 4.

        show_viewport (:obj:`bool`, optional):
            If the viewport should be shown (Linux only) Defaults to True.

        ticks_per_sec (:obj:`int`, optional):
            Number of frame ticks per unreal second. Defaults to 30.

        copy_state (:obj:`bool`, optional):
            If the state should be copied or returned as a reference. Defaults to True.

    """

    def __init__(self, agent_definitions=None, binary_path=None, scenario_key=None, window_height=512, window_width=512,
                 start_world=True, uuid="", gl_version=4, verbose=False,
                 pre_start_steps=2, show_viewport=True, ticks_per_sec=30, copy_state=True, scenario_path=None):

        if agent_definitions is None:
            agent_definitions = []

        # Initialize variables
        self._window_height = window_height
        self._window_width = window_width
        self._uuid = uuid
        self._pre_start_steps = pre_start_steps
        self._copy_state = copy_state
        self._ticks_per_sec = ticks_per_sec
        self._scenario_key = scenario_key
        self._scenario_path = scenario_path
        self._initial_agent_defs = agent_definitions
        self._spawned_agent_defs = []

        # Start world based on OS
        if start_world:
            world_key = scenario_key.split("-")[0]
            if os.name == "posix":
                self.__linux_start_process__(binary_path, world_key, gl_version, verbose=verbose, show_viewport=show_viewport)
            elif os.name == "nt":
                self.__windows_start_process__(binary_path, world_key, verbose=verbose)
            else:
                raise HolodeckException("Unknown platform: " + os.name)

        # Initialize Client
        self._client = HolodeckClient(self._uuid)
        self._command_center = CommandCenter(self._client)
        self._client.command_center = self._command_center
        self._reset_ptr = self._client.malloc("RESET", [1], np.bool)
        self._reset_ptr[0] = False

        # Set up agents already in the world
        self.agents = dict()
        self._state_dict = dict()
        self._agent = None

        # Spawn agents not yet in the world.
        # TODO implement this section for future build automation update

        # Set the default state function
        self.num_agents = len(self.agents)
        self._default_state_fn = self._get_single_state if self.num_agents == 1 else self._get_full_state

        self._client.acquire()

        # Flag indicates if the user has called .reset() before .tick() and .step()
        self._initial_reset = False
        self.reset()

    @property
    def action_space(self):
        """Gives the action space for the main agent.

        Returns:
            :class:`~holodeck.spaces.ActionSpace`: The action space for the main agent.
        """
        return self._agent.action_space

    def info(self):
        """Returns a string with specific information about the environment.
        This information includes which agents are in the environment and which sensors they have.

        Returns:
            :obj:`str`: Information in a string format.
        """
        result = list()
        result.append("Agents:\n")
        for agent in self.agents:
            result.append("\tName: ")
            result.append(agent.name)
            result.append("\n\tType: ")
            result.append(type(agent).__name__)
            result.append("\n\t")
            result.append("Sensors:\n")
            for _, sensor in agent.sensors.items():
                result.append("\t\t")
                result.append(sensor.name)
                result.append("\n")
        return "".join(result)

    def _load_scenario(self):
        """Loads the scenario defined in self._scenario_key.

        Instantiates all agents and sensors.

        If no scenario is defined, does nothing.
        """
        if self._scenario_key is not None:
            scenario = get_scenario(self._scenario_key)
        elif self._scenario_path is not None:
            scenario = load_scenario_file(self._scenario_path)
        else:
            return

        for agent in scenario['agents']:
            sensors = []
            for sensor in agent['sensors']:
                if 'sensor_type' not in sensor:
                    raise HolodeckException(
                        "Sensor for agent {} is missing required key 'sensor_type'".format(agent['agent_name']))

                # Default values for a sensor
                sensor_config = {
                    'location': [0, 0, 0],
                    'rotation': [0, 0, 0],
                    'socket': "",
                    'configuration': {},
                    'sensor_name': sensor['sensor_type']
                }
                # Overwrite the default values with what is defined in the scenario config
                sensor_config.update(sensor)

                sensors.append(SensorDefinition(agent['agent_name'],
                                                sensor_config['sensor_name'],
                                                sensor_config['sensor_type'],
                                                socket=sensor_config['socket'],
                                                location=sensor_config['location'],
                                                rotation=sensor_config['rotation'],
                                                config=sensor_config['configuration']))
                
            agent_def = AgentDefinition(agent['agent_name'], agent['agent_type'], starting_loc=agent["location"], sensors=sensors)
            is_main_agent = False
            if "main_agent" in scenario:
                is_main_agent = scenario["main_agent"] == agent["agent_name"]
            self.add_agent(agent_def, is_main_agent)
            self.agents[agent['agent_name']].set_control_scheme(agent['control_scheme'])
            self._spawned_agent_defs.append(agent_def)

    def reset(self):
        """Resets the environment, and returns the state.
        If it is a single agent environment, it returns that state for that agent. Otherwise, it returns a dict from
        agent name to state.

        Returns (tuple or dict):
            For single agent environment, returns the same as `step`.

            For multi-agent environment, returns the same as `tick`.
        """
        # Reset level
        self._initial_reset = True
        self._reset_ptr[0] = True
        self.tick()  # Must tick once to send reset before sending spawning commands
        self.tick()  # Bad fix to potential race condition. See issue https://github.com/BYU-PCCL/holodeck/issues/224
        self.tick()
        # Clear command queue
        if self._command_center.queue_size > 0:
            print("Warning: Reset called before all commands could be sent. Discarding",
                  self._command_center.queue_size, "commands.")
        self._command_center.clear()

        # Load agents
        self._spawned_agent_defs = []
        self.agents = dict()
        self._state_dict = dict()
        for agent_def in self._initial_agent_defs:
            self.add_agent(agent_def)

        self._load_scenario()

        self.num_agents = len(self.agents)
        self._default_state_fn = self._get_single_state if self.num_agents == 1 else self._get_full_state

        for _ in range(self._pre_start_steps + 1):
            self.tick()
        
        for agent_def in self._spawned_agent_defs:
            self.teleport(agent_def.name, agent_def.starting_loc, [0.0, 0.0, 0.0])

        return self._default_state_fn()

    def step(self, action):
        """Supplies an action to the main agent and tells the environment to tick once.
        Primary mode of interaction for single agent environments.

        Args:
            action (:obj:`np.ndarray`): An action for the main agent to carry out on the next tick.

        Returns:
            (:obj:`dict`, :obj:`float`, :obj:`bool`, info): A 4tuple:
                - State: Dictionary from sensor enum (see :class:`~holodeck.sensors.HolodeckSensor`) to :obj:`np.ndarray`.
                - Reward (:obj:`float`): Reward returned by the environment.
                - Terminal: The bool terminal signal returned by the environment.
                - Info: Any additional info, depending on the world. Defaults to None.
        """
        if not self._initial_reset:
            raise HolodeckException("You must call .reset() before .step()")

        if self._agent is not None:
            self._agent.act(action)

        self._command_center.handle_buffer()
        self._client.release()
        self._client.acquire()

        reward, terminal = self._get_reward_terminal()
        return self._default_state_fn(), reward, terminal, None

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

        self._command_center.handle_buffer()

        self._client.release()
        self._client.acquire()

        return self._default_state_fn()

    def teleport(self, agent_name, location=None, rotation=None):
        """Teleports the target agent to any given location, and applies a specific rotation.

        Args:
            agent_name (:obj:`str`): The name of the agent to teleport.
            location (:obj:`np.ndarray` or :obj:`list`): XYZ coordinates (in meters) for the agent to be teleported to.
                If no location is given, it isn't teleported, but may still be rotated. Defaults to None.
            rotation (:obj:`np.ndarray` or :obj:`list`): A new rotation target for the agent.
                If no rotation is given, it isn't rotated, but may still be teleported. Defaults to None.
        """
        self.agents[agent_name].teleport(location, rotation)

    def set_state(self, agent_name, location, rotation, velocity, angular_velocity):
        """Sets a new state for any agent given a location, rotation and linear and angular velocity. Will sweep and be
        blocked by objects in it's way however

        Args:
            agent_name (:obj:`str`): The name of the agent to teleport.
            location (:obj:`np.ndarray` or :obj:`list`): XYZ coordinates (in meters) for the agent to be teleported to.
            rotation (:obj:`np.ndarray` or :obj:`list`): A new rotation target for the agent.
            velocity (:obj:`np.ndarray` or :obj:`list`): A new velocity for the agent.
            angular velocity (:obj:`np.ndarray` or :obj:`list`): A new angular velocity for the agent.
        """
        self.agents[agent_name].set_state(location, rotation, velocity, angular_velocity)

    def act(self, agent_name, action):
        """Supplies an action to a particular agent, but doesn't tick the environment.
        Primary mode of interaction for multi-agent environments. After all agent commands are supplied,
        they can be applied with a call to `tick`.

        Args:
            agent_name (:obj:`str`): The name of the agent to supply an action for.
            action (:obj:`np.ndarray` or :obj:`list`): The action to apply to the agent. This action will be applied every
                time `tick` is called, until a new action is supplied with another call to act.
        """
        self.agents[agent_name].act(action)

    def tick(self):
        """Ticks the environment once. Normally used for multi-agent environments.

        Returns:
            :obj:`dict`: A dictionary from agent name to its full state. The full state is another dictionary
                from :obj:`holodeck.sensors.Sensors` enum to np.ndarray, containing the sensors information
                for each sensor. The sensors always include the reward and terminal sensors.
        """
        if not self._initial_reset:
            raise HolodeckException("You must call .reset() before .tick()")

        self._command_center.handle_buffer()

        self._client.release()
        self._client.acquire()
        return self._get_full_state()

    def _enqueue_command(self, command_to_send):
        self._command_center.enqueue_command(command_to_send)

    def add_agent(self, agent_def, is_main_agent=False):
        """Add an agent in the world. 
        
        It will be spawn when :meth:`tick` or :meth:`step` is called next.

        The agent won't be able to be used until the next frame.

        Args:
            agent_def (:class:`~holodeck.agents.AgentDefinition`): The definition of the agent to spawn.
        """
        if agent_def.name in self.agents:
            raise Exception("Error. Duplicate agent name. ")
        else:
            self.agents[agent_def.name] = AgentFactory.build_agent(self._client, agent_def)
            self._state_dict[agent_def.name] = self.agents[agent_def.name].agent_state_dict

            if not agent_def.existing:
                command_to_send = SpawnAgentCommand(agent_def.starting_loc, agent_def.name, agent_def.type.agent_type)
                self._client.command_center.enqueue_command(command_to_send)
            self.agents[agent_def.name].add_sensors(agent_def.sensors)
            if is_main_agent:
                self._agent = self.agents[agent_def.name]

    def set_ticks_per_capture(self, agent_name, ticks_per_capture):
        """Queues a rgb camera rate command. It will be applied when :meth:`tick` or :meth:`step` is called next.
        The specified agent's rgb camera will capture images every specified number of ticks.
        The sensor's image will remain unchanged between captures.
        This method must be called after every call to env.reset.

        Args:
            agent_name (:obj:`str`): The name of the agent whose rgb camera should be modified.
            ticks_per_capture (:obj:`int`): The amount of ticks to wait between camera captures.
        """
        if not isinstance(ticks_per_capture, int) or ticks_per_capture < 1:
            print("Ticks per capture value " + str(ticks_per_capture) + " invalid")
        elif agent_name not in self.agents:
            print("No such agent %s" % agent_name)
        else:
            self.agents[agent_name].set_ticks_per_capture(ticks_per_capture)
            command_to_send = RGBCameraRateCommand(agent_name, ticks_per_capture)
            self._enqueue_command(command_to_send)

    def draw_line(self, start, end, color=None, thickness=10.0):
        """Draws a debug line in the world

        Args:
            start (:obj:`list`): The start location of the line, ``[x, y, z]``
            end (:obj:`list`): The end location of the line, ``[x, y, z]``
            color (:obj:`list``): RGB values for the color, ``[r, g, b]``
            thickness (:obj:`float`): thickness of the line
        """
        color = [255, 0, 0] if color is None else color
        command_to_send = DebugDrawCommand(0, start, end, color, thickness)
        self._enqueue_command(command_to_send)

    def draw_arrow(self, start, end, color=None, thickness=10.0):
        """Draws a debug arrow in the world

        Args:
            start (:obj:`list`): The start location of the arrow, ``[x, y, z]``
            end (:obj:`list`): The end location of the arrow, ``[x, y, z]``
            color (:obj:`list`): RGB values for the color, ``[x, y, z]``
            thickness (:obj:`float`): thickness of the arrow
        """
        color = [255, 0, 0] if color is None else color
        command_to_send = DebugDrawCommand(1, start, end, color, thickness)
        self._enqueue_command(command_to_send)

    def draw_box(self, center, extent, color=None, thickness=10.0):
        """Draws a debug box in the world

        Args:
            center (:obj:`list`): The start location of the box, ``[x, y, z]``
            extent (:obj:`list`): The extent of the box, ``[x, y, z]``
            color (:obj:`list`): RGB values for the color, ``[x, y, z]``
            thickness (:obj:`float`): thickness of the lines
        """
        color = [255, 0, 0] if color is None else color
        command_to_send = DebugDrawCommand(2, center, extent, color, thickness)
        self._enqueue_command(command_to_send)

    def draw_point(self, loc, color=None, thickness=10.0):
        """Draws a debug point in the world

        Args:
            loc (:obj:`list`): The location of the point, ``[x, y, z]``
            color (:obj:`list`): RGB values for the color, ``[x, y, z]``
            thickness (:obj:`float`): thickness of the point, ``[x, y, z]``
        """
        color = [255, 0, 0] if color is None else color
        command_to_send = DebugDrawCommand(3, loc, [0, 0, 0], color, thickness)
        self._enqueue_command(command_to_send)

    def set_fog_density(self, density):
        """Change the fog density.

        The change will occur when :meth:`tick` or :meth:`step` is called next.

        By the next tick, the exponential height fog in the world will have the new density. If there is no fog in the
        world, it will be created with the given density.

        Args:
            density (:obj:`float`): The new density value, between 0 and 1. The command will not be sent if the given
                density is invalid.
        """
        if density < 0 or density > 1:
            raise HolodeckException("Fog density should be between 0 and 1")

        self.send_world_command("SetFogDensity", num_params=[density])

    def set_day_time(self, hour):
        """Change the time of day.

        Daytime will change when :meth:`tick` or :meth:`step` is called next.

        By the next tick, the lighting and the skysphere will be updated with the new hour.

        If there is no skysphere, skylight, or directional source light in the world, this command will fail silently.

        Args:
            hour (:obj:`int`): The hour in 24-hour format, between 0 and 23 inclusive.
        """
        self.send_world_command("SetHour", num_params=[hour % 24])

    def start_day_cycle(self, day_length):
        """Start the day cycle.

        The cycle will start when :meth:`tick` or :meth:`step` is called next.

        The sky sphere will then update each tick with an updated sun angle as it moves about the sky. The length of a
        day will be roughly equivalent to the number of minutes given.

        If there is no skysphere, skylight, or directional source light in the world, this command will fail silently.

        Args:
            day_length (:obj:`int`): The number of minutes each day will be.
        """
        if day_length <= 0:
            raise HolodeckException("The given day length should be between above 0!")

        self.send_world_command("SetDayCycle", num_params=[1, day_length])

    def stop_day_cycle(self):
        """Stop the day cycle.

        The cycle will stop when :meth:`tick` or :meth:`step` is called next.

        By the next tick, day cycle will stop where it is.

        If there is no skysphere, skylight, or directional source light in the world, this command will fail silently.
        """
        self.send_world_command("SetDayCycle", num_params=[0, -1])

    def set_weather(self, weather_type):
        """Set the world's weather.

        The new weather will be applied when :meth:`tick` or :meth:`step` is called next.

        By the next tick, the lighting, skysphere, fog, and relevant particle systems will be updated and/or spawned
        to the given weather.

        If there is no skysphere, skylight, or directional source light in the world, this command will fail silently.

        ..note::
            Because this command can affect the fog density, any changes made by a change_fog_density command before
            a set_weather command called will be undone. It is recommended to call change_fog_density after calling set
            weather if you wish to apply your specific changes.

        In all downloadable worlds, the weather is clear by default.

        If the given type string is not available, the command will not be sent.

        Args:
            weather_type (:obj:`str`): The type of weather, which can be ``rain`` or ``cloudy``.

        """
        if not weather_type.lower() in ["rain", "cloudy"]:
            raise HolodeckException("Invalid weather type " + weather_type)

        self.send_world_command("SetWeather", string_params=[weather_type])

    def teleport_camera(self, location, rotation):
        """Teleport the camera to the given location

        By the next tick, the camera's location and rotation will be updated

        Args:
            location (:obj:`list` of size 3): The location to give the camera
            rotation (:obj:`list` of size 3): The rotation to give the camera

        """
        self._enqueue_command(TeleportCameraCommand(location, rotation))

    def should_render_viewport(self, render_viewport):
        """Controls whether the viewport is rendered or not

        Args:
            render_viewport (:obj:`boolean`): If the viewport should be rendered
        """
        self._enqueue_command(RenderViewportCommand(render_viewport))

    def set_render_quality(self, render_quality):
        """Adjusts the rendering quality of Holodeck.
        Args:
            render_quality (:obj:`int`): An integer between 0 = Low Quality and 3 = Epic quality.
        """
        self._enqueue_command(RenderQualityCommand(render_quality))

    def set_control_scheme(self, agent_name, control_scheme):
        """Set the control scheme for a specific agent.

        Args:
            agent_name (:obj:`str`): The name of the agent to set the control scheme for.
            control_scheme (:obj:`int`): A control scheme value (see :class:`~holodeck.agents.ControlSchemes`)
        """
        if agent_name not in self.agents:
            print("No such agent %s" % agent_name)
        else:
            self.agents[agent_name].set_control_scheme(control_scheme)

    def set_sensor_enabled(self, agent_name, sensor_name, enabled):
        """Enable or disable an agent's sensor.

        Args:
            agent_name (:obj:`str`): The name of the agent whose sensor will be switched
            sensor_name (:obj:`str`): The name of the sensor to be switched
            enabled (:obj:`bool`): Boolean representing whether to enable or disable the sensor
        """
        if agent_name not in self._sensor_map:
            print("No such agent %s" % agent_name)
        else:
            command_to_send = SetSensorEnabledCommand(agent_name, sensor_name, enabled)
            self._enqueue_command(command_to_send)

    def send_world_command(self, name, num_params=[], string_params=[]):
        """Send a custom command.

        A custom command sends an abitrary command that may only exist in a specific world or package. It is given a
        name and any amount of string and number parameters that allow it to alter the state of the world.

        Args:
            name (:obj:`str`): The name of the command, ex "OpenDoor"
            num_params (obj:`list` of :obj:`int`): List of arbitrary number parameters
            string_params (obj:`list` of :obj:`int`): List of arbitrary string parameters
        """
        command_to_send = CustomCommand(name, num_params, string_params)
        self._enqueue_command(command_to_send)

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
                                                '-ResY=' + str(self._window_height), '--HolodeckUUID=' + self._uuid,
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
        loading_semaphore = win32event.CreateSemaphore(None, 0, 1, 'Global\\HOLODECK_LOADING_SEM' + self._uuid)
        self._world_process = subprocess.Popen([binary_path, task_key, '-HolodeckOn', '-LOG=HolodeckLog.txt',
                                                '-ResX=' + str(self._window_width), '-ResY=' + str(self._window_height),
                                                '--HolodeckUUID=' + self._uuid,
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

        if self._agent is not None:
            return self._create_copy(self._state_dict[self._agent.name]) if self._copy_state \
                else self._state_dict[self._agent.name]
        else:
            return self._get_full_state()

    def _get_full_state(self):
        return self._create_copy(self._state_dict) if self._copy_state else self._state_dict

    def _get_reward_terminal(self):
        reward = None
        terminal = None
        if self._agent is not None:
            for sensor in self._state_dict[self._agent.name]:
                if "Task" in sensor:
                    reward = self._state_dict[self._agent.name][sensor][0]
                    terminal = self._state_dict[self._agent.name][sensor][1] == 1
        return reward, terminal

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