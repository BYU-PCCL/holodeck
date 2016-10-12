from .SimulatorAgent import SimulatorAgent
from .CommandBuilder import CommandBuilder
from collections import defaultdict
import json
import base64
import time

class AndroidAgent(SimulatorAgent):
    def __init__(self, hostname="localhost", port=8989, agentName="DefaultFlyingAgent",
                 global_state_sensors={}):
        super(AndroidAgent, self).__init__(hostname, port, agentName)

        self.loading_state = defaultdict(None)
        self.current_state = defaultdict(None)
        self.global_state_sensors = set(global_state_sensors)

        # Subscribe the function for sensor messages
        for sensor in self.global_state_sensors:
            self.subscribe(sensor, self._onGlobalStateSensor)

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

        if "PressureSensor" in self.current_state:
            pressure_readings = json.loads(self.current_state["PressureSensor"])
            output["PressureSensor"] = self.current_state["PressureSensor"]

        if "RelativeSkeletalPositionSensor" in self.current_state:
            skel_arr = []
            skeletal_positions = json.loads(self.current_state["RelativeSkeletalPositionSensor"])
            for obj in skeletal_positions:
                skel_arr.append(obj["Quaternion"]["X"])
                skel_arr.append(obj["Quaternion"]["Y"])
                skel_arr.append(obj["Quaternion"]["Z"])
                skel_arr.append(obj["Quaternion"]["W"])
            output["RelativeSkeletalPositionSensor"] = skel_arr

        if "JointRotationSensor" in self.current_state:
            joint_arr = []
            joint_rotations = json.loads(self.current_state["JointRotationSensor"])
            for obj in joint_rotations:
                joint_arr.append(obj)
            output["JointRotationSensor"] = joint_arr

        if "IMUSensor" in self.current_state:
            imu_arr = []
            imu_readings = json.loads(self.current_state["JointRotationSensor"])
            for obj in imu_readings:
                imu_arr.append(obj)
            output["IMUSensor"] = imu_arr

        return output