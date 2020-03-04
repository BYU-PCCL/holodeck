import uuid

from holodeck.environments import HolodeckEnvironment

from . import finish
import holodeck
from holodeck import packagemanager as pm
import pytest


weather_config = {
    "name": "test_weather_config",
    "world": "MazeWorld",
    "main_agent": "sphere0",
    "agents": [
        {
            "agent_name": "sphere0",
            "agent_type": "SphereAgent",
            "sensors": [
                {
                    "sensor_type": "RGBCamera",
                    "socket": "CameraSocket",
                    "sensor_name": "TestCamera",
                }
            ],
            "control_scheme": 0,
            "location": [0.95, -1.75, 0.5],
        }
    ],
    "window_width": 1024,
    "window_height": 1024,
}

weather_type_test_data = [
    # weather_type, max_err
    pytest.param("sunny", 1000, id="Sunny"),
    pytest.param("cloudy", 1000, id="Cloudy"),
    pytest.param("rain", 1000, id="Rain"),
]

fog_density_test_data = [
    # fog_depth, max_err
    pytest.param(0, 1000, id="Fog density 0%"),
    pytest.param(1, 1000, id="Fog density 100%"),
]

time_test_data = [
    # hour, max_err
    pytest.param(0, 1000, id="Time 0"),
    pytest.param(12, 1000, id="Time 12"),
    pytest.param(23, 1000, id="Time 23"),
]

day_cycle_test_data = [
    # cycle_length, max_err_before, max_err_after
    pytest.param(1, 500, 1000, 1000, id="1 minute day cycle"),
    pytest.param(5, 500, 1000, 1000, id="5 minute day cycle"),
    pytest.param(30, 500, 1000, 1000, id="30 minute day cycle"),
]


def generate_mazeworld_walkthrough():
    """Runs through Mazeworld and records state at every tic, so that tests
    can analyze the results
    without having to run through the maze multiple times

    Returns: list of 4tuples, output from step()
    """

    def on_step(state_reward_terminal_):
        on_step.states.append(state_reward_terminal_)

    on_step.states = list()

    env = holodeck.make("MazeWorld-FinishMazeSphere", show_viewport=False)

    finish.navigate(env, on_step)
    env.__on_exit__()

    return on_step.states


def pytest_generate_tests(metafunc):
    if "DefaultWorlds" not in holodeck.installed_packages():
        pytest.skip(
            msg="Skipping MazeWorld tests since DefaultWorlds is not "
            "installed",
            allow_module_level=True,
        )

    if "complete_mazeworld_states" in metafunc.fixturenames:
        metafunc.parametrize(
            "complete_mazeworld_states", ["mazeworld"], indirect=True
        )


states = None


@pytest.fixture
def complete_mazeworld_states(request):
    """Gets an environment for the scenario matching request.param. Creates
    the env
    or uses a cached one. Calls .reset() for you
    """
    global states
    if request.param == "mazeworld":
        if states is None:
            states = generate_mazeworld_walkthrough()

        return states


def env_with_config(config):
    binary_path = pm.get_binary_path_for_package("DefaultWorlds")
    return HolodeckEnvironment(
        scenario=config,
        binary_path=binary_path,
        show_viewport=False,
        uuid=str(uuid.uuid4()),
    )
