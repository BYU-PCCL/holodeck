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
    command = np.array([0, 0])
    for j in xrange(10):
        env.reset()
        for i in tqdm(range(300)):
            # command_str = raw_input("Command: ")
            # command_list = command_str.strip().split()
            # command[0] = command_list[0]
            # command[1] = command_list[1]
            # if (i / 100) % 2 == 0:
            #     command = np.array([1, 1], np.float32)
            # else:
            #     command = np.array([1, -1], np.float32)
            command = np.random.normal(0, 2, 2)
            state, reward, terminal, _ = env.step(command)
            # print i, reward, terminal, len(state)

            cv2.imshow("test", state[0])
            cv2.waitKey(1)


if __name__ == "__main__":
    editor_example()
    print("Finished")
