import holodeck
import pytest
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
def max_tick_env():
    """shares an environment with different
    instances of the same test
    """

    global shared_max_tick_env

    if shared_max_tick_env is None:

        binary_path = holodeck.packagemanager.get_binary_path_for_package(
            "DefaultWorlds"
        )

        shared_max_tick_env = holodeck.environments.HolodeckEnvironment(
            scenario=max_height_config,
            binary_path=binary_path,
            show_viewport=False,
            uuid=str(uuid.uuid4()),
        )

    with shared_max_tick_env:
        yield shared_max_tick_env

# Test:
# No max_ticks
def test_no_max_ticks(shared_max_tick_env){

}
# Set max max_ticks, using various tick functions
# - tick
# - step
# - act?
# - reset?