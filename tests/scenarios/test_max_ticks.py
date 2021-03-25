import holodeck
import pytest
import uuid

from holodeck.exceptions import HolodeckException

max_tick_config = {
    "name": "test",
    "world": "TestWorld",
    "main_agent": "uav0",
    "agents": [
        {
            "agent_name": "agent0",
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

SHARED_MAX_TICK_ENV = None


@pytest.fixture(scope="module")
def set_max_tick_env():
    """shares an environment with different
    instances of the same test
    """

    global SHARED_MAX_TICK_ENV

    if SHARED_MAX_TICK_ENV is None:

        binary_path = holodeck.packagemanager.get_binary_path_for_package(
            "DefaultWorlds"
        )

        SHARED_MAX_TICK_ENV = holodeck.environments.HolodeckEnvironment(
            scenario=max_tick_config,
            binary_path=binary_path,
            show_viewport=False,
            uuid=str(uuid.uuid4()),
            max_ticks=10,
        )

    with SHARED_MAX_TICK_ENV:
        yield SHARED_MAX_TICK_ENV


def test_max_ticks(set_max_tick_env):
    """Validates that the instance stops and throws a HolodeckException when
    the max number of ticks is reached."""

    try:
        command = [0, 0, 0, 2000]
        set_max_tick_env.act("agent0", command)
        for _ in range(10):
            set_max_tick_env.tick(1)

        assert False, "No HolodeckException was thrown!"
    except HolodeckException:
        assert True


def test_max_ticks_reset(set_max_tick_env):
    """Validates that the reset function does not hit the max_tick threshold
    and resets the environment correctly."""

    set_max_tick_env.reset()

    try:
        command = [0, 0, 0, 2000]
        set_max_tick_env.act("agent0", command)
        for _ in range(9):
            set_max_tick_env.tick(1)

        set_max_tick_env.reset()

        for _ in range(9):
            set_max_tick_env.tick(1)

        assert True
    except HolodeckException:
        assert False, "A HolodeckException was thrown when using reset()!"


def test_max_ticks_tick(set_max_tick_env):
    """Validates that tick() will hit the max_tick threshold"""

    set_max_tick_env.reset()

    try:
        command = [0, 0, 0, 2000]
        set_max_tick_env.act("agent0", command)
        for _ in range(10):
            set_max_tick_env.tick(1)

        assert False, "No HolodeckException was thrown when using tick()!"
    except HolodeckException:
        assert True


def test_max_ticks_step(set_max_tick_env):
    """Validates that step() will hit the max_tick threshold"""

    set_max_tick_env.reset()

    try:
        command = [0, 0, 0, 2000]
        set_max_tick_env.act("agent0", command)
        for _ in range(10):
            set_max_tick_env.step(1)
        assert False, "No HolodeckException was thrown when using step()!"
    except HolodeckException:
        assert True


def test_no_max_ticks():
    """Validates that not setting max_tick will not throw a HolodeckException"""

    binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")
    no_max_tick_env = holodeck.environments.HolodeckEnvironment(
        scenario=max_tick_config,
        binary_path=binary_path,
        show_viewport=False,
        uuid=str(uuid.uuid4()),
    )

    try:
        command = [0, 0, 0, 2000]
        no_max_tick_env.act("agent0", command)
        for _ in range(50):
            no_max_tick_env.tick(1)
        assert True
    except HolodeckException:
        assert False, "A HolodeckException was thrown with no max_tick set!"
