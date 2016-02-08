import zmq
import json
import threading
from collections import defaultdict

class SimulatorAgent(object):
    def __init__(self, hostname="localhost", port=8989, agentName="DefaultAgent"):
        self.context = zmq.Context()
        self.socket = self.context.socket(zmq.DEALER)
        self.socket.setsockopt(zmq.IDENTITY, agentName.encode("ascii"))
        self.socket.connect("tcp://" + hostname + ":" + str(port))
        self.delegates = defaultdict(list)

        self.isListening = True
        self.thread = threading.Thread(target=self.listen)
        self.thread.start()

    def sendCommand(self, type, command):
        message = {
            "type": type,
            "commandjson": json.dumps(command)
        }

        return self.sendString(json.dumps(message))

    def sendString(self, string):
        return self.socket.send_string(string.encode("ascii"))

    def receive(self, blocking=True):
        try:
            data = self.socket.recv(flags=zmq.NOBLOCK if not blocking else None)
            return json.loads(data)

        except zmq.Again as e:
            return None

    def listen(self):
        while self.isListening:
            message = self.receive(False)
            if message is not None:
                message['type'] = 'Raw' + message['type']
                self.publish(message)

    def kill(self):
        self.isListening = False
        self.thread.join()

    def subscribe(self, type, function):
        self.delegates[type].append(function)

    def unsubscribe(self, type, function):
        self.delegates[type].remove(function)

    def publish(self, message):
        for function in self.delegates[message['type']]:
            function(message['data'])