import zmq
import json
import threading
from collections import defaultdict
import time
from .CommandBuilder import CommandBuilder

class SimulatorAgent(object):
    def __init__(self, hostname="localhost", port=8989, agentName="DefaultAgent"):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.setsockopt(zmq.IDENTITY, agentName.encode("ascii"))
        self.socket.connect("tcp://" + hostname + ":" + str(port))
        self.socket.setsockopt(zmq.SNDTIMEO, 500)
        self.delegates = defaultdict(list)

        self.isListening = True
        self.thread = threading.Thread(target=self.listen)
        self.thread.start()

    class WorldCommandBuilder(CommandBuilder):
        def __init__(self, agent, commandType='SimulatorCommand'):
           super(self.__class__, self).__init__(agent, commandType)
           self.type = commandType

        def setAllowedTicksBetweenCommands(self, ticks):
            self.update({
                "AllowedTicksBetweenCommands": ticks
            })

            return self

        def setLocalTranslation(self,seconds):
            self.update({
                "TimeDeltaBetweenTicks": seconds
            })

            return self

        def restartLevel(self):
            self.update({
                "Restart": True
            })

            return self

    def waitFor(self, type):
        class context:
            isWaiting = True

        def wait(command, type):
            context.isWaiting = False

        self.subscribe(type, wait)

        while(context.isWaiting):
            self.sendCommand("WaitFor" + type, None)
            time.sleep(1)

        self.unsubscribe(type, wait)

        return self

    def sendCommand(self, type, command):
        message = {
            "CommandType": type,
            "CommandJSON": json.dumps(command) if command else ""
        }
        return self.sendString(json.dumps(message))

    def sendString(self, string):
        #print(string)
        #print(type(string))
        return self.socket.send_string(string)#.encode("ascii"))

    def receive(self, blocking=True):
        try:
            data = self.socket.recv(flags=zmq.NOBLOCK if not blocking else None)
            return json.loads(data.decode())

        except zmq.Again as e:
            return None

    def listen(self):
        while self.isListening:
            message = self.receive(False)
            if message is not None:
                message['type'] = message['type']
                self.publish(message)

    def kill(self):
        self.socket.setsockopt(zmq.LINGER, 0)
        self.socket.close()
        self.isListening = False
        self.thread.join()

    def subscribe(self, type, function):
        self.delegates[type].append(function)

    def unsubscribe(self, type, function):
        self.delegates[type].remove(function)

    def publish(self, message):
        for function in self.delegates[message['type']]:
            function(message['data'], message['type'])

    def worldCommand(self):
        command = SimulatorAgent.WorldCommandBuilder(self)
        return command
