import holodeck
from holodeck.packagemanager import load_config
from holodeck.tests.test_utils import *


def test_spawn():	
	scenario_name = "AndroidPlayground-default"

    env = holodeck.make(scenario_name)

    agent_sensors = [sensors.LocationSensor]
    agent_def = AgentDefinition("uav0", agents.UavAgent, agent_sensors)


    start_loc = np.array([100, 100, 100])
    env.spawn_agent(agent_def, start_loc)

    state = env.tick()

    almost_equal(state["uav0"]["LocationSensor"], start_loc) 

    print("done")
    