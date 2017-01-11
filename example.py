import numpy as np
from tqdm import tqdm
import random
import cv2
from Holodeck.HolodeckEnvironment import HolodeckUAVEnvironment, HolodeckContinuousSphereEnvironment, HolodeckDiscreteSphereEnvironment
import time


def uav_example():
    print("Connecting to environment")
    env = HolodeckUAVEnvironment(verbose=True)
    print("Connected")
    action = np.array([[0, 0, 5, 14.70]])

    for x in range(10):
        for i in tqdm(range(100)):
            a = np.random.normal(size=3).reshape([1, 3])
            action = np.concatenate((a, np.random.normal(loc=13, size=1).reshape([1, 1])), axis=1)
            state, reward, terminal = env.act(action)

            # cv2.imshow('preview', state[0])
            # cv2.waitKey(1)

        env.reset()


def continuous_sphere_example():
    print("Connecting to environment")
    env = HolodeckContinuousSphereEnvironment(verbose=True)
    print("Connected")
    #action = np.array([[0, 0, 5, 14.70]])

    for x in range(10):
        for i in tqdm(range(100)):
            action = np.random.normal(size=2).reshape([2]) * 20.0
            state, reward, terminal = env.act(action)

            # cv2.imshow('preview', state[0])
            # cv2.waitKey(1)
            time.sleep(1)

        env.reset()


def discrete_sphere_example():
    print("Connecting to environment")
    env = HolodeckDiscreteSphereEnvironment(verbose=True)
    print("Connected")
    #action = np.array([[0, 0, 5, 14.70]])

    for x in range(10):
        for i in tqdm(range(100)):
            action = np.zeros([4], np.uint8)
            action[random.randint(0, 3)] = 1
            state, reward, terminal = env.act(action)

            # cv2.imshow('preview', state[0])
            # cv2.waitKey(1)

        env.reset()


if __name__ == "__main__":
    discrete_sphere_example()
    print("Finished")


