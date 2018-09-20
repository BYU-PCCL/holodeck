"""This module contains the classes used for formatting and sending commands to the Holodeck backend.

To create a new command to send to the Holodeck backend, simply subclass from command.
"""

from holodeck.agents import *


class CommandsGroup(object):
    """Holds Command objects in a list, and when requested packages everything in the correct json format"""

    def __init__(self):
        self._commands = []

    def add_command(self, command):
        """Adds a command to the list"""
        self._commands.append(command)

    def to_json(self):
        """Return a string of the commands array object and all of the commands inside the array"""
        commands = ",".join(map(lambda x: x.to_json(), self._commands))
        return "{\"commands\": [" + commands + "]}"

    def clear(self):
        """Clear the list of commands"""
        self._commands.clear()


class Command(object):
    """Base class for Command objects. Can return itself in json format. You must set the command type."""

    def __init__(self):
        self._parameters = []
        self._command_type = ""

    def set_command_type(self, command_type):
        """Set the type of the command.
        Positional Arguments:
        command_type -- This is the name of the command that it will be set to.
        """
        self._command_type = command_type

    def add_number_parameters(self, number):
        """Add given number parameters to the internal list.
        Positional Arguments:
        number -- A number or list of numbers to add to the parameters.
        """
        if isinstance(number, list):
            for x in number:
                self.add_number_parameters(x)
            return
        self._parameters.append("{ \"value\": " + str(number) + " }")

    def add_string_parameters(self, string):
        """Add given string parameters to the internal list.
        Positional Arguments:
        string -- A string or list of strings to add to the parameters.
        """
        if isinstance(string, list):
            for x in string:
                self.add_string_parameters(x)
            return
        self._parameters.append("{ \"value\": \"" + string + "\" }")

    def to_json(self):
        """Return this object in json format."""
        to_return = "{ \"type\": \"" + self._command_type + "\", \"params\": [" + ",".join(self._parameters) + "]}"
        return to_return


class SpawnAgentCommand(Command):
    """Holds the information to be sent to Holodeck that is needed for spawning an agent."""
    __type_keys = {
        DiscreteSphereAgent: "SphereRobot",
        UavAgent: "UAV",
        NavAgent: "NavAgent",
        AndroidAgent: "Android"
    }

    def __init__(self, location, name, agent_type):
        """Sets the command type to SpawnAgent and initialized this object.

        :param location: The place to spawn the agent in the world in XYZ
        :param name: The name to give the agent
        :param agent_type: The type of agent (UAVAgent, NavAgent, etc..)
        """
        Command.__init__(self)
        self._command_type = "SpawnAgent"
        self.set_location(location)
        self.set_type(agent_type)
        self.set_name(name)

    def set_location(self, location):
        """Set the location to spawn the agent at.
        Positional Arguments:
        location -- XYZ coordinate of where to spawn the agent.
        """
        if len(location) != 3:
            print("Invalid location given to spawn agent command")
            return
        self.add_number_parameters(location)

    def set_name(self, name):
        """Set the name to give the agent.
        Positional Arguments:
        name -- The name to set the agent to.
        """
        self.add_string_parameters(name)

    def set_type(self, agent_type):
        """Set the type of agent to spawn in Holodeck. Currently accepted agents are: DiscreteSphereAgent, UAVAgent,
        and AndroidAgent.
        Positional Arguments:
        agent_type -- The type of agent to spawn.
        """
        type_str = SpawnAgentCommand.__type_keys[agent_type]
        self.add_string_parameters(type_str)


class ChangeFogDensityCommand(Command):

    def __init__(self, density):
        """Sets the command type to ChangeFogDensity and initialized this object.

        :param density: The new density, should be something between 0-1
        """
        Command.__init__(self)
        self._command_type = "ChangeFogDensity"
        self.set_density(density)

    def set_density(self, density):
        """Set the density for the fog.
        Positional Arguments:
        density -- The new density, should be something between 0-1
        """
        if density < 0 or density > 1:
            print("Fog density should be between 0 and 1")
            return
        self.add_number_parameters(density)


class DayTimeCommand(Command):

    def __init__(self, hour):
        """Sets the command type to DayTime and initialized this object.

        :param hour: The hour in military time, should be something between 0-23
        """
        Command.__init__(self)
        self._command_type = "DayTime"
        self.set_hour(hour)

    def set_hour(self, hour):
        """Set the hour.
        Positional Arguments:
        hour -- The hour in military time, should be something between 0-23
        """
        if hour < 0 or hour > 23:
            print("The hour should be in military time; between 0 and 23")
            return
        self.add_number_parameters(hour)


class DayCycleCommand(Command):

    def __init__(self, start):
        """Sets the command type to DayCycle and initialized this object.

        :param start: bool representing whether to start or stop the day night cycle
        """
        Command.__init__(self)
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
    """ Avaiable weather types. """
    _types = [
        "rain",
        "cloudy"
    ]

    def __init__(self, weather_type):
        """Sets the command type to SetWeather and initialized this object.

        :param type: The weather type, should be one of the above array
        """
        Command.__init__(self)
        self._command_type = "SetWeather"
        self.set_type(weather_type)

    def set_type(self, weather_type):
        """Set the weather type.
        Positional Arguments:
        type: The weather type, should be one of the above array
        """
        weather_type.lower()
        exists = self.has_type(weather_type)
        if exists:
            self.add_string_parameters(weather_type)

    @staticmethod
    def has_type(weather_type):
        """Checks the validity of the type. Returns true if it exists in the type array
        Positional Arguments:
        type: The weather type, should be one of the above array
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
        location: A three dimensional array representing rotation in x,y,z
        """
        self.add_number_parameters(rotation)
