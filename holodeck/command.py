"""This module contains the classes used for formatting and sending commands to the Holodeck backend.

To create a new command to send to the Holodeck backend, simply subclass from command.
"""


import numpy as np


class CommandsGroup(object):
    """Holds Command objects in a list, and when requested packages everything in the correct json format."""

    def __init__(self):
        self._commands = []

    def add_command(self, command):
        """Adds a command to the list

        Args:
            command (Command): A command to add."""
        self._commands.append(command)

    def to_json(self):
        """
        Returns:
             str: Json for commands array object and all of the commands inside the array."""
        commands = ",".join(map(lambda x: x.to_json(), self._commands))
        return "{\"commands\": [" + commands + "]}"

    def clear(self):
        """Clear the list of commands."""
        self._commands.clear()

    @property
    def size(self):
        """
        Returns:
            int: Size of commands group"""
        return len(self._commands)


class Command(object):
    """Base class for Command objects. Commands are used for IPC between the holodeck python bindings and holodeck
    binaries. Can return itself in json format. You must set the command type."""
    def __init__(self):
        self._parameters = []
        self._command_type = ""

    def set_command_type(self, command_type):
        """Set the type of the command.

        Args:
            command_type (str): This is the name of the command that it will be set to.
        """
        self._command_type = command_type

    def add_number_parameters(self, number):
        """Add given number parameters to the internal list.

        Args:
            number (list of int or list of float): A number or list of numbers to add to the parameters.
        """
        if isinstance(number, list):
            for x in number:
                self.add_number_parameters(x)
            return
        self._parameters.append("{ \"value\": " + str(number) + " }")

    def add_string_parameters(self, string):
        """Add given string parameters to the internal list.

        Args:
            string (list of str or str): A string or list of strings to add to the parameters.
        """
        if isinstance(string, list):
            for x in string:
                self.add_string_parameters(x)
            return
        self._parameters.append("{ \"value\": \"" + string + "\" }")

    def to_json(self):
        """
        Returns:
            str: This object in json format."""
        to_return = "{ \"type\": \"" + self._command_type + "\", \"params\": [" + ",".join(self._parameters) + "]}"
        return to_return


class CommandCenter(object):

    def __init__(self, client):
        self._client = client

        # Set up command buffer
        self._command_bool_ptr = self._client.malloc("command_bool", [1], np.bool)
        self.max_buffer = 1048576  # This is the size of the command buffer that Holodeck expects/will read.
        self._command_buffer_ptr = self._client.malloc("command_buffer", [self.max_buffer], np.byte)
        self._commands = CommandsGroup()
        self._should_write_to_command_buffer = False

    def clear(self):
        self._commands.clear()

    def handle_buffer(self):
        """Checks if we should write to the command buffer, writes all of the queued commands to the buffer, and then
        clears the contents of the self._commands list"""
        if self._should_write_to_command_buffer:
            self._write_to_command_buffer(self._commands.to_json())
            self._should_write_to_command_buffer = False
            self._commands.clear()

    def enqueue_command(self, command_to_send):
        self._should_write_to_command_buffer = True
        self._commands.add_command(command_to_send)

    def _write_to_command_buffer(self, to_write):
        """Write input to the command buffer.  Reformat input string to the correct format.

        Args:
            to_write (str): The string to write to the command buffer.
        """

        np.copyto(self._command_bool_ptr, True)
        to_write += '0'  # The gason JSON parser in holodeck expects a 0 at the end of the file.
        input_bytes = str.encode(to_write)
        if len(input_bytes) > self.max_buffer:
            raise Exception("Error: Command length exceeds buffer size")
        for index, val in enumerate(input_bytes):
            self._command_buffer_ptr[index] = val

    @property
    def queue_size(self):
        """
        Returns:
            int: Size of commands queue"""
        return self._commands


class SpawnAgentCommand(Command):
    """Holds the information to be sent to Holodeck that is needed for spawning an agent.

    Args:
        location (list of float): The place to spawn the agent in XYZ coordinates (meters).
        name (str): The name of the agent.
        agent_type (str or type): The type of agent to spawn (UAVAgent, NavAgent, ...)
    """

    def __init__(self, location, name, agent_type):
        super(SpawnAgentCommand, self).__init__()
        self._command_type = "SpawnAgent"
        self.set_location(location)
        self.set_type(agent_type)
        self.set_name(name)

    def set_location(self, location):
        """Set the location to spawn the agent at.

        Args:
            location (list of float): XYZ coordinate of where to spawn the agent.
        """
        if len(location) != 3:
            print("Invalid location given to spawn agent command")
            return
        self.add_number_parameters(location)

    def set_name(self, name):
        """Set the name to give the agent.

        Args:
            name (str): The name to set the agent to.
        """
        self.add_string_parameters(name)

    def set_type(self, agent_type):
        """Set the type of agent to spawn in Holodeck. Currently accepted agents are: DiscreteSphereAgent, UAVAgent,
        and AndroidAgent.

        Args:
            agent_type (str or type): The type of agent to spawn.
        """
        if not isinstance(agent_type, str):
            agent_type = agent_type.agent_type  # Get str from type
        self.add_string_parameters(agent_type)


class DebugDrawCommand(Command):

    def __init__(self, draw_type, start, end, color, thickness):
        """Draws a debug lines, points, etc... in the world

        Args:
            draw_type (int) : The type of object to draw, 0: line, 1: arrow, 2: box, 3: point
            start (list of 3 floats): The start location of the object
            end (list of 3 floats): The end location of the object (not used for point, and extent for box)
            color (list of 3 floats): RGB values for the color
            thickness (float): thickness of the line/object
        """

        super(DebugDrawCommand, self).__init__()
        self._command_type = "DebugDraw"

        self.add_number_parameters(draw_type)
        self.add_number_parameters(start)
        self.add_number_parameters(end)
        self.add_number_parameters(color)
        self.add_number_parameters(thickness)


class TeleportCameraCommand(Command):
    def __init__(self, location, rotation):
        """Sets the command type to TeleportCamera and initialized this object.
        :param location: The location to give the camera
        :param rotation: The rotation to give the camera
        """
        Command.__init__(self)
        self._command_type = "TeleportCamera"
        self.set_location(location)
        self.set_rotation(rotation)

    def set_location(self, location):
        """Set the location.
        Positional Arguments:
        location: A three dimensional array representing location in x,y,z
        """
        self.add_number_parameters(location)

    def set_rotation(self, rotation):
        """Set the rotation.
        Positional Arguments:
        rotation: A three dimensional array representing rotation in x,y,z
        """
        self.add_number_parameters(rotation)


class SetSensorEnabledCommand(Command):
    def __init__(self, agent, sensor, enabled):
        """Sets the command type to SetSensorEnabled and initializes the object.
        :param agent: Name of the agent whose sensor will be switched
        :param sensor: Name of the sensor to be switched
        :param enabled: Boolean representing the sensor state
        """
        Command.__init__(self)
        self._command_type = "SetSensorEnabled"
        self.set_agent(agent)
        self.set_sensor(sensor)
        self.set_enabled(enabled)

    def set_agent(self, agent):
        """Set the agent name.
        Positional Arguments:
        agent: String representing the name of the agent whose sensor will be switched
        """
        self.add_string_parameters(agent)

    def set_sensor(self, sensor):
        """Set the sensor name.
        Positional Arguments:
        sensor: String representing the name of the sensor to be switched
        """
        self.add_string_parameters(sensor)

    def set_enabled(self, enabled):
        """Set sensor state.
        Positional Arguments:
        enabled: Boolean representing the new sensor state
        """
        self.add_number_parameters(1 if enabled else 0)


class AddSensorCommand(Command):
    def __init__(self, sensor_definition):
        """Sets the command type to AddSensor and initializes the object.
        :param sensor_definition: Definition for sensor to add.
        """
        Command.__init__(self)
        self._command_type = "AddSensor"
        self.set_agent(sensor_definition.agent_name)
        self.set_sensor(sensor_definition.sensor_name)
        self.set_type(sensor_definition.type.sensor_type)
        self.set_params(sensor_definition.params)
        self.set_socket(sensor_definition.socket)
        self.set_location(sensor_definition.location)
        self.set_rotation(sensor_definition.rotation)

    def set_agent(self, agent):
        """Set the agent name.
        Positional Arguments:
        agent: String representing the name of the agent to add sensor
        """
        self.add_string_parameters(agent)

    def set_sensor(self, sensor):
        """Set the sensor name.
        Positional Arguments:
        sensor: String representing the name of the sensor
        """
        self.add_string_parameters(sensor)

    def set_type(self, sensor_type):
        """Set the sensor type.
        Positional Arguments:
        sensor_type: String representing the class of the sensor
        """
        self.add_string_parameters(sensor_type)

    def set_params(self, sensor_params):
        """Set the sensor params.
        Positional Arguments:
        sensor_params: Json string of sensor parameters
        """
        self.add_string_parameters(sensor_params)

    def set_socket(self, sensor_socket):
        """Set the sensor socket.
        Positional Arguments:
        sensor_socket: String representing name of the socket where sensor will be attached
        """
        self.add_string_parameters(sensor_socket)

    def set_location(self, sensor_location):
        """Set the sensor location.
        Positional Arguments:
        sensor_location: Tuple of floats representing the location of the sensor
        """
        self.add_number_parameters(sensor_location[0])
        self.add_number_parameters(sensor_location[1])
        self.add_number_parameters(sensor_location[2])

    def set_rotation(self, sensor_rotation):
        """Set the sensor rotation.
        Positional Arguments:
        sensor_rotation: Tuple of floats representing the rotation of the sensor
        """
        self.add_number_parameters(sensor_rotation[0])
        self.add_number_parameters(sensor_rotation[1])
        self.add_number_parameters(sensor_rotation[2])


class RemoveSensorCommand(Command):
    def __init__(self, agent, sensor):
        """Sets the command type to RemoveSensor and initializes the object.
        :param agent: Name of the agent whose sensor will be removed
        :param sensor: Name of the sensor to be removed
        """
        Command.__init__(self)
        self._command_type = "RemoveSensor"
        self.set_agent(agent)
        self.set_sensor(sensor)

    def set_agent(self, agent):
        """Set the agent name.
        Positional Arguments:
        agent: String representing the name of the agent whose sensor will be removed
        """
        self.add_string_parameters(agent)

    def set_sensor(self, sensor):
        """Set the sensor name.
        Positional Arguments:
        sensor: String representing the name of the sensor to be removed
        """
        self.add_string_parameters(sensor)


class RenderViewportCommand(Command):
    def __init__(self, render_viewport):
        """
        :param render_viewport: Boolean if the viewport should be rendered or not
        """
        Command.__init__(self)
        self.set_command_type("RenderViewport")
        self.add_number_parameters(int(bool(render_viewport)))


class RGBCameraRateCommand(Command):
    def __init__(self, agent_name, ticks_per_capture):
        """Sets the command type to RGBCameraRate and initializes this object.
        :param agent_name: The name of the agent whose pixel camera rate should be modified
        :param ticks_per_capture: The number of ticks that should pass per capture of the pixel camera
        """
        Command.__init__(self)
        self._command_type = "RGBCameraRate"
        self.set_agent(agent_name)
        self.set_ticks_per_capture(ticks_per_capture)

    def set_ticks_per_capture(self, ticks_per_capture):
        """Set the ticks per capture.
        Positional Arguments:
        ticks_per_capture: An int representing the number of ticks per capture of the camera
        """
        self.add_number_parameters(ticks_per_capture)

    def set_agent(self, agent_name):
        """Set the agent.
        Positional Arguments:
        agent_name: A string representing the name of the agent
        """
        self.add_string_parameters(agent_name)


class RenderQualityCommand(Command):
    def __init__(self, render_quality):
        """Adjusts the rendering quality of Holodeck.
        :param render_quality: An integer between 0 and 3.
                                    0 = low
                                    1 = medium
                                    2 = high
                                    3 = epic
        """
        Command.__init__(self)
        self.set_command_type("AdjustRenderQuality")
        self.add_number_parameters(int(render_quality))


class CustomCommand(Command):
    def __init__(self, name, num_params=[], string_params=[]):
        """Send a custom command that is specific to the world in use.
        :param name: The name of the command, ex "OpenDoor"
        :param num_params: List of arbitrary number parameters
        :param string_params: List of arbitrary string parameters
        """
        Command.__init__(self)
        self.set_command_type("CustomCommand")
        self.add_string_parameters(name)
        self.add_number_parameters(num_params)
        self.add_string_parameters(string_params)
