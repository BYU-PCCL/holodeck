from SimulatorAgent import SimulatorAgent
from CommandBuilder import CommandBuilder

class UAVAgent(SimulatorAgent):
    def __init__(self, hostname="localhost", port=8989, agentName="DefaultFlyingAgent"):
        super(UAVAgent, self).__init__(hostname, port, agentName)
        print "Initialized"

    class UAVCommandBuilder(CommandBuilder):
        def __init__(self, agent):
            super(self.__class__, self).__init__(agent, type="UAVCommand")
            self.type = "UAVCommand"

        def setLocalRotation(self, roll, pitch, yaw):
            self.update({
                "localRoll": roll,
                "localPitch": pitch,
                "localYaw": yaw
            })

            return self

        def setLocalTranslation(self, x, y, z):
            self.update({
                "x": x,
                "y": y,
                "z": z
            })

            return self

    def command(self):
        command = UAVAgent.UAVCommandBuilder(self)
        return command
