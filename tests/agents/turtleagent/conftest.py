import holodeck
import uuid
from . import finish
import pytest


def generate_turtle_walkthrough():
    """Runs through the maze in TestWorld and records state at every tic, so that tests
    can analyze the results without having to run through the maze multiple times

    Returns: list of 4tuples, output from step()
    """

    def on_step(state_reward_terminal_):
        on_step.states.append(state_reward_terminal_)

    on_step.states = list()

    binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

    with holodeck.environments.HolodeckEnvironment(
        scenario=cfg,
        binary_path=binary_path,
        show_viewport=False,
        uuid=str(uuid.uuid4()),
    ) as env:

        finish.navigate(env, on_step)

    return on_step.states


def pytest_generate_tests(metafunc):
    if "complete_mazeworld_states" in metafunc.fixturenames:
        metafunc.parametrize("complete_mazeworld_states", ["mazeworld"], indirect=True)


states = None


@pytest.fixture
def complete_mazeworld_states(request):
    """Gets an environment for the scenario matching request.param. Creates the env
    or uses a cached one. Calls .reset() for you
    """
    global states
    if request.param == "mazeworld":
        if states is None:
            states = generate_turtle_walkthrough()

        return states


cfg = {
    "name": "test_turtleagent_movement",
    "world": "TestWorld",
    "main_agent": "turtle0",
    "agents": [
        {
            "agent_name": "turtle0",
            "agent_type": "TurtleAgent",
            "main_agent": True,
            "control_scheme": 0,
            "sensors": [
                {"sensor_type": "RotationSensor"},
                {"sensor_type": "LocationSensor"},
                {
                    "sensor_type": "DistanceTask",
                    "configuration": {
                        "GoalActor": "teapot",
                        "Interval": 0.5,
                        "GoalDistance": 2,
                        "MaximizeDistance": False,
                    },
                },
            ],
            "location": [-6, 29.8, 5.8],
        }
    ],
}
