"""Tests for the IMU sensor attached to the agent"""

import uuid
import holodeck
import numpy as np
import pytest
from tests.utils.equality import almost_equal

turtle_config = {
    "name": "test_imu_sensor",
    "world": "TestWorld",
    "main_agent": "turtle0",
    "agents": [
        {
            "agent_name": "turtle0",
            "agent_type": "TurtleAgent",
            "sensors": [
                {
                    "sensor_type": "IMUSensor",
                },
            ],
            "control_scheme": 0,
            "location": [0, 0, 0.1],
        }
    ],
}

SHARED_IMU_SENSOR_ENV = None

@pytest.fixture(scope="module")
def imu_sensor_env():
    """Sets up an environment with different instances of the same test"""
    
    global SHARED_IMU_SENSOR_ENV

    if SHARED_IMU_SENSOR_ENV is None:

        binary_path = holodeck.packagemanager.get_binary_path_for_package(
            "DefaultWorlds"
        )

        SHARED_IMU_SENSOR_ENV = holodeck.environments.HolodeckEnvironment(
            scenario=turtle_config,
            binary_path=binary_path,
            show_viewport=False,
            uuid=str(uuid.uuid4()),
        )
    
    with SHARED_IMU_SENSOR_ENV:
        yield SHARED_IMU_SENSOR_ENV


def test_imu_sensor_at_rest(imu_sensor_env):
    """Validates that the IMU sensor is correctly reading input when agent is at rest."""

    imu_sensor_env.reset()


    at_rest_sensor_reading = np.array([[0, 0, 9.8], [0, 0, 0]])

    new_state = imu_sensor_env.tick()
    sensed_imu_data = new_state["IMUSensor"]
    print(sensed_imu_data)

    assert almost_equal(at_rest_sensor_reading, sensed_imu_data), "The sensor did not read the agent at rest correctly!py"


def test_imu_sensor_after_applied_force(imu_sensor_env):
    imu_sensor_env.reset()

    imu_sensor_env.tick(10)
    orig_sensor_reading = imu_sensor_env.tick()["IMUSensor"]

    imu_sensor_env.step([10, 0])
    new_sensor_reading = imu_sensor_env.tick()["IMUSensor"]
    
    assert not almost_equal(orig_sensor_reading, new_sensor_reading)

