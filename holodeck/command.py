"""This module contains the classes used for formatting and sending commands to the Holodeck backend.

To create a new command to send to the Holodeck backend, simply subclass from command.
"""

from holodeck.agents import *


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


class SpawnAgentCommand(Command):
    """Holds the information to be sent to Holodeck that is needed for spawning an agent.

    Args:
        location (list of float): The place to spawn the agent in XYZ coordinates (meters).
        name (str): The name of the agent.
        agent_type (str): The type of agent to spawn (UAVAgent, NavAgent, ...)
    """
    __type_keys = {
        DiscreteSphereAgent: "SphereRobot",
        UavAgent: "UAV",
        NavAgent: "NavAgent",
        AndroidAgent: "Android"
    }

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
            agent_type (str): The type of agent to spawn.
        """
        type_str = SpawnAgentCommand.__type_keys[agent_type]
        self.add_string_parameters(type_str)


class ChangeFogDensityCommand(Command):
    """A command for changing the fog density in the world.

    Args:
        density (float): A value between 0 and 1.
    """
    def __init__(self, density):
        super(ChangeFogDensityCommand, self).__init__()
        self._command_type = "ChangeFogDensity"
        self.set_density(density)

    def set_density(self, density):
        """Set the density for the fog.

        Args:
            density (float): A value between 0 and 1.
        """
        if density < 0 or density > 1:
            print("Fog density should be between 0 and 1")
            return
        self.add_number_parameters(density)


class DayTimeCommand(Command):
    """A command to change the time of day.

    Args:
        hour (int): The hour in military time, should be something between 0-23
    """
    def __init__(self, hour):
        super(DayTimeCommand, self).__init__()
        self._command_type = "DayTime"
        self.set_hour(hour)

    def set_hour(self, hour):
        """Set the hour.

        Args:
            hour (int): The hour in military time, should be something between 0-23
        """
        if hour < 0 or hour > 23:
            print("The hour should be in military time; between 0 and 23")
            return
        self.add_number_parameters(hour)


class DayCycleCommand(Command):
    """A command for turning on and off the day/night cycle.

    Args:
        start (bool): Whether to start or stop the day night cycle
    """
    def __init__(self, start):
        super(DayCycleCommand, self).__init__()
        self._command_type = "DayCycle"
        self.set_command(start)

    def set_day_length(self, day_length):
        """Set the day length in minutes.
        Positional Arguments:
        hour -- The day length in minutes. Cannot be at or below 0
        """
        if day_length <= 0:
            print("The day length should not be equal to or below 0")
            return
        self.add_number_parameters(day_length)

    def set_command(self, start):
        """Start or stop the command
        Positional Arguments:
        start -- Bool for whether to start(true) the day cycle or stop(false).
        """
        if start:
            self.add_string_parameters("start")
        else:
            self.add_string_parameters("stop")


class SetWeatherCommand(Command):
    """A command to set the weather type.

    Args:
        weather_type (str): The weather type. Can be "rain" or "cloudy".
    """
    _types = [
        "rain",
        "cloudy"
    ]

    def __init__(self, weather_type):
        Command.__init__(self)
        self._command_type = "SetWeather"
        self.set_type(weather_type)

    def set_type(self, weather_type):
        """Set the weather type.

        Args:
            weather_type (str): The weather type.
        """
        weather_type.lower()
        exists = self.has_type(weather_type)
        if exists:
            self.add_string_parameters(weather_type)

    @staticmethod
    def has_type(weather_type):
        """Checks the validity of the type. Returns true if it exists in the type array

        Args:
            weather_type (str): The weather type, should be one of the above array
        """
        return weather_type in SetWeatherCommand._types


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
