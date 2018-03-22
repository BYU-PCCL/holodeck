import numpy as np
from .Agents import *


class Commands(object):
    def __init__(self):
        self._commands = []

    def add_command(self, command):
        self._commands.append(command)

    def to_json(self):
        to_return = "{\"commands\": ["
        for x in self._commands:
            to_return += x.to_json() + ","
        if len(self._commands) > 0:
            to_return = to_return[:-1]
        to_return += "]}"
        return to_return


class Command(object):

    def __init__(self):
        self._number_parameters = []
        self._string_parameters = []
        self._command_type = ""

    def set_command_type(self, command_type):
        self._command_type = command_type

    def add_number_parameters(self, number):
        if type(number) == list:
            self._number_parameters.extend(number)
            return
        self._number_parameters.append(number)

    def add_string_parameters(self, string):
        if type(string) == list:
            self._string_parameters.extend(string)
            return
        self._string_parameters.append(string)

    def to_json(self):
        to_return = "{ "
        to_return += "\"type\": \"" + self._command_type + "\", "
        to_return += "\"params\": ["
        for item in self._number_parameters:
            to_return += "{ \"value\": " + str(item) + " },"
        for item in self._string_parameters:
            to_return += "{ \"value\": \"" + str(item) + "\" },"
        to_return = to_return[:-1]
        to_return += "]}"
        return to_return


class SpawnAgentCommand(Command):
    __type_keys__ = {
        DiscreteSphereAgent: "SphereRobot",
        UAVAgent: "UAV",
        NavAgent: "NavAgent",
        AndroidAgent: "Android"
    }

    def __init__(self, location, name, agent_type):
        Command.__init__(self)
        self._command_type = "SpawnAgent"
        self.set_location(location)
        self.set_type(agent_type)
        self.set_name(name)

    def set_location(self, location):
        if len(location) != 3:
            print("Invalid location given to spawn agent command")
            return
        self.add_number_parameters(location)

    def set_name(self, name):
        self.add_string_parameters(name)

    def set_type(self, agent_type):
        type_str = SpawnAgentCommand.__type_keys__[agent_type]
        self.add_string_parameters(type_str)






