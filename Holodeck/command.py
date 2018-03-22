from .Agents import *


class CommandsGroup(object):
    """Holds Command objects in a list, and when requested packages everything in the correct json format"""
    def __init__(self):
        self._commands = []

    def add_command(self, command):
        """Adds a command to the list"""
        self._commands.append(command)

    def to_json(self):
        """Returns a string of the commands array object and all of the commands inside the array"""
        commands = ",".join(map(lambda x: x.to_json(), self._commands))
        return "{\"commands\": [" + commands + "]}"

    def clear(self):
        """Clears the list of commands"""
        self._commands.clear()


class Command(object):
    """Base class for Command objects. Can return itself in json format. You must set the command type."""
    def __init__(self):
        self._parameters = []
        self._command_type = ""

    def set_command_type(self, command_type):
        """Sets the type of the command"""
        self._command_type = command_type

    def add_number_parameters(self, number):
        """Adds number parameters to the list"""
        if isinstance(number, list):
            for x in number:
                self.add_number_parameters(x)
            return
        self._parameters.append("{ \"value\": " + str(number) + " }")

    def add_string_parameters(self, string):
        """Adds string parameters to the list"""
        if isinstance(string, list):
            for x in string:
                self.add_string_parameters(x)
            return
        self._parameters.append("{ \"value\": \"" + string + "\" }")

    def to_json(self):
        """Returns this object in json format"""
        to_return = "{ \"type\": \"" + self._command_type + "\", \"params\": [" + ",".join(self._parameters) + "]}"
        return to_return


class SpawnAgentCommand(Command):
    """Holds the information to be sent to Holodeck that is needed for spawning an agent."""
    __type_keys = {
        DiscreteSphereAgent: "SphereRobot",
        UAVAgent: "UAV",
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
        """Set the location to spawn the agent at"""
        if len(location) != 3:
            print("Invalid location given to spawn agent command")
            return
        self.add_number_parameters(location)

    def set_name(self, name):
        """Sets the name to give the agent"""
        self.add_string_parameters(name)

    def set_type(self, agent_type):
        """Sets the type of agent to spawn in Holodeck"""
        type_str = SpawnAgentCommand.__type_keys[agent_type]
        self.add_string_parameters(type_str)
