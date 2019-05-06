import holodeck
from holodeck import agents
from holodeck import sensors
from holodeck.environments import *
from holodeck.tests.test_utils import *

editor_test = True

def test_sensor_coords():

    if editor_test:
        env = HolodeckEnvironment(start_world=False)

    else:
        env = holodeck.make("UrbanCity")

    env.reset()

    agent_sensors = [sensors.RGBCamera, sensors.LocationSensor, sensors.OrientationSensor, sensors.VelocitySensor, sensors.RotationSensor, sensors.IMUSensor]
    agent = AgentDefinition("uav0", agents.UavAgent, agent_sensors)

    # Test spawning units
    loc = [12, 30, 100]
    env.spawn_agent(agent, loc)
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



