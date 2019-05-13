import holodeck
from holodeck.packagemanager import get_scenario
from holodeck.tests.test_utils import *


# Ensure that all agents and sensors exist in the world
def load_test(env, scenario_name):

    env.reset()
    scenario = get_scenario(scenario_name)
    assert len(env.agents) == len(scenario['agents'])

    for agent in scenario['agents']:
        assert agent['agent_name'] in env.agents
        assert len(agent['sensors']) == len(env.agents[agent['agent_name']].sensors)

        for sensor in agent['sensors']:
            assert sensor['sensor_type'] in env.agents[agent['agent_name']].sensors

    print("done")


# Ensure that resetting a world results in nearly identical sensor states
def reset_test(env, agent_name, sensors_to_ignore=None):
    test_resets = 5

    env.reset()
    init_state = env._get_full_state()[agent_name]
    agent_count = len(env.agents)
    sensor_count = sum([len(env.agents[agent].sensors) for agent in env.agents])

    for _ in range(test_resets):
        env.tick()
        env.reset()
        state = env._get_full_state()[agent_name]

        assert compare_agent_states(init_state, state, 0.3, is_close=True, to_ignore=sensors_to_ignore)
        assert agent_count == len(env.agents)
        assert sensor_count == sum([len(env.agents[agent].sensors) for agent in env.agents])

    print("done")


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
