"""This file contains multiple examples of how you might use Holodeck."""
import numpy as np

import holodeck
from holodeck import agents
from holodeck.environments import *
from holodeck.sensors import Sensors


def uav_example():
    """A basic example of how to use the UAV agent."""
    env = holodeck.make("UrbanCity")

    for i in range(10):
        env.reset()

        # This command tells the UAV to not roll or pitch, but to constantly yaw left at 10m altitude.
        command = np.array([0, 0, 1, 10])
        for _ in range(300):
            state, reward, terminal, _ = env.step(command)

            # To access specific sensor data:
            pixels = state[Sensors.PIXEL_CAMERA]
            velocity = state[Sensors.VELOCITY_SENSOR]
            # For a full list of sensors the UAV has, view the README

            # To access and change hyperparameters of the agent:
            params = env.get_hyperparameters()
            params[UAVHyperparameters.UAV_MAX_PITCH] = 0


def sphere_example():
    """A basic example of how to use the sphere agent."""
    env = holodeck.make("MazeWorld")

    # This command is to constantly rotate to the right
    command = 2
    for i in range(10):
        env.reset()
        for _ in range(300):
            state, reward, terminal, _ = env.step(command)

            # To access specific sensor data:
            pixels = state[Sensors.PIXEL_CAMERA]
            orientation = state[Sensors.ORIENTATION_SENSOR]
            # For a full list of sensors the sphere robot has, view the README

            # Note: The sphere agent doesn't have any hyperparameters.


def multi_agent_example():
    """A basic example of using multiple agents"""
    env = holodeck.make("UrbanCity")

    cmd0 = np.array([0, 0, 1, 5])
    cmd1 = np.array([0, 0, -0.7, 5])
    for i in range(10):
        env.reset()
        # This will queue up a new agent to spawn into the environment, given that the coordinates are not blocked.
        sensors = [Sensors.PIXEL_CAMERA, Sensors.LOCATION_SENSOR, Sensors.VELOCITY_SENSOR]
        agent = AgentDefinition("uav1", agents.UavAgent, sensors)
        env.spawn_agent(agent, [1, 1, 5])
        env.tick()  # Tick the environment once so the second agent spawns before we try to interact with it.

        env.act("uav0", cmd0)
        env.act("uav1", cmd1)
        for _ in range(600):
            states = env.tick()
            uav0_terminal = states["uav0"][Sensors.TERMINAL]
            uav1_reward = states["uav1"][Sensors.REWARD]
            uav1_hyperparameters = env.get_hyperparameters("uav1")


def editor_example():
    """This editor example shows how to interact with holodeck worlds while they are being built
    in the Unreal Engine. Most people that use holodeck will not need this.
    """
    sensors = [Sensors.PIXEL_CAMERA, Sensors.LOCATION_SENSOR, Sensors.VELOCITY_SENSOR]
    agent = AgentDefinition("uav0", agents.UavAgent, sensors)
    env = HolodeckEnvironment(agent, start_world=False)
    env.agents["uav0"].set_control_scheme(1)
    command = [0, 0, 1, 1]

    for i in range(10):
        env.reset()
        for _ in range(3000):
            state, reward, terminal, _ = env.step(command)


def editor_multi_agent_example():
    """This editor example shows how to interact with holodeck worlds that have multiple agents.
    This is specifically for when working with UE4 directly and not a prebuilt binary.
    """
    agent_definitions = [
        AgentDefinition("uav0", agents.UavAgent, [Sensors.PIXEL_CAMERA, Sensors.LOCATION_SENSOR]),
        AgentDefinition("uav1", agents.UavAgent, [Sensors.LOCATION_SENSOR, Sensors.VELOCITY_SENSOR])
    ]
    env = HolodeckEnvironment(agent_definitions, start_world=False)

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
