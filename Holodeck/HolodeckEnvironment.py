import Holodeck.SimulatorAgent
from multiprocessing import Process
import os


class World:
    def start(self, world, width, height):
        os.system(world + " -SILENT LOG=MyLog.txt -ResX=" + str(width) + " -ResY=" + str(height) + " >/dev/null")


class HolodeckEnvironment:

    def __init__(self, agent_type, agent_name, task_key=None, height=256, width=256, verbose=False):
        self.resolution = (height, width, 1)
        self.verbose = verbose
        self.state_sensors = []
        self.frames = 0

        # task_map = {
        #     "TrainStation": "worlds/TrainStation_UAV_v1.00/LinuxNoEditor/Holodeck/Binaries/Linux/Holodeck"
        # }
        #
        # self.world_process = Process(target=World.start, args=(task_map[task_key], width, height))
        # self.world_process.start()

        self.agent = agent_type(hostname='localhost', port=8989, agentName=agent_name, height=height, width=width)
        self.agent.wait_for_connect()
        # self.agent.send_command('SimulatorCommand', {"AllowedTicksBetweenCommands": 1})

    def get_action_dim(self):
        return self.agent.get_action_dim()

    def get_state_dim(self):
        raise NotImplementedError()

    def reset(self):
        self.frames = 0
        self.agent.send_command('SimulatorCommand', {'Restart': True})

    def act(self, action):
        assert action.shape == self.get_action_dim()

        self.frames += 1

        response = self.agent.act(action, ['Terminal', 'Reward'] + self.state_sensors)
        terminal, reward = response[0], response[1]

        return response[2:], reward, terminal


class HolodeckUAVEnvironment(HolodeckEnvironment):
    def __init__(self, agent_name="UAV0", verbose=False):
        super(HolodeckUAVEnvironment, self).__init__(agent_name=agent_name, verbose=verbose,
                                                     agent_type=Holodeck.SimulatorAgent.UAVAgent)
        self.state_sensors = ['PrimaryPlayerCamera']

    def get_state_dim(self):
        return tuple(self.resolution)


class HolodeckContinuousSphereEnvironment(HolodeckEnvironment):
    def __init__(self, agent_name="sphere0", verbose=False):
        super(HolodeckContinuousSphereEnvironment, self).__init__(agent_name=agent_name, verbose=verbose,
                                                                  agent_type=Holodeck.SimulatorAgent.ContinuousSphereAgent)
        self.state_sensors = ['PrimaryPlayerCamera']

    def get_state_dim(self):
        return tuple(self.resolution)


class HolodeckDiscreteSphereEnvironment(HolodeckEnvironment):
    def __init__(self, agent_name="sphere0", verbose=False):
        super(HolodeckDiscreteSphereEnvironment, self).__init__(agent_name=agent_name, verbose=verbose,
                                                                agent_type=Holodeck.SimulatorAgent.DiscreteSphereAgent)
        self.state_sensors = ['PrimaryPlayerCamera']

    def get_state_dim(self):
        return tuple(self.resolution)


class HolodeckAndroidEnvironment(HolodeckEnvironment):
    def __init__(self, agent_name="android0", verbose=False):
        super(HolodeckAndroidEnvironment, self).__init__(agent_name=agent_name, verbose=verbose,
                                                         agent_type=Holodeck.SimulatorAgent.AndroidAgent)

        # self.agent.send_command('AndroidConfiguration', {"AreCollisionsVisible": True})
        self.state_sensors = ['PrimaryPlayerCamera', 'IMUSensor', 'JointRotationSensor', 'RelativeSkeletalPositionSensor']

    def get_state_dim(self):
        return tuple(self.resolution)