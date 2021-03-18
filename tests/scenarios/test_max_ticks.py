import holodeck
from holodeck.exceptions import HolodeckException
import pytest
import sys
import uuid

max_tick_config = {
    "name": "test",
    "world": "TestWorld",
    "main_agent": "uav0",
    "agents": [
        {
            "agent_name": "uav0",
            "agent_type": "UavAgent",
            "sensors": [
                {
                    "sensor_type": "LocationSensor",
                },
                {"sensor_type": "VelocitySensor"},
                {"sensor_type": "RGBCamera"},
            ],
            "control_scheme": 0,
            "location": [0, 0, 5],
        }
    ],
}

shared_max_tick_env = None


@pytest.fixture(scope="module")
def set_max_tick_env():
    """shares an environment with different
    instances of the same test
    """

    global shared_max_tick_env

    if shared_max_tick_env is None:

        binary_path = holodeck.packagemanager.get_binary_path_for_package(
            "DefaultWorlds"
        )

        shared_max_tick_env = holodeck.environments.HolodeckEnvironment(
            scenario=max_tick_config,
            binary_path=binary_path,
            show_viewport=False,
            uuid=str(uuid.uuid4()),
            max_ticks=10,
        )

    with shared_max_tick_env:
        yield shared_max_tick_env


def test_max_ticks(shared_max_tick_env):
    try:
        for _ in range(9):
            command = [0, 0, 0, 2000]
            shared_max_tick_env.act("agent0", command)
            shared_max_tick_env.tick(1)

        shared_max_tick_env.reset()
        assert True
    except HolodeckException:
        assert False


def test_max_ticks_tick(shared_max_tick_env):
    shared_max_tick_env.reset()
    try:
        for _ in range(10):
            command = [0, 0, 0, 2000]
            shared_max_tick_env.act("agent0", command)
            shared_max_tick_env.tick(1)
        assert False
    except HolodeckException:
        assert True


def test_max_ticks_step(shared_max_tick_env):
    shared_max_tick_env.reset()
    try:
        for _ in range(10):
            command = [0, 0, 0, 2000]
            shared_max_tick_env.act("agent0", command)
            shared_max_tick_env.step(1)
        assert False
    except HolodeckException:
        assert True


def test_no_max_ticks(shared_max_tick_env):

    shared_max_tick_env.reset()
    shared_max_tick_env.max_ticks = sys.maxsize
    try:
        for _ in range(10):
            command = [0, 0, 0, 2000]
            shared_max_tick_env.act("agent0", command)
            shared_max_tick_env.tick(1)
        assert False
    except HolodeckException:
        assert True