import holodeck
from holodeck.packagemanager import get_scenario
from holodeck.tests.test_utils import *


# scenario_list = ["MazeWorld-default", "AndroidPlayground-default", "CyberPunkCity-default", 
#                  "EuropeanForest-default", "InfiniteForest-default", "RedwoodForest-default", 
#                  "UrbanCity-default"]
scenario_list = ["AndroidPlayground-default", "CyberPunkCity-default", 
                  "EuropeanForest-default", "RedwoodForest-default", 
                  "UrbanCity-default"]

def test_loading():
    for scenario_name in scenario_list:

        env = holodeck.make(scenario_name)
        scenario = get_scenario(scenario_name)
        initial_state = []

        env.reset()
        assert len(env.agents) == len(scenario['agents'])

        for agent in scenario['agents']:
            assert agent['agent_name'] in env.agents
            assert len(agent['sensors']) == len(env.agents[agent['agent_name']].sensors)

            for sensor in agent['sensors']:
                assert sensor['sensor_name'] in env.agents[agent['agent_name']].sensors

    print("done")


def test_reset():
    test_resets = 5

    for scenario_name in scenario_list:

        env = holodeck.make(scenario_name)
        scenario = get_scenario(scenario_name)
        initial_state = []

        init_state = env.reset()
        agent_count = len(env.agents)
        sensor_count = sum([len(env.agents[agent].sensors) for agent in env.agents])

        for _ in range(test_resets):
            env.tick()
            state = env.reset()

            assert state_almost_equal(init_state, state, 0.9)
            assert agent_count == len(env.agents)
            assert sensor_count == sum([len(env.agents[agent].sensors) for agent in env.agents])

    print("done")


def test_sensors():	
    num_ticks = 50

    for scenario_name in scenario_list:
        
        env = holodeck.make(scenario_name)
        scenario = get_scenario(scenario_name)

        init_state = env.reset()

        for _ in range(num_ticks):
            state = env.tick()
        print(init_state)
        print(state)

        if is_full_state(state):
            for agent in state:
                for sensor in state[agent]:
                    # Sensor values should change after ticks
                    assert not np.array_equal(state[agent][sensor], init_state[agent][sensor])
        else:
            for sensor in state:
                # Sensor values should change after ticks
                assert not np.array_equal(state[sensor], init_state[sensor])

    print("done")
