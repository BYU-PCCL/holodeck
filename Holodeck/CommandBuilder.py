from collections import defaultdict

class CommandBuilder(object):
    def __init__(self, agent, type):
        self.command = defaultdict(object)
        self.agent = agent
        self.type = type

    def update(self, partialCommand):
        self.command.update(partialCommand)

    def append(self, property, partialCommand):
        if type(self.command[property]) is not list:
            self.command[property] = list()
        self.command[property].append(partialCommand)

    def send(self):
        self.agent.sendCommand(self.type, self.command)
        return self.command