"""This file contains multiple examples of how you might use Holodeck."""
import numpy as np

from Holodeck import Holodeck, Agents
from Holodeck.Environments import *
from Holodeck.Sensors import Sensors
from Holodeck.AgentSettings import *


def uav_example():
    """A basic example of how to use the UAV agent."""
    env = Holodeck.make("UrbanCity")

    # To get the mass of the UAV
    mass = env.get_setting("uav0", UAVSettings.UAV_MASS)

    for i in range(10):
        env.reset()

        # This command tells the UAV to not roll or pitch, but to constantly yaw left at 10m altitude.
        command = np.array([0, 0, 1, 10])
        for _ in range(300):
            state, reward, terminal, _ = env.step(command)

            # To access specific sensor data:
            pixels = state[Sensors.PRIMARY_PLAYER_CAMERA]
            velocity = state[Sensors.VELOCITY_SENSOR]
            # For a full list of sensors the UAV has, view the README


def sphere_example():
    """A basic example of how to use the sphere agent."""
    env = Holodeck.make("MazeWorld")

    # This command is to constantly rotate to the right
    command = 2
    for i in range(10):
        env.reset()
        for _ in range(300):
            state, reward, terminal, _ = env.step(command)

            # To access specific sensor data:
            pixels = state[Sensors.PRIMARY_PLAYER_CAMERA]
            orientation = state[Sensors.ORIENTATION_SENSOR]
            # For a full list of sensors the sphere robot has, view the README


def editor_example():
    """This editor example shows how to interact with Holodeck worlds while they are being built
    in the Unreal Engine. Most people that use Holodeck will not need this.
    """
    sensors = [Sensors.PRIMARY_PLAYER_CAMERA, Sensors.LOCATION_SENSOR, Sensors.VELOCITY_SENSOR]
    agent = AgentDefinition("uav0", Agents.UAVAgent, sensors)
    env = HolodeckEnvironment(agent, start_world=False)
    command = [0, 0, 1, 2]

    for i in range(10):
        #  for i in range(25):
        env.reset()
        for _ in range(300):
            state, reward, terminal, _ = env.step(command)


def editor_multi_agent_example():
    """This editor example shows how to interact with Holodeck worlds that have multiple agents.
    This is specifically for when working with UE4 directly and not a prebuilt binary.
    """
    agents = [AgentDefinition("uav0", Agents.UAVAgent, [Sensors.PRIMARY_PLAYER_CAMERA, Sensors.LOCATION_SENSOR]),
              AgentDefinition("uav1", Agents.UAVAgent, [Sensors.LOCATION_SENSOR, Sensors.VELOCITY_SENSOR])]
    env = HolodeckEnvironment(agents, start_world=False)

    cmd0 = np.array([0, 0, 0.5, 5])
    cmd1 = np.array([0, 0, -0.7, 7])
    for i in range(10):
        env.reset()
        env.act("uav0", cmd0)
        env.act("uav1", cmd1)
        for _ in range(300):
            states = env.tick()
            uav0_terminal = states["uav0"][Sensors.TERMINAL]
            uav1_reward = states["uav1"][Sensors.REWARD]


if __name__ == "__main__":
    uav_example()
    print("Finished")
