import uuid
from holodeck import packagemanager as pm
from holodeck.environments import HolodeckEnvironment
import pytest
import math

test_data = [
    # agent_name, control_scheme, exp_min, exp_max, test_id
    pytest.param("AndroidAgent", 0, [-20 for _ in range(94)], [20 for _ in range(94)], id="AndroidAgent 0"),
    pytest.param("AndroidAgent", 1, [-1 for _ in range(94)], [1 for _ in range(94)], id="AndroidAgent 1"),
    pytest.param("UavAgent", 0, [-5.087, -6.5080, -0.8, -59.844], [5.087, 6.5080, 0.8, 59.844], id="UavAgent 1"),
    pytest.param("SphereAgent", 0, 0, 4, id="SphereAgent 0"),
    pytest.param("SphereAgent", 1, [-20, -20], [20, 20], id="SphereAgent 1"),
]

config = {
    "name": "test_collision_sensor",
    "world": "TestWorld",
    "main_agent": "test_agent",
    "agents": [
        {
            "agent_name": "UavAgent",
            "agent_type": "UavAgent",
            "sensors": [
                {
                    "sensor_type": "LocationSensor",
                }
            ],
            "control_scheme": 0,
            "location": [0, 0, 5]
        }
    ]
}


def is_close(a, b):
    for x, y in zip(a, b):
        if not math.isclose(x, y, rel_tol=1e-05):
            return False

    return True


@pytest.mark.parametrize("agent, control_scheme, exp_min, exp_max", test_data)
def test_min_max_action_space_constraints(agent, control_scheme, exp_min, exp_max):
    binary_path = pm.get_binary_path_for_package("DefaultWorlds")

    config["agents"][0]["agent_type"] = agent
    config["agents"][0]["agent_name"] = agent
    config["agents"][0]["control_scheme"] = control_scheme

    with HolodeckEnvironment(scenario=config,
                             binary_path=binary_path,
                             show_viewport=False,
                             uuid=str(uuid.uuid4())) as env:

        min_result = env.agents[agent].get_control_scheme_min_values(control_scheme)
        max_result = env.agents[agent].get_control_scheme_max_values(control_scheme)

        if type(min_result) == list:
            assert is_close(min_result, exp_min)
        else:
            assert math.isclose(min_result, exp_min, rel_tol=1e-05)

        if type(max_result) == list:
            assert is_close(max_result, exp_max)
        else:
            assert math.isclose(max_result, exp_max, rel_tol=1e-05)

