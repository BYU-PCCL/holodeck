"""This module contains the classes used for formatting and sending commands to the Holodeck backend.

To create a new command to send to the Holodeck backend, simply subclass from command.
"""


import numpy as np


class CommandsGroup(object):
    """Represents a list of commands
    
    Can convert list of commands to json.
    
    """

    def __init__(self):
        self._commands = []

    def add_command(self, command):
        """Adds a command to the list

        Args:
            command (:class:`Command`): A command to add."""
        self._commands.append(command)

    def to_json(self):
        """
        Returns:
             :obj:`str`: Json for commands array object and all of the commands inside the array.
             
        """
        commands = ",".join(map(lambda x: x.to_json(), self._commands))
        return "{\"commands\": [" + commands + "]}"

    def clear(self):
        """Clear the list of commands.
        
        """
        self._commands.clear()

    @property
    def size(self):
        """
        Returns:
            int: Size of commands group"""
        return len(self._commands)


class Command(object):
    """Base class for Command objects.
    
    Commands are used for IPC between the holodeck python bindings and holodeck
    binaries.

    Derived classes must set the ``_command_type``.

    The order in which :meth:`add_number_parameters` and :meth:`add_number_parameters` are called
    is significant, they are added to an ordered list. Ensure that you are adding parameters in
    the order the client expects them. 
    
    """

    def __init__(self):
        self._parameters = []
        self._command_type = ""

    def set_command_type(self, command_type):
        """Set the type of the command.

        Args:
            command_type (:obj:`str`): This is the name of the command that it will be set to.

        """
        self._command_type = command_type

    def add_number_parameters(self, number):
        """Add given number parameters to the internal list.

        Args:
            number (:obj:`list` of :obj:`int`/:obj:`float`, or singular :obj:`int`/:obj:`float`): 
                A number or list of numbers to add to the parameters.

        """
        if isinstance(number, list):
            for x in number:
                self.add_number_parameters(x)
            return
        self._parameters.append("{ \"value\": " + str(number) + " }")

    def add_string_parameters(self, string):
        """Add given string parameters to the internal list.

        Args:
            string (:obj:`list` of :obj:`str` or :obj:`str`): 
                A string or list of strings to add to the parameters.

        """
        if isinstance(string, list):
            for x in string:
                self.add_string_parameters(x)
            return
        self._parameters.append("{ \"value\": \"" + string + "\" }")

    def to_json(self):
        """Converts to json.

        Returns:
            :obj:`str`: This object as a json string.
        
        """
        to_return = "{ \"type\": \"" + self._command_type + "\", \"params\": [" + ",".join(self._parameters) + "]}"
        return to_return


class CommandCenter(object):
    """Manages pending commands to send to the client (the engine).

    Args:
        client (:class:`~holodeck.holodeckclient.HolodeckClient`): Client to send commands to

    """
    def __init__(self, client):
        self._client = client

        # Set up command buffer
        self._command_bool_ptr = self._client.malloc("command_bool", [1], np.bool)
        self.max_buffer = 1048576  # This is the size of the command buffer that Holodeck expects/will read.
        self._command_buffer_ptr = self._client.malloc("command_buffer", [self.max_buffer], np.byte)
        self._commands = CommandsGroup()
        self._should_write_to_command_buffer = False

    def clear(self):
        """Clears pending commands

        """
        self._commands.clear()

    def handle_buffer(self):
        """Writes the list of commands into the command buffer, if needed.
        
        Checks if we should write to the command buffer, writes all of the queued commands to the buffer, and then
        clears the contents of the self._commands list
        
        """
        if self._should_write_to_command_buffer:
            self._write_to_command_buffer(self._commands.to_json())
            self._should_write_to_command_buffer = False
            self._commands.clear()

    def enqueue_command(self, command_to_send):
        """Adds command to outgoing queue.

        Args:
            command_to_send (:class:`Command`): Command to add to queue

        """
        self._should_write_to_command_buffer = True
        self._commands.add_command(command_to_send)

    def _write_to_command_buffer(self, to_write):
        """Write input to the command buffer. 
        
        Reformat input string to the correct format.

        Args:
            to_write (:class:`str`): The string to write to the command buffer.

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
        return self._commands.size


class SpawnAgentCommand(Command):
    """Spawn an agent in the world.

    Args:
        location (:obj:`list` of :obj:`float`): The place to spawn the agent in XYZ coordinates (meters).
        name (:obj:`str`): The name of the agent.
        agent_type (:obj:`str` or type): The type of agent to spawn (UAVAgent, NavAgent, ...)

    """

    def __init__(self, location, name, agent_type):
        super(SpawnAgentCommand, self).__init__()
        self._command_type = "SpawnAgent"
        self.set_location(location)
        self.set_type(agent_type)
        self.set_name(name)

    def set_location(self, location):
        """Set where agent will be spawned.

        Args:
            location (:obj:`list` of :obj:`float`): [X,Y,Z] coordinate of where to spawn the agent.

        """
        if len(location) != 3:
            print("Invalid location given to spawn agent command")
            return
        self.add_number_parameters(location)

    def set_name(self, name):
        """Set agents name

        Args:
            name (:obj:`str`): The name to set the agent to.

        """
        self.add_string_parameters(name)

    def set_type(self, agent_type):
        """Set the type of agent.

        Args:
            agent_type (:obj:`str` or :obj:`type`): The type of agent to spawn.

        """
        if not isinstance(agent_type, str):
            agent_type = agent_type.agent_type  # Get str from type
        self.add_string_parameters(agent_type)


class DebugDrawCommand(Command):
    """Draw debug geometry in the world.

    Args:
        draw_type (:obj:`int`) : The type of object to draw, ``0``: line, ``1``: arrow, ``2``: box, ``3``: point
        start (:obj:`list` of 3 :obj:`floats`): The start location of the object
        end (:obj:`list` of 3 :obj:`floats`): The end location of the object (not used for point, and extent for box)
        color (:obj:`list` of 3 :obj:`floats`): [R,G,B] values for the color
        thickness (:obj:`float`): thickness of the line/object

    """
    def __init__(self, draw_type, start, end, color, thickness):
        super(DebugDrawCommand, self).__init__()
        self._command_type = "DebugDraw"

        self.add_number_parameters(draw_type)
        self.add_number_parameters(start)
        self.add_number_parameters(end)
        self.add_number_parameters(color)
        self.add_number_parameters(thickness)


class TeleportCameraCommand(Command):
    """Move the viewport camera (agent follower)

    Args:
        location (:obj:`list` of size 3): The location to give the camera
        rotation (:obj:`list` of size 3): The rotation to give the camera

    """
    def __init__(self, location, rotation):
        Command.__init__(self)
        self._command_type = "TeleportCamera"
        self.add_number_parameters(location)
        self.add_number_parameters(rotation)


class SetSensorEnabledCommand(Command):
    """Enable or disable a sensor on an agent

    Args:
        agent (:obj:`str`): Name of the agent to modify
        sensor (:obj:`str`): Name of the sensor to enable or disable
        enabled (:obj:`bool`): State to set sensor to

    """
    def __init__(self, agent, sensor, enabled):
        Command.__init__(self)
        self._command_type = "SetSensorEnabled"
        self.add_string_parameters(agent)
        self.add_string_parameters(sensor)
        self.add_number_parameters(1 if enabled else 0)


class AddSensorCommand(Command):
    def __init__(self, sensor_definition):
        """Add a sensor to an agent

        Args:
            sensor_definition (~holodeck.sensors.SensorDefinition): Sensor to add
        """

        Command.__init__(self)
        self._command_type = "AddSensor"
        self.add_string_parameters(sensor_definition.agent_name)
        self.add_string_parameters(sensor_definition.sensor_name)
        self.add_string_parameters(sensor_definition.type.sensor_type)
        self.add_string_parameters(sensor_definition.get_config_json_string())
        self.add_string_parameters(sensor_definition.socket)

        self.add_number_parameters(sensor_definition.location[0])
        self.add_number_parameters(sensor_definition.location[1])
        self.add_number_parameters(sensor_definition.location[2])

        self.add_number_parameters(sensor_definition.rotation[0])
        self.add_number_parameters(sensor_definition.rotation[1])
        self.add_number_parameters(sensor_definition.rotation[2])


class RemoveSensorCommand(Command):
    """Remove a sensor from an agent

    Args:
        agent (:obj:`str`): Name of agent to modify
        sensor (:obj:`str`): Name of the sensor to remove

    """
    def __init__(self, agent, sensor):
        Command.__init__(self)
        self._command_type = "RemoveSensor"
        self.add_string_parameters(agent)
        self.add_string_parameters(sensor)


class RenderViewportCommand(Command):
    """Enable or disable the viewport

    Args:
        render_viewport (:obj:`bool`): If viewport should be rendered

    """
    def __init__(self, render_viewport):
        Command.__init__(self)
        self.set_command_type("RenderViewport")
        self.add_number_parameters(int(bool(render_viewport)))


class RGBCameraRateCommand(Command):
    """Set the number of ticks between captures of the RGB camera.

    Args:
        agent_name (:obj:`str`): name of the agent to modify
        ticks_per_capture (:obj:`int`): number of ticks between captures

    """
    def __init__(self, agent_name, ticks_per_capture):
        Command.__init__(self)
        self._command_type = "RGBCameraRate"
        self.add_string_parameters(agent_name)
        self.add_number_parameters(ticks_per_capture)


class RenderQualityCommand(Command):
    """Adjust the rendering quality of Holodeck

    Args:
        render_quality (int): 0 = low, 1 = medium, 3 = high, 3 = epic

    """
    def __init__(self, render_quality):
        Command.__init__(self)
        self.set_command_type("AdjustRenderQuality")
        self.add_number_parameters(int(render_quality))


class CustomCommand(Command):
    """Send a custom command to the currently loaded world.

    Args:
        name (:obj:`str`): The name of the command, ex "OpenDoor"
        num_params (obj:`list` of :obj:`int`): List of arbitrary number parameters
        string_params (obj:`list` of :obj:`int`): List of arbitrary string parameters

    """
    def __init__(self, name, num_params=None, string_params=None):
        if num_params is None:
            num_params = []

        if string_params is None:
            string_params = []

        Command.__init__(self)
        self.set_command_type("CustomCommand")
        self.add_string_parameters(name)
        self.add_number_parameters(num_params)
        self.add_string_parameters(string_params)
