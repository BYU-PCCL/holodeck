"""
Ensure that every scenario can be loaded and ticked a few times without crashing.
"""

import holodeck


def test_load_scenario(scenario):
    env = holodeck.make(scenario)
    for _ in range(30):
        env.tick()
    env.__on_exit__()


def test_all_agents_and_sensors_present(env_scenario):
    env, scenario = env_scenario
    scenario = holodeck.packagemanager.get_scenario(scenario)

    assert len(env.agents) == len(scenario['agents']), \
        "Length of agents did not match!"

    for agent in scenario['agents']:
        assert agent['agent_name'] in env.agents, \
            "Agent is not in the environment!"

        assert len(agent['sensors']) == len(env.agents[agent['agent_name']].sensors), \
            "length of sensors did not match!"

        for sensor in agent['sensors']:
            assert sensor['sensor_type'] in env.agents[agent['agent_name']].sensors, \
                "Sensor is missing!"

