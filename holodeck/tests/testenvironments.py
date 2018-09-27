import holodeck
from holodeck import agents
from holodeck.environments import *
from holodeck.sensors import Sensors
import cv2

# test that pixel camera works properly
def camera_test(env, agent_name, command, test_time):

    # Test basic control and pixel_camera
    for i in range(1):
        env.reset()

        for j in range(test_time):
            state, reward, terminal, _ = env.step(command)

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
    for i in range(1):
        env.reset()

        state, reward, terminal, _ = env.step(command)

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

        for j in range(500):
            env.tick()

def world_command_test(env, agent_name, command, test_time):
    """A few examples to showcase commands for manipulating the worlds."""

    env.act(agent_name, command)

    print("Testing teleport camera")
    env.teleport_camera([11, 0, 11], [-1, 0, -1])
    for _ in range(test_time):
        _ = env.tick()
    env.reset()

    print("Testing set_day_time")
    # The set_day_time_command sets the hour between 0 and 23 (military time). This example sets it to 6 AM.
    env.set_day_time(6)
    for _ in range(test_time):
        _ = env.tick()
    env.reset()  # reset() undoes all alterations to the world

    print("Testing start_day_cycle")
    # The start_day_cycle command starts rotating the sun to emulate day cycles.
    # The parameter sets the day length in minutes.
    env.start_day_cycle(1)
    for _ in range(test_time*3):
        _ = env.tick()
    env.reset()

    print("Testing set_fog_density")
    # The set_fog_density changes the density of the fog in the world. 1 is the maximum density.
    env.set_fog_density(.5)
    for _ in range(test_time):
        _ = env.tick()
    env.reset()

    print("Testing set_weather(rain)")
    # The set_weather_command changes the weather in the world. The two available options are "rain" and "cloudy".
    # The rainfall particle system is attached to the agent, so the rain particles will only be found around each agent.
    # Every world is clear by default.
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

    #holodeck.package_info("DefaultWorlds")
    test_default_worlds()
    #holodeck.install("DefaultWorlds")
