"""Tests for the IMU sensor attached to the agent"""

import uuid
import holodeck
import numpy as np
import pytest
import pprint
from tests.utils.equality import almost_equal

turtle_config = {
    "name": "test_imu_sensor",
    "world": "TestWorld",
    "main_agent": "uav0",
    "agents": [
        {
            "agent_name": "uav0",
            "agent_type": "UavAgent",
            "sensors": [
                {
                    "sensor_type": "IMUSensor",
                },
            ],
            "control_scheme": 0,
            "location": [0, 0, 0.5],
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
            #binary_path=binary_path,
            show_viewport=False,
            start_world=False,
            #uuid=str(uuid.uuid4()),
        )
    
    with SHARED_IMU_SENSOR_ENV:
        yield SHARED_IMU_SENSOR_ENV


def test_imu_sensor_at_rest(imu_sensor_env):
    """Validates that the IMU sensor is correctly reading input when agent is at rest."""

    imu_sensor_env.reset()

    imu_sensor_env.tick()
    at_rest_sensor_reading = np.array([[0, 0, 9.8], [0, 0, 0]])

    new_state = imu_sensor_env.tick()
    sensed_imu_data = new_state["IMUSensor"]

    assert almost_equal(at_rest_sensor_reading, sensed_imu_data), "The sensor did not read the agent at rest correctly!py"


def test_imu_sensor_after_applied_force(imu_sensor_env):
    """Validates that the sensor reads new data when a forces is applied."""
    imu_sensor_env.reset()

    imu_sensor_env.tick()
    orig_sensor_reading = imu_sensor_env.tick()["IMUSensor"]

    imu_sensor_env.step([0, 0, 15, 100])

    imu_sensor_env.tick(25)

    new_sensor_reading = imu_sensor_env.tick()["IMUSensor"]
    
    assert not almost_equal(orig_sensor_reading, new_sensor_reading)
