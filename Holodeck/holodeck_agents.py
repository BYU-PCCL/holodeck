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

        def move(self, forward, right):
            self.update({
                "Forward": forward,
                "Right": right
                })
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
        """Returns the most recent readings from sensors as the current state.
        If all the sensor don't come in during the alloted time, an exception is thrown."""

        #wait for all sensors to come in. If time is exceeded, throw exception
        count = 0
        while set(self.loading_state.keys()) != self.global_state_sensors:
            time.sleep(.05)
            count += .05
            if count > 4:
                raise Exception()

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



class UAVAgent(SimulatorAgent):
    def __init__(self, hostname="localhost", port=8989, agentName="DefaultFlyingAgent"):
        super(UAVAgent, self).__init__(hostname, port, agentName)
        self._IMG_HEIGHT = 256
        self._IMG_WIDTH = 256
        self._IMG_CHANNELS = 3
        self._NUM_SENSORS = 4
        self._action_dim = [4]
        self._state_dim = ([self._IMG_HEIGHT, self._IMG_WIDTH, self._IMG_CHANNELS], [1, self._NUM_SENSORS])

    class UAVCommandBuilder(CommandBuilder):
        def __init__(self, agent, commandType='UAVCommand'):
            super(self.__class__, self).__init__(agent, commandType)
            self.type = commandType

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