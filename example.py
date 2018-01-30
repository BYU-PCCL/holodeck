import numpy as np

from Holodeck import Holodeck, Agents
from Holodeck.Environments import *
from Holodeck.Sensors import Sensors


# This is a basic example of how to use the UAV agent
def uav_example():
    env = Holodeck.make("UrbanCity")

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
            # For a full list of sensors the sphere robot as, view the README


# This editor example shows how to interact with Holodeck worlds while they are being built
# in the Unreal Engine. Most people that use Holodeck will not need this.
def editor_example():
    sensors = [Sensors.PRIMARY_PLAYER_CAMERA, Sensors.LOCATION_SENSOR, Sensors.VELOCITY_SENSOR]
    agent = AgentDefinition("sphere0", Agents.ContinuousSphereAgent, sensors)
    env = HolodeckEnvironment(agent, start_world=False)
    command = np.random.normal(0, 5, 2)

    for i in range(10):
        env.reset()
        for _ in range(300):
            state, reward, terminal, _ = env.step(command)


# This editor example shows how to interact with Holodeck worlds that have multiple agents.
# This is specifically for when working with UE4 directly and not a prebuilt binary.
def editor_multi_agent_example():
    agents = [AgentDefinition("uav0", Agents.UAVAgent, [Sensors.PRIMARY_PLAYER_CAMERA, Sensors.LOCATION_SENSOR]),
              AgentDefinition("uav1", Agents.UAVAgent, [Sensors.LOCATION_SENSOR, Sensors.VELOCITY_SENSOR])]
    env = HolodeckEnvironment(agents, start_world=False)

    cmd1 = np.array([0, 0, 0.5, 5])
    cmd2 = np.array([0, 0, -0.7, 7])
    for i in range(10):
        env.reset()
        cmd2[3] = i
        env.act("uav0", cmd1)
        env.act("uav1", cmd2)
        for _ in tqdm(range(300)):
            states = env.tick()
            # print("********")
            # print(states)


if __name__ == "__main__":
    uav_example()
    print("Finished")
