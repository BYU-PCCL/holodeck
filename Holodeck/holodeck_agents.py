from .SimulatorAgent import SimulatorAgent
from .CommandBuilder import CommandBuilder
from collections import defaultdict
import json
import base64
import time

class SphereRobotAgent(SimulatorAgent):
    def __init__(self, hostname="localhost", port=8989, agentName="DefaultFlyingAgent",
                 global_state_sensors={}):
        super(SphereRobotAgent, self).__init__(hostname, port, agentName,global_state_sensors)

        self._IMG_HEIGHT = 256
        self._IMG_WIDTH = 256
        self._IMG_CHANNELS = 3
        self._NUM_SENSORS = 3
        self._action_dim = (1,8)
        self._state_dim = ([self._IMG_HEIGHT, self._IMG_WIDTH, self._IMG_CHANNELS], [1, self._NUM_SENSORS])

    class SphereRobotBuilder(CommandBuilder):
        def __init__(self, agent, commandType='SphereRobotCommand'):
            super(self.__class__, self).__init__(agent, commandType)
            self.type = commandType

        def move(self, forward, right):
            self.update({
                "Forward": forward,
                "Right": right
                })
            return self

    def command(self):
        command = SphereRobotAgent.SphereRobotBuilder(self)
        return command

    def act(self,action):
        movements = [(1,0),(-1,0),(0,1),(0,-1),(1,1),(-1,-1),(1,-1),(-1,1)]
        for i in range(len(action[0])):
            if action[0][i] == 1:
                self.command().move(movements[i][0], movements[i][1]).send()

class UAVAgent(SimulatorAgent):
    def __init__(self, hostname="localhost", port=8989, agentName="DefaultFlyingAgent", global_state_sensors={}):
        super(UAVAgent, self).__init__(hostname, port, agentName, global_state_sensors)
        self._IMG_HEIGHT = 256
        self._IMG_WIDTH = 256
        self._IMG_CHANNELS = 3
        self._NUM_SENSORS = 4
        self._action_dim = (1,4)
        self._state_dim = ([self._IMG_HEIGHT, self._IMG_WIDTH, self._IMG_CHANNELS], [1, self._NUM_SENSORS])

    class UAVCommandBuilder(CommandBuilder):
        def __init__(self, agent, commandType='UAVCommand'):
            super(self.__class__, self).__init__(agent, commandType)
            self.type = commandType

        def set(self, roll, pitch, yaw, altitude):
            self.update({
                "Roll": roll,
                "Pitch": pitch,
                "YawRate": yaw,
                "Altitude": altitude
            })
            return self


    class UAVConfigurationBuilder(CommandBuilder):
        def __init__(self, agent, commandType='UAVConfiguration'):
            super(self.__class__, self).__init__(agent, commandType)
            self.type = commandType

            return self

    def command(self):
        command = UAVAgent.UAVCommandBuilder(self)
        return command

    def configure(self):
        configuration = UAVAgent.UAVConfigurationBuilder(self)
        return configuration

    def act(self,action):
        self.command().set(action[0][0], action[0][1], action[0][2], action[0][3]).send()
        return None



class AndroidAgent(SimulatorAgent):
    def __init__(self, hostname="localhost", port=8989, agentName="DefaultFlyingAgent",
                 global_state_sensors={}):
        super(AndroidAgent, self).__init__(hostname, port, agentName,global_state_sensors)

        self._IMG_HEIGHT = 256
        self._IMG_WIDTH = 256
        self._IMG_CHANNELS = 3
        self._NUM_SENSORS = 5
        self._action_dim = (1,127)
        self._state_dim = ([self._IMG_HEIGHT, self._IMG_WIDTH, self._IMG_CHANNELS], [1, self._NUM_SENSORS])

    class AndroidCommandBuilder(CommandBuilder):
        def __init__(self, agent, commandType='AndroidCommand'):
            super(self.__class__, self).__init__(agent, commandType)
            self.type = commandType

        def setJointRotationAndForce(self, boneConstraintVector):
            self.update({'ConstraintVector': boneConstraintVector})
            return self

        def getJointRotationAndForceSpace(self):
            return (127)

    class AndroidConfigurationBuilder(CommandBuilder):
        def __init__(self, agent, commandType='AndroidConfiguration'):
            super(self.__class__, self).__init__(agent, commandType)
            self.type = commandType

        def setCollisionsVisible(self, flag):
            self.update({
                "AreCollisionsVisible": flag
            })

            return self

    def command(self):
        command = AndroidAgent.AndroidCommandBuilder(self)
        return command

    def configure(self):
        configuration = AndroidAgent.AndroidConfigurationBuilder(self)
        return configuration

    def act(self,action):
        self.command().setJointRotationAndForce(list(action[0])).send()