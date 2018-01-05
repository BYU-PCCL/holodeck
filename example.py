from __future__ import print_function
from tqdm import tqdm
import numpy as np

from Holodeck import Holodeck, Agents
from Holodeck.Environments import HolodeckEnvironment
from Holodeck.Sensors import Sensors


def editor_example():
    env = HolodeckEnvironment(agent_name="sphere0", agent_type=Agents.ContinuousSphereAgent,
                              start_world=False)
    env.add_state_sensors([Sensors.PRIMARY_PLAYER_CAMERA, Sensors.ORIENTATION_SENSOR])

    for i in range(10):
        env.reset()
        for _ in tqdm(range(300)):
            command = np.random.normal(0, 5, 2)
            state, reward, terminal, _ = env.step(command)


def sphere_example():
    env = Holodeck.make("ConiferForest")

    print("Connected")
    for i in range(10):
        env.reset()
        for _ in tqdm(range(300)):
            command = np.array([0, 0, 1, 10])
            state, reward, terminal, _ = env.step(command)


if __name__ == "__main__":
    sphere_example()
    print("Finished")
