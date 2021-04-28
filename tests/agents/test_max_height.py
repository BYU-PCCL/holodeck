import holodeck
import pytest
import uuid

from tests.utils.equality import almost_equal

height_config = {
    "name": "test_max_height",
    "world": "TestWorld",
    "main_agent": "uav0",
    "agents": [
        {
            "agent_name": "uav0",
            "agent_type": "UavAgent",
            "sensors": [
                {
                    "sensor_type": "LocationSensor",
                }
            ],
            "control_scheme": 0,
            "location": [0, 0, 2],
            "max_height": 3,
        }
    ],
}

no_height_config = {
    "name": "test_max_height",
    "world": "TestWorld",
    "main_agent": "uav0",
    "agents": [
        {
            "agent_name": "uav0",
            "agent_type": "UavAgent",
            "sensors": [
                {
                    "sensor_type": "LocationSensor",
                }
            ],
            "control_scheme": 0,
            "location": [0, 0, 2],
        }
    ],
}

binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

shared_max_height_env = None


@pytest.fixture(scope="module")
def max_height_env():
    """shares an environment with different
    instances of the same test
    """

    global shared_max_height_env

    if shared_max_height_env is None:

        binary_path = holodeck.packagemanager.get_binary_path_for_package(
            "DefaultWorlds"
        )

        shared_max_height_env = holodeck.environments.HolodeckEnvironment(
            scenario=height_config,
            binary_path=binary_path,
            show_viewport=False,
            uuid=str(uuid.uuid4()),
        )

    with shared_max_height_env:
        yield shared_max_height_env


def test_max_height_set(max_height_env):
    """Make sure that the agent doesn't travel higher than the set max height."""
    max_height_env.reset()

    max_height = height_config["agents"][0]["max_height"]

    command = [0, 0, 0, 1000]
    max_height_env.act("uav0", command)
    state = max_height_env.tick(50)

    current_location = state["LocationSensor"]

    assert (current_location[2] < max_height) or almost_equal(
        current_location[2], max_height
    ), "UAV ignored max height that was set!"


def test_stuck_at_max_height(max_height_env):
    """Make sure that the agent doesn't get stuck at the max height after it is first stopped."""
    max_height_env.reset()

    max_height = height_config["agents"][0]["max_height"]

    command = [0, 0, 0, 100]
    max_height_env.act("uav0", command)
    state = max_height_env.tick(50)

    command = [0, 0, 0, 0]
    max_height_env.act("uav0", command)
    state = max_height_env.tick(50)

    current_location = state["LocationSensor"]

    assert (current_location[2] < max_height) and not (
        almost_equal(current_location[2], max_height)
    ), "UAV did not fall from max height!"


def test_no_max_height_set():
    """Make sure that not setting a max height will default to not applying a max height."""

    with holodeck.environments.HolodeckEnvironment(
        scenario=no_height_config,
        binary_path=binary_path,
        show_viewport=False,
        uuid=str(uuid.uuid4()),
    ) as env:

        command = [0, 0, 0, 1000]
        state = env.tick()
        old_location = state["LocationSensor"]

        env.act("uav0", command)
        state = env.tick(50)
        current_location = state["LocationSensor"]

        assert (old_location[2] < current_location[2]) and not (
            almost_equal(old_location[2], current_location[2])
        ), "UAV stopped moving up despite no set max height!"
