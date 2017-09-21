import numpy as np
from tqdm import tqdm
from Holodeck.HolodeckEnvironment import *
from Holodeck.HolodeckSensors import HolodeckSensor
import cv2
import time


def editor_example():
    env = HolodeckEnvironment(agent_name="sphere0", task_key=HolodeckMaps.MAZE_WORLD_SPHERE,
                              agent_type=Holodeck.HolodeckAgents.ContinuousSphereAgent)
    env.add_state_sensors([HolodeckSensor.PRIMARY_PLAYER_CAMERA, HolodeckSensor.ORIENTATION_SENSOR])

    print("Connected")
    for i in xrange(10):
        env.reset()
        for _ in tqdm(range(300)):
            command = np.random.normal(0, 5, 2)
            state, reward, terminal, _ = env.step(command)


if __name__ == "__main__":
    editor_example()
    print("Finished")
