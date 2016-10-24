from .SimulatorAgent import SimulatorAgent
from .CommandBuilder import CommandBuilder
from collections import defaultdict
import json
import base64
import time

class SphereRobotAgent(SimulatorAgent):
    def __init__(self, hostname="localhost", port=8989, agentName="DefaultFlyingAgent",
                 global_state_sensors={}):
        super(SphereRobotAgent, self).__init__(hostname, port, agentName)

        self.loading_state = defaultdict(None)
        self.current_state = defaultdict(None)
        self.global_state_sensors = set(global_state_sensors)

        # Subscribe the function for sensor messages
        for sensor in self.global_state_sensors:
            self.subscribe(sensor, self._onGlobalStateSensor)

    class SphereRobotBuilder(CommandBuilder):
        def __init__(self, agent, commandType='SphereRobotCommand'):
            super(self.__class__, self).__init__(agent, commandType)
            self.type = commandType

        def moveForward(self, value):
            self.update({"Forward": value})
            return self

        def moveRight(self, value):
            self.update({"Right": value})
            return self

    def command(self):
        command = SphereRobotAgent.SphereRobotBuilder(self)
        return command

    def _onGlobalStateSensor(self, data, type):
        self.loading_state[type] = data

        if set(self.loading_state.keys()) == self.global_state_sensors:
            self.publish({'type': 'State',
                          'data': self.current_state})

    def getNextState(self):
        """Returns the most recent readings from sensors as the current state."""

        #wait for all sensors to come in. Add way to get out when a sensor fails to arrive?
        while set(self.loading_state.keys()) != self.global_state_sensors:
            time.sleep(.05)

        #load in current state
        self.current_state = self.loading_state
        self.loading_state = defaultdict(None)

        output = {}

        if "CameraSensorArray2D" in self.current_state:
            camera_arr = []
            sensor = json.loads(self.current_state["CameraSensorArray2D"])
            for obj in sensor:
                for camera,base64_image in obj.items():
                    img = base64.b64decode(base64_image)
                    camera_arr.append(img)
            output["CameraSensorArray2D"] = camera_arr

        if "Score" in self.current_state:
            output["Score"] = self.current_state["Score"]

        if "Terminal" in self.current_state:
            output["Terminal"] = self.current_state["Terminal"]


        return output