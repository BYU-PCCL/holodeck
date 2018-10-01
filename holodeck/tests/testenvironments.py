import holodeck
from holodeck import agents
from holodeck.environments import *
from holodeck.sensors import Sensors
import cv2

"""
    Future Tests to Implement:
        Test to be run when releasing a new version:

        Pixel camera images can be retrieved properly and the sizes can be adjusted.
        Do the package manager functions work properly
        Test that multi agents work properly
        Test that the tasks work properly for the packaged worlds.
        Hyper parameters can be set correctly
        Sensors sense correctly
        Each agent in packaged worlds have all the sensors they should
        -Take screenshots at the beginning of each world as well sensor data and
        ensure that all the numbers and images line up. We don't want these changing between releases.
"""


# test that pixel camera works properly
def camera_test(env, agent_name, command, test_time):

    # Test basic control and pixel_camera
    for _ in range(1):
        env.reset()

        for j in range(test_time):
            state, _, _, _ = env.step(command)

            # To access specific sensor data:
            pixels = state[Sensors.PIXEL_CAMERA]
            if j < 2:
                cv2.namedWindow("Image")
                cv2.moveWindow("Image",500,500)
                cv2.imshow("Image", pixels[:, :, 0:3])
                cv2.waitKey(0)
                cv2.destroyAllWindows()


# TODO implement sensor checking
def sensor_test():
    # print different sensor results a couple times for each sensor
    pass


# Tests spawn agent works correctly.
def spawn_test(env, agent_name, command):

    # Test spawn, teleport agent and teleport camera
    for _ in range(1):
        env.reset()

        _ = env.step(command)

        spawn_loc = [0, 0, 20]

        sensors = [Sensors.LOCATION_SENSOR, Sensors.VELOCITY_SENSOR]
        agent = AgentDefinition("uav1", agents.UavAgent, sensors)

        env.spawn_agent(agent, spawn_loc)
        env.tick()
        env.set_control_scheme("uav1", ControlSchemes.UAV_ROLL_PITCH_YAW_RATE_ALT)

        command0 = [0, 0, 0, 1]
        command1 = [0, 0, 0, 10]
        env.act("uav0", command0)
        env.act("uav1", command1)

        for _ in range(500):
            env.tick()


def world_command_test(env, agent_name, command, test_time):

    env.act(agent_name, command)

    print("Testing teleport camera")
    env.teleport_camera([11, 0, 11], [-1, 0, -1])
    for _ in range(test_time):
        _ = env.tick()
    env.reset()

    print("Testing set_day_time")
    env.set_day_time(6)
    for _ in range(test_time):
        _ = env.tick()
    env.reset()

    print("Testing start_day_cycle")
    env.start_day_cycle(1)
    for _ in range(test_time*3):
        _ = env.tick()
    env.reset()

    print("Testing set_fog_density")
    env.set_fog_density(.5)
    for _ in range(test_time):
        _ = env.tick()
    env.reset()

    print("Testing set_weather(rain)")
    env.set_weather("rain")
    for _ in range(test_time):
        _ = env.tick()
    env.reset()

    print("Testing set_weather(cloudy)")
    env.set_weather("cloudy")
    for _ in range(test_time):
        _ = env.tick()
    env.reset()


def test_default_worlds():

    uav_worlds = ['EuropeanForest', 'RedwoodForest', 'UrbanCity', 'CyberPunkCity', 'InfiniteForest']
    sphere_worlds = ['MazeWorld']
    android_worlds = ['AndroidPlayground']

    test_time = 200

    for world in uav_worlds:
        env = holodeck.make(world)
        env.set_control_scheme("uav0", ControlSchemes.UAV_ROLL_PITCH_YAW_RATE_ALT)

        print("Testing World Commands")
        world_command_test(env, "uav0", [0, 0, 1, 10], test_time)

        print("Testing camera")
        camera_test(env, "uav0", [0, 0, 1, 10], test_time)

    for world in sphere_worlds:
        env = holodeck.make(world)

        print("Testing World Commands")
        world_command_test(env, "sphere0", 0, test_time)

        print("Testing camera")
        camera_test(env, "sphere0", 0, test_time)

    for world in android_worlds:
        env = holodeck.make(world)

        print("Testing World Commands")
        world_command_test(env, "android0", np.ones(94)*10, test_time)

        print("Testing camera")
        camera_test(env, "android0", np.ones(94)*10, test_time)


if __name__ == "__main__":

    test_default_worlds()
