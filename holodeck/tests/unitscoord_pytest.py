import holodeck
from holodeck import agents
from holodeck import sensors
from holodeck.environments import *
from holodeck.tests.test_utils import *
import math

editor_test = True

# LHS Version
def eulerAnglesToRotationMatrix(theta):
    theta = np.copy(np.array(theta))
    theta[0] *= -1
    theta[2] *= -1

    R_x = np.array([[1, 0, 0],
                    [0, math.cos(theta[0]), -math.sin(theta[0])],
                    [0, math.sin(theta[0]), math.cos(theta[0])]
                    ])

    R_y = np.array([[math.cos(theta[1]), 0, math.sin(theta[1])],
                    [0, 1, 0],
                    [-math.sin(theta[1]), 0, math.cos(theta[1])]
                    ])

    R_z = np.array([[math.cos(theta[2]), -math.sin(theta[2]), 0],
                    [math.sin(theta[2]), math.cos(theta[2]), 0],
                    [0, 0, 1]
                    ])

    R = np.dot(R_z, np.dot(R_y, R_x))

    return R


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
    loc = [138, 303, 902]
    env.teleport("uav0", loc)
    state = env.tick()
    sensed_loc = state["uav0"]["LocationSensor"]
    assert almost_equal(loc, sensed_loc)

    # Test teleport and rotate and units
    loc = [123, 3740, 1030]
    rot_deg = np.array([0, 0, 90])
    rot_rad = rot_deg * math.pi / 180.0
    rot_matrix = eulerAnglesToRotationMatrix(rot_rad)
    env.teleport("uav0", loc, rot_deg)
    state = env.tick()
    sensed_loc = state["uav0"]["LocationSensor"]
    sensed_rot = state["uav0"]["OrientationSensor"]
    assert almost_equal(loc, sensed_loc)
    assert almost_equal(rot_matrix, sensed_rot)

    print("done")



