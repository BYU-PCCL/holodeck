from .SimulatorAgent import SimulatorAgent
from .CommandBuilder import CommandBuilder
from collections import defaultdict

class AndroidAgent(SimulatorAgent):
    def __init__(self, hostname="localhost", port=8989, agentName="DefaultFlyingAgent",
                 global_state_sensors={}):
        super(AndroidAgent, self).__init__(hostname, port, agentName)

        self.current_state = defaultdict(None)
        self.global_state_sensors = set(global_state_sensors)

        # Subscribe the function for sensor messages
        for sensor in self.global_state_sensors:
            self.subscribe(sensor, self._onGlobalStateeSensor)

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

    def _onGlobalStateeSensor(self, data, type):
        self.current_state[type] = data

        if set(self.current_state.keys()) == self.global_state_sensors:
            self.publish({'type': 'State',
                          'data': self.current_state})