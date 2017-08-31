import numpy as np
from tqdm import tqdm
from Holodeck.HolodeckEnvironment import *
from Holodeck.HolodeckSensors import HolodeckSensor
import cv2
import time


def editor_example():
    print("Connecting to android environment")
    env = HolodeckEnvironment(agent_name="sphere0", start_world=False,
                              agent_type=Holodeck.HolodeckAgents.ContinuousSphereAgent)
    env.add_state_sensors([HolodeckSensor.PRIMARY_PLAYER_CAMERA, HolodeckSensor.ORIENTATION_SENSOR])

    print("Connected")
    command = None
    for j in xrange(10):
        for i in tqdm(range(300)):
            if (i / 100) % 2 == 0:
                command = np.array([1, 1], dtype=np.float32)
            else:
                command = np.array([-1, 1], dtype=np.float32)
            state, reward, terminal, _ = env.step(command)
            print i, reward, terminal, len(state)

            cv2.imshow("test", state[0])
            cv2.waitKey(1)

        env.reset()


if __name__ == "__main__":
    editor_example()
    print("Finished")

