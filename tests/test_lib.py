import holodeck
from holodeck.packagemanager import get_scenario
from test_utils import *


# Ensure that actions change the sensor data
def action_test(env, agent_name, action, sensors):

    num_ticks = 10

    env.reset()
    init = env._get_full_state()[agent_name]

    for _ in range(num_ticks):
        env.act(agent_name, action)
        final = env.tick()[agent_name]
    
    for sensor_name in init:
        if sensor_name in sensors:
            sensor1 = init[sensor_name]
            sensor2 = final[sensor_name]
            assert not almost_equal(sensor1, sensor2, r_thresh=0) 

    print("done")
