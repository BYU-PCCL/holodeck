from SimulatorAgent import SimulatorAgent
from CommandBuilder import CommandBuilder

class AndroidAgent(SimulatorAgent):
    def __init__(self, hostname="localhost", port=8989, agentName="DefaultFlyingAgent"):
        super(AndroidAgent, self).__init__(hostname, port, agentName)

    class AndroidCommandBuilder(CommandBuilder):
        def __init__(self, agent, commandType='AndroidCommand'):
            super(self.__class__, self).__init__(agent, commandType)
            self.type = commandType

        def setBoneConstraint(self, bone, x, y, z, w, force):
            self.append('BoneConstraints', {
                "Bone": bone,
                "X": x,
                "Y": y,
                "Z": z,
                "W": w,
                "Force": force
            })

            return self

    def command(self):
        command = AndroidAgent.AndroidCommandBuilder(self)
        return command
