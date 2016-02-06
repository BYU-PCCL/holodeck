class CommandBuilder(object):
    def __init__(self, agent, type):
        self.command = None
        self.agent = agent
        self.type = type

    def update(self, partialCommand):
        self.command = self.command if self.command else dict()
        self.command.update(partialCommand)

    def send(self):
        self.agent.sendCommand(self.type, self.command)
        return None