import zmq
import json

class SimulatorAgent(object):
    def __init__(self, hostname="localhost", port=8989, agentName="DefaultAgent"):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.setsockopt(zmq.IDENTITY, agentName.encode("ascii"))
        self.socket.connect("tcp://" + hostname + ":" + str(port))

    def sendCommand(self, type, command):
        message = {
            "type": type,
            "commandJSON": json.dumps(command)
        }

        return self.sendString(json.dumps(message))

    def sendString(self, string):
        return self.socket.send_string(string.encode("ascii"))

    def receive(self):
        data = self.socket.recv()
        if(data):
            data = json.loads(data)
        return  data

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


