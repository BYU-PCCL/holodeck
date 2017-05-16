import Holodeck.SimulatorAgent
from gym import spaces
from multiprocessing import Process
import subprocess
import atexit
import os

from HolodeckClient import HolodeckClient


class HolodeckEnvironment(object):
    def __init__(self, agent_type, agent_name, task_key=None, height=256, width=256, verbose=False,
                 grayscale=False, hostname="localhost", start_world=True):
        self._resolution = (height, width, 1 if grayscale else 3)
        self._grayscale = grayscale
        self._verbose = verbose
        self._state_sensors = ["Reward", "Terminal"]
        self._frames = 0
        self._client = HolodeckClient()

        task_map = {
            "TrainStation_UAV": "./worlds/TrainStation_UAV_v1.02/LinuxNoEditor/Holodeck/Binaries/Linux/Holodeck",
            "MazeWorld_UAV": "./worlds/MazeWorld_UAV_v1.00/LinuxNoEditor/Holodeck/Binaries/Linux/Holodeck",
            "ForestWorld_UAV": "./worlds/ForestWorld_UAV_v1.00/LinuxNoEditor/Holodeck/Binaries/Linux/Holodeck",
            "MazeWorld_sphere": "./worlds/MazeWorld_sphere_v1.00/LinuxNoEditor/Holodeck/Binaries/Linux/Holodeck",
            "ExampleWorld_android": ("./worlds/ExampleWorld_android_v1.00/LinuxNoEditor/Holodeck/"
                                     "Binaries/Linux/Holodeck")
        }

        if self._verbose:
            print "starting process"

        if start_world:
            self.world_process = subprocess.Popen([task_map[task_key], '-opengl4', '-SILENT', '-LOG=MyLog.txt',
                                                   '-ResX=' + str(width), " -ResY=" + str(height)],
                                                  stdout=open(os.devnull, 'w') if not verbose else None,
                                                  stderr=open(os.devnull, 'w') if not verbose else None)

        if self._verbose:
            print "process started"

        atexit.register(self.__on_exit__)

        if self._verbose:
            print "process registered for exit"

        self._agent = agent_type(hostname=hostname, port=8989, agentName=agent_name, height=height, width=width,
                                 grayscale=grayscale)
        self._agent.wait_for_connect()

    def __on_exit__(self):
        if hasattr(self, 'world_process'):
            self.world_process.kill()

    @property
    def action_space(self):
        return self._agent.action_space

    @property
    def observation_space(self):
        raise NotImplementedError()

    def reset(self):
        self.frames = 0
        self._agent.send_command('SimulatorCommand', {'Restart': True})

        return self.step(self.action_space.sample())[0]

    def render(self):
        pass

    def step(self, action):
        # note: this assert currently doesn't work with discrete sphere robot because it's a one hot vector
        # assert action.shape == self.action_space.sample().shape, (action.shape, self.action_space.sample().shape)

        self.frames += 1

        # act
        self._agent.act(action, self._client)

        # TODO: Ensure that responses are only received after acting

        # get responses
        result = []
        reward = None
        terminal = None
        for sensor in self._state_sensors:
            if sensor == "Reward":
                reward = self._client.get_sensor(self._agent.name, sensor)
            elif sensor == "Terminal":
                terminal = self._client.get_sensor(self._agent.name, sensor)
            else:
                result.append(self._client.get_sensor(self._agent.name, sensor))

        return result, reward, terminal, None

    def add_state_sensors(self, sensors):
        if type(sensors) == str:
            self._state_sensors.append(sensors)
        elif type(sensors) == list:
            self._state_sensors += sensors


class HolodeckUAVEnvironment(HolodeckEnvironment):
    def __init__(self, agent_name="UAV0", verbose=False, grayscale=False):
        super(HolodeckUAVEnvironment, self).__init__(agent_name=agent_name, verbose=verbose,
                                                     agent_type=Holodeck.SimulatorAgent.UAVAgent, grayscale=grayscale)
        self.state_sensors = ['PrimaryPlayerCamera']

    @property
    def observation_space(self):
        return spaces.Box(0, 255, shape=self._resolution)


class HolodeckUAVMazeWorld(HolodeckEnvironment):
    def __init__(self, agent_name="UAV0", verbose=False, resolution=(32, 32), grayscale=False, hostname="localhost",
                 start_world=True):
        super(HolodeckUAVMazeWorld, self).__init__(agent_name=agent_name, verbose=verbose, task_key="MazeWorld_UAV",
                                                   height=resolution[0], width=resolution[1],
                                                   agent_type=Holodeck.SimulatorAgent.UAVAgent, grayscale=grayscale,
                                                   hostname=hostname, start_world=start_world)
        self.add_state_sensors(['PrimaryPlayerCamera', "OrientationSensor"])

    @property
    def observation_space(self):
        return spaces.Box(0, 255, shape=self._resolution)


class HolodeckUAVForestWorld(HolodeckEnvironment):
    def __init__(self, agent_name="UAV0", verbose=False, resolution=(32, 32), grayscale=False, hostname="localhost",
                 start_world=True):
        super(HolodeckUAVForestWorld, self).__init__(agent_name=agent_name, verbose=verbose, task_key="ForestWorld_UAV",
                                                     height=resolution[0], width=resolution[1],
                                                     agent_type=Holodeck.SimulatorAgent.UAVAgent, grayscale=grayscale,
                                                     hostname=hostname, start_world=start_world)
        self.add_state_sensors(['PrimaryPlayerCamera', "OrientationSensor"])

    @property
    def observation_space(self):
        return spaces.Box(0, 255, shape=self._resolution)


class HolodeckContinuousSphereEnvironment(HolodeckEnvironment):
    def __init__(self, agent_name="sphere0", verbose=False, grayscale=False):
        super(HolodeckContinuousSphereEnvironment, self).__init__(agent_name=agent_name, verbose=verbose,
                                                                  agent_type=Holodeck.SimulatorAgent.ContinuousSphereAgent,
                                                                  grayscale=grayscale)
        self.add_state_sensors(['PrimaryPlayerCamera'])

    @property
    def observation_space(self):
        return spaces.Box(0, 255, shape=self._resolution)


class HolodeckContinuousSphereMazeWorld(HolodeckEnvironment):
    def __init__(self, agent_name="sphere0", verbose=False, resolution=(32, 32), grayscale=False, hostname="localhost",
                 start_world=True):
        super(HolodeckContinuousSphereMazeWorld, self).__init__(agent_name=agent_name, verbose=verbose,
                                                                task_key="MazeWorld_sphere",
                                                                height=resolution[0], width=resolution[1],
                                                                agent_type=Holodeck.SimulatorAgent.ContinuousSphereAgent,
                                                                grayscale=grayscale,
                                                                hostname=hostname, start_world=start_world)
        self.add_state_sensors(['PrimaryPlayerCamera'])

    @property
    def observation_space(self):
        return spaces.Box(-1, 1, shape=self._resolution)


class HolodeckDiscreteSphereEnvironment(HolodeckEnvironment):
    def __init__(self, agent_name="sphere0", verbose=False, grayscale=False, hostname="localhost", start_world=True):
        super(HolodeckDiscreteSphereEnvironment, self).__init__(agent_name=agent_name, verbose=verbose,
                                                                agent_type=Holodeck.SimulatorAgent.DiscreteSphereAgent,
                                                                grayscale=grayscale,
                                                                hostname=hostname, start_world=start_world)
        self.add_state_sensors(['PrimaryPlayerCamera'])

    @property
    def observation_space(self):
        return spaces.Box(0, 255, shape=self._resolution)


class HolodeckDiscreteSphereMazeWorld(HolodeckEnvironment):
    def __init__(self, agent_name="sphere0", verbose=False, resolution=(32, 32), grayscale=False, hostname="localhost",
                 start_world=True):
        super(HolodeckDiscreteSphereMazeWorld, self).__init__(agent_name=agent_name, verbose=verbose,
                                                              task_key="MazeWorld_sphere",
                                                              height=resolution[0], width=resolution[1],
                                                              agent_type=Holodeck.SimulatorAgent.DiscreteSphereAgent,
                                                              grayscale=grayscale,
                                                              hostname=hostname, start_world=start_world)
        self.add_state_sensors(['PrimaryPlayerCamera'])

    @property
    def observation_space(self):
        return spaces.Box(0, 255, shape=self._resolution)


class HolodeckAndroidEnvironment(HolodeckEnvironment):
    def __init__(self, agent_name="android0", verbose=False, grayscale=False, hostname="localhost", start_world=True):
        super(HolodeckAndroidEnvironment, self).__init__(agent_name=agent_name, verbose=verbose,
                                                         agent_type=Holodeck.SimulatorAgent.AndroidAgent,
                                                         grayscale=grayscale,
                                                         hostname=hostname, start_world=start_world)

        # self.agent.send_command('AndroidConfiguration', {"AreCollisionsVisible": True})
        # self.state_sensors = ['PrimaryPlayerCamera', 'IMUSensor', 'JointRotationSensor', 'RelativeSkeletalPositionSensor']
        self.add_state_sensors(['PrimaryPlayerCamera'])

    @property
    def observation_space(self):
        return spaces.Box(0, 255, shape=self._resolution)


class HolodeckAndroidExampleWorldEnvironment(HolodeckEnvironment):
    def __init__(self, agent_name="android0", verbose=False, resolution=(32, 32), grayscale=False, hostname="localhost",
                 start_world=True):
        super(HolodeckAndroidExampleWorldEnvironment, self).__init__(agent_name=agent_name, verbose=verbose,
                                                                     task_key="ExampleWorld_android",
                                                                     height=resolution[0], width=resolution[1],
                                                                     agent_type=Holodeck.SimulatorAgent.AndroidAgent,
                                                                     grayscale=grayscale,
                                                                     hostname=hostname, start_world=start_world)

        # self.agent.send_command('AndroidConfiguration', {"AreCollisionsVisible": True})
        # self.state_sensors = ['PrimaryPlayerCamera', 'IMUSensor', 'JointRotationSensor',
        # 'RelativeSkeletalPositionSensor']
        self.add_state_sensors(['PrimaryPlayerCamera', 'IMUSensor', 'JointRotationSensor',
                               'RelativeSkeletalPositionSensor'])

    @property
    def observation_space(self):
        return spaces.Box(0, 255, shape=self._resolution)
