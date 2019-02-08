"""This file contains multiple examples of how you might use Holodeck."""
import numpy as np

import holodeck
from holodeck import agents
from holodeck.environments import *
from holodeck import sensors


def uav_example():
    """A basic example of how to use the UAV agent."""
    env = holodeck.make("UrbanCity")

    # This changes the control scheme for the uav
    env.agents["uav0"].set_control_scheme(ControlSchemes.UAV_ROLL_PITCH_YAW_RATE_ALT)

    for i in range(10):
        env.reset()

        # This command tells the UAV to not roll or pitch, but to constantly yaw left at 10m altitude.
        command = np.array([0, 0, 2, 10])
        for _ in range(1000):
            state, reward, terminal, _ = env.step(command)

            # To access specific sensor data:
            pixels = state["RGBCamera"]
            velocity = state["VelocitySensor"]
            # For a full list of sensors the UAV has, view the README

    # You can control the AgentFollower camera (what you see) by pressing V to toggle spectator
    # mode. This detaches the camera and allows you to move freely about the world.
    # You can also press C to snap to the location of the camera to see the world from the perspective of the
    # agent. See the Controls section of the ReadMe for more details.


def sphere_example():
    """A basic example of how to use the sphere agent."""
    env = holodeck.make("MazeWorld")

    # This command is to constantly rotate to the right
    command = 2
    for i in range(10):
        env.reset()
        for _ in range(1000):
            state, reward, terminal, _ = env.step(command)

            # To access specific sensor data:
            pixels = state["RGBCamera"]
            orientation = state["OrientationSensor"]

    # For a full list of sensors the sphere robot has, view the README


def android_example():
    """A basic example of how to use the android agent."""
    env = holodeck.make("AndroidPlayground")

    # The Android's command is a 94 length vector representing torques to be applied at each of his joints
    command = np.ones(94) * 10
    for i in range(10):
        env.reset()
        for j in range(1000):
            if j % 50 == 0:
                command *= -1

            state, reward, terminal, _ = env.step(command)

            # To access specific sensor data:
            pixels = state["RGBCamera"]
            orientation = state["OrientationSensor"]

    # For a full list of sensors the android has, view the README


def multi_agent_example():
    """A basic example of using multiple agents"""
    env = holodeck.make("UrbanCity")

    cmd0 = np.array([0, 0, -2, 10])
    cmd1 = np.array([0, 0, 5, 10])
    for i in range(10):
        env.reset()
        # This will queue up a new agent to spawn into the environment, given that the coordinates are not blocked.
        env.agents["uav0"].set_control_scheme(ControlSchemes.UAV_ROLL_PITCH_YAW_RATE_ALT)

        env.tick()  # Tick the environment once so the second agent spawns before we try to interact with it.
        env.act("uav0", cmd0)
        for _ in range(1000):
            states = env.tick()
            uav0_terminal = states["uav0"]["Terminal"]
            uav1_reward = states["uav1"]["Reward"]


def world_command_examples():
    """A few examples to showcase commands for manipulating the worlds."""
    env = holodeck.make("MazeWorld")

    # This is the unaltered MazeWorld
    for _ in range(300):
        _ = env.tick()
    env.reset()

    # The set_day_time_command sets the hour between 0 and 23 (military time). This example sets it to 6 AM.
    env.set_day_time(6)
    for _ in range(300):
        _ = env.tick()
    env.reset()  # reset() undoes all alterations to the world

    # The start_day_cycle command starts rotating the sun to emulate day cycles.
    # The parameter sets the day length in minutes.
    env.start_day_cycle(5)
    for _ in range(1500):
        _ = env.tick()
    env.reset()

    # The set_fog_density changes the density of the fog in the world. 1 is the maximum density.
    env.set_fog_density(.25)
    for _ in range(300):
        _ = env.tick()
    env.reset()

    # The set_weather_command changes the weather in the world. The two available options are "rain" and "cloudy".
    # The rainfall particle system is attached to the agent, so the rain particles will only be found around each agent.
    # Every world is clear by default.
    env.set_weather("rain")
    for _ in range(500):
        _ = env.tick()
    env.reset()

    env.set_weather("cloudy")
    for _ in range(500):
        _ = env.tick()
    env.reset()

    env.teleport_camera([1000, 1000, 1000], [0, 0, 0])
    for _ in range(500):
        _ = env.tick()
    env.reset()


def editor_example():
    """This editor example shows how to interact with holodeck worlds while they are being built
    in the Unreal Engine. Most people that use holodeck will not need this.
    """
    agent_sensors = [sensors.RGBCamera, sensors.LocationSensor, sensors.VelocitySensor]
    agent = AgentDefinition("uav0", agents.UavAgent, agent_sensors)
    env = HolodeckEnvironment([agent], start_world=False)
    env.agents["uav0"].set_control_scheme(1)
    command = [0, 0, 10, 50]

    for i in range(10):
        env.reset()
        for _ in range(1000):
            state, reward, terminal, _ = env.step(command)


def editor_multi_agent_example():
    """This editor example shows how to interact with holodeck worlds that have multiple agents.
    This is specifically for when working with UE4 directly and not a prebuilt binary.
    """
    agent_definitions = [
        AgentDefinition("uav0", agents.UavAgent, [sensors.RGBCamera, sensors.LocationSensor]),
        AgentDefinition("uav1", agents.UavAgent, [sensors.LocationSensor, sensors.VelocitySensor])
    ]
    env = HolodeckEnvironment(agent_definitions, start_world=False)

    cmd0 = np.array([0, 0, -2, 10])
    cmd1 = np.array([0, 0, 5, 10])

    for i in range(10):
        env.reset()
        env.act("uav0", cmd0)
        env.act("uav1", cmd1)
        for _ in range(1000):
            states = env.tick()

            uav0_terminal = states["uav0"][sensors.Terminal]
            uav1_reward = states["uav1"][sensors.Reward]


if __name__ == "__main__":

    if 'DefaultWorlds' not in holodeck.installed_packages():
        # This will install the binaries for the DefaultWorlds Package if it is not already installed.
        holodeck.install("DefaultWorlds")
        print(holodeck.package_info("DefaultWorlds"))

    uav_example()
