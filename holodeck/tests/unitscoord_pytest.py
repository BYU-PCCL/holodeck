import holodeck
from holodeck import agents
from holodeck import sensors
from holodeck.environments import *
from holodeck.tests.test_utils import *
import math

editor_test = True


def rot_matrix_to_euler_angles(R):
    sy = math.sqrt(R[0, 0] * R[0, 0] + R[1, 0] * R[1, 0])

    singular = sy < 1e-6

    if not singular:
        x = math.atan2(R[2, 1], R[2, 2])
        y = math.atan2(-R[2, 0], sy)
        z = math.atan2(R[1, 0], R[0, 0])
    else:
        x = math.atan2(-R[1, 2], R[1, 1])
        y = math.atan2(-R[2, 0], sy)
        z = 0

    return np.array([x, y, z])


def test_sensor_coords():

    if editor_test:
        env = HolodeckEnvironment(start_world=False)

    else:
        env = holodeck.make("UrbanCity")

    env.reset()

    agent_sensors = [sensors.RGBCamera, sensors.LocationSensor, sensors.VelocitySensor, sensors.OrientationSensor, sensors.IMUSensor]
    agent = AgentDefinition("uav0", agents.UavAgent, agent_sensors)

    # Test spawning units
    loc = [12, 30, 100]
    env.spawn_agent(agent, loc)
    state = env.tick()
    sensed_loc = state["uav0"]["LocationSensor"]
    assert almost_equal(loc, sensed_loc)

    # Test teleport units
    loc = [138, 303, 10560]
    env.teleport("uav0", loc)
    state = env.tick()
    sensed_loc = state["uav0"]["LocationSensor"]
    assert almost_equal(loc, sensed_loc)

    # Test teleport and rotate and units
    loc = [123, 3740, 1030]
    rot = [1,6,4]
    env.teleport("uav0", loc, rot)
    state = env.tick()
    sensed_loc = state["uav0"]["LocationSensor"]
    sensed_rot = state["uav0"]["OrientationSensor"]
    sensed_rot = rot_matrix_to_euler_angles(sensed_rot)
    assert almost_equal(loc, sensed_loc)
    assert almost_equal(rot, sensed_rot)

    print("done")



