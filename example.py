import numpy as np

from Holodeck import Holodeck, Agents
from Holodeck.Environments import HolodeckEnvironment
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
    env = HolodeckEnvironment(agent_name="sphere0", agent_type=Agents.ContinuousSphereAgent,
                              start_world=False)
    env.add_state_sensors([Sensors.PRIMARY_PLAYER_CAMERA, Sensors.ORIENTATION_SENSOR])

    for i in range(10):
        env.reset()
        for _ in range(300):
            command = np.random.normal(0, 5, 2)
            state, reward, terminal, _ = env.step(command)


if __name__ == "__main__":
    uav_example()
    print("Finished")
