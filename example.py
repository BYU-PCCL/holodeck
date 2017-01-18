import numpy as np
from tqdm import tqdm
import random
from Holodeck.HolodeckEnvironment import *
import time


def uav_example():
    print("Connecting to environment")
    env = HolodeckUAVMazeWorld(verbose=False, resolution=(256, 256))
    print("Connected")

    for x in range(10):
        for i in tqdm(range(100)):
            a = np.random.normal(size=3).reshape([1, 3])
            action = np.array([0, 0, 5, np.random.normal(loc=13, size=1)])
            state, reward, terminal, _ = env.step(action)
            print terminal

            # cv2.imshow('preview', state[0])
            # cv2.waitKey(1)

    env.reset()


def continuous_sphere_example():
    print("Connecting to environment")
    env = HolodeckContinuousSphereMazeWorld(verbose=True,resolution=(256,256))
    print("Connected")
    #action = np.array([[0, 0, 5, 14.70]])

    for x in range(10):
        for i in tqdm(range(100)):
            action = np.random.normal(size=2).reshape([2]) * 20.0
            print action
            state, reward, terminal, _ = env.step(action)

            # cv2.imshow('preview', state[0])
            # cv2.waitKey(1)
            # time.sleep(1)

        env.reset()


def discrete_sphere_example():
    print("Connecting to environment")
    env = HolodeckDiscreteSphereMazeWorld(verbose=True,resolution=(256,256))
    print("Connected")
    #action = np.array([[0, 0, 5, 14.70]])

    for x in range(10):
        for i in tqdm(range(100)):
            action = np.zeros([4], np.uint8)
            action[random.randint(0, 3)] = 1
            print action
            state, reward, terminal, _ = env.step(action)

            # cv2.imshow('preview', state[0])
            # cv2.waitKey(1)

        env.reset()


if __name__ == "__main__":
    uav_example()
    #continuous_sphere_example()
    #discrete_sphere_example()
    print("Finished")


