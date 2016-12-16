import Holodeck.holodeck_agents as ha
import numpy as np
import json
import base64
import io
from scipy.misc import imread
import cv2

class HolodeckEnvironment:

    def __init__(self, agent_type, hostname="localhost", port=8989, agent_name="DefaultAgent",global_state_sensors={}):
        """

        :param agent_type: str()
        :param hostname:
        :param port:
        :param agent_name:
        """
        agents = {"UAV": ha.UAVAgent, "SPHERE": ha.SphereRobotAgent, "ANDROID": ha.AndroidAgent}
        if agent_type in agents.keys():
            agent = agents[agent_type]
        else:
            raise KeyError(agent_type + " is not a valid agent type")
        self.AGENT = agents[agent_type](hostname=hostname, port=port, agentName=agent_name,global_state_sensors=global_state_sensors).waitFor("Connect")
        self.agent_type = agent_type

        #default have simulator to pause every 1 frame
        self.AGENT.worldCommand().setAllowedTicksBetweenCommands(1).send()

        # self.HOSTNAME = hostname
        # self.PORT = port
        # self.AGENT_NAME = agent_name

    def get_action_dim(self):
        return self.AGENT.get_action_space_dim()

    def get_state_dim(self):
        return self.AGENT.get_state_space_dim()

    def reset(self):
        self.AGENT.worldCommand().restartLevel().send()

    def act(self, action):
        assert action.shape == self.get_action_dim()

        self.AGENT.act(action)

        state = self.AGENT.get_state()

        sensor_data_list = []
        sensor_data = np.empty([1, 0])

        if "ViewportClient" in state:
            viewport_readings = state["ViewportClient"][1:-2].split(",")
            int_viewport_readings = map(int, viewport_readings)
            encoded_readings = bytearray(int_viewport_readings)

            fd = io.BytesIO( encoded_readings )
            np_img = imread( fd )
            out_np_img = cv2.cvtColor(np_img[:,:,:-1], cv2.COLOR_BGR2RGB)
            if len(np_img.shape) > 1:
                sensor_data_list.append(out_np_img)

        if "CameraSensorArray2D" in state:
            sensor = json.loads(state["CameraSensorArray2D"])
            for obj in sensor:
                for camera,base64_image in obj.items():
                    img = base64.b64decode(base64_image)

                    np_img = np.fromstring(img, dtype=np.uint8)
                    sensor_data_list.append(np_img)

        if "RelativeSkeletalPositionSensor" in state:
            skel_arr = []
            skeletal_positions = json.loads(state["RelativeSkeletalPositionSensor"])
            for obj in skeletal_positions:
                skel_arr.append(obj["Quaternion"]["X"])
                skel_arr.append(obj["Quaternion"]["Y"])
                skel_arr.append(obj["Quaternion"]["Z"])
                skel_arr.append(obj["Quaternion"]["W"])
            sensor_data = np.concatenate((sensor_data, np.array([skel_arr])), axis=1)

        if "JointRotationSensor" in state:
            joint_arr = []
            joint_rotations = json.loads(state["JointRotationSensor"])
            for obj in joint_rotations:
                joint_arr.append(obj)
            sensor_data = np.concatenate((sensor_data, np.array([joint_arr])), axis=1)

        if "IMUSensor" in state:
            imu_arr = []
            imu_readings = json.loads(state["IMUSensor"])
            for obj in imu_readings:
                imu_arr.append(obj)
            sensor_data = np.concatenate((sensor_data, np.array([imu_arr])), axis=1)

        # if "PressureSensor" in state:
        #     pressure_readings = json.loads(state["PressureSensor"])
        #     output["PressureSensor"] = state["PressureSensor"]

        sensor_data_list.append(sensor_data)

        return (sensor_data_list,
                state["Score"] if "Score" in state else None,
                state["Terminal"] if "Terminal" in state else None)
