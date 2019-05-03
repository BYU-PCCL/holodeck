import holodeck
from holodeck import agents
from holodeck import sensors
from holodeck.environments import *
from holodeck.tests.test_utils import *
import pytest

editor_test = True

@pytest.fixture(scope="session")
def env():

    loc = [12, 30, 100]
    agent_sensors = [sensors.RGBCamera, sensors.LocationSensor, sensors.OrientationSensor, sensors.VelocitySensor,
                     sensors.RotationSensor, sensors.IMUSensor]
    agent = AgentDefinition("uav0", agents.UavAgent, sensors=agent_sensors, starting_loc=loc)

    env = HolodeckEnvironment(start_world=False, agent_definitions = [agent])

    return env


def test_sensor_coords(env):
    env.reset()
    loc = [12, 30, 100]

    state = env.tick()
    sensed_loc = state["uav0"]["LocationSensor"]
    assert almost_equal(loc, sensed_loc)

    # Test teleport units
    loc = [138, 303, 902]
    env.teleport("uav0", loc)
    state = env.tick()
    sensed_loc = state["uav0"]["LocationSensor"]
    assert almost_equal(loc, sensed_loc)

    # Test teleport and rotate and units
    loc = [123, 3740, 1030]
    rot_deg = np.array([34, 25, 67])
    env.teleport("uav0", loc, rot_deg)
    state = env.tick()
    sensed_loc = state["uav0"]["LocationSensor"]
    sensed_rot = state["uav0"]["RotationSensor"]
    assert almost_equal(loc, sensed_loc)
    assert almost_equal(rot_deg, sensed_rot)


    # Test orientation sensor
    loc = [123, 3740, 1030]
    rot_deg = np.array([0, 90, 0])
    env.teleport("uav0", loc, rot_deg)
    state = env.tick()
    sensed_loc = state["uav0"]["LocationSensor"]
    sensed_or = state["uav0"]["OrientationSensor"]
    assert almost_equal(loc, sensed_loc)

    accurate_or = np.zeros((3,3))
    accurate_or[0,2] = 1.0
    accurate_or[1,1] = 1.0
    accurate_or[2,0] = -1.0

    assert almost_equal(accurate_or, sensed_or)
    print("done")


def test_set_state(env):
    env.reset()

    # Test spawning units
    loc = [12, 30, 100]
    rot = [34, 78, 94]
    vel = [1, 4, 3]
    ang_vel = [90, 180, 0]

    state = env.tick()
    env.set_state("uav0",loc, rot, (0,0,0), (0,0,0))
    state = env.tick()

    sensed_loc = state["uav0"]["LocationSensor"]
    sensed_rot = state["uav0"]["RotationSensor"]
    assert almost_equal(loc, sensed_loc)
    assert almost_equal(rot, sensed_rot)

    env.set_state("uav0", loc, rot, vel, ang_vel)
    state = env.tick()
    sensed_vel = state["uav0"]["VelocitySensor"]
    sensed_ang_vel = state["uav0"]["IMUSensor"][1]

    vel[2] = vel[2] - 9/30
    assert almost_equal(vel, sensed_vel, r_thresh=0.12)
    assert almost_equal(ang_vel, sensed_ang_vel, r_thresh=0.1,a_thresh=1e-2)


def test_adding_agent(env):

    loc = [23,50,284]
    rot = [34,2,90]

    agent_sensors = [sensors.RGBCamera, sensors.LocationSensor, sensors.OrientationSensor, sensors.VelocitySensor,
                     sensors.RotationSensor, sensors.IMUSensor]
    agent = AgentDefinition("uav1", agents.UavAgent, sensors=agent_sensors, starting_loc=loc)

    env.add_agent(agent)
    state = env.tick()
    env.set_state("uav1", loc, rot, (0, 0, 0), (0, 0, 0))
    state = env.tick()

    sensed_loc = state["uav1"]["LocationSensor"]
    sensed_rot = state["uav1"]["RotationSensor"]
    assert almost_equal(loc, sensed_loc)
    assert almost_equal(rot, sensed_rot)