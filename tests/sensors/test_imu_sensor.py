"""Tests for the IMU sensor attached to the agent"""

import holodeck
import numpy as np
import pytest
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
            # binary_path=binary_path,
            show_viewport=False,
            start_world=False,
            # uuid=str(uuid.uuid4()),
        )

    with SHARED_IMU_SENSOR_ENV:
        yield SHARED_IMU_SENSOR_ENV


def test_imu_sensor_at_rest(imu_sensor_env):
    """Validates that the IMU sensor is correctly reading input when agent is at rest."""

    imu_sensor_env.reset()
    imu_sensor_env.tick()
    at_rest_sensor_reading = np.array([[0, 0, 9.8], [0, 0, 0]])

    new_state = imu_sensor_env.tick(20)
    sensed_imu_data = new_state["IMUSensor"]
    assert almost_equal(
        at_rest_sensor_reading, sensed_imu_data, 0.5, 0.5
    ), "The sensor did not read the agent at rest correctly!"


def test_imu_sensor_yaw(imu_sensor_env):
    """Validates that when a force is applied to rotate the UAV on the z-axis that
    the change in angular velocity on the z-axis was caught by the sensor"""

    imu_sensor_env.reset()
    imu_sensor_env.tick(20)
    orig_sensor_val = imu_sensor_env.tick()["IMUSensor"]
    assert almost_equal(orig_sensor_val[1][2], 0.0, 0.1, 0.1)

    imu_sensor_env.step([0, 0, 15, 100])
    imu_sensor_env.tick(25)
    new_sensor_reading = imu_sensor_env.tick()["IMUSensor"]
    assert new_sensor_reading[1][2] > orig_sensor_val[1][2]


def test_imu_sensor_roll(imu_sensor_env):
    """Validates that when a rotational force is applied on the x-axis of the UAV that the
    change in angular velocity on the x-axis and the change in linear acceleration on the
    y-axis were caught by the sensor."""

    imu_sensor_env.reset()
    imu_sensor_env.tick(20)
    orig_sensor_val = imu_sensor_env.tick()["IMUSensor"]
    assert almost_equal(orig_sensor_val[1][0], 0.0, 0.1, 0.1)

    imu_sensor_env.step([0, 15, 0, 100])
    imu_sensor_env.tick(25)
    new_sensor_reading = imu_sensor_env.tick()["IMUSensor"]
    assert abs(new_sensor_reading[1][0]) > abs(orig_sensor_val[1][0])
    assert abs(new_sensor_reading[0][1]) > abs(orig_sensor_val[0][1])


def test_imu_sensor_pitch(imu_sensor_env):
    """Validates that when a rotational force is applied on the y-axis of the UAV that the
    change in angular velocity on the y-axis and the change in linear acceleration on the
    x-axis were caught by the sensor."""

    imu_sensor_env.reset()
    imu_sensor_env.tick(20)
    orig_sensor_val = imu_sensor_env.tick()["IMUSensor"]
    assert almost_equal(orig_sensor_val[1][1], 0.0, 0.1, 0.1)

    imu_sensor_env.step([15, 0, 0, 100])
    imu_sensor_env.tick(25)
    new_sensor_reading = imu_sensor_env.tick()["IMUSensor"]
    assert abs(new_sensor_reading[1][1]) > abs(orig_sensor_val[1][1])
    assert abs(new_sensor_reading[0][0]) > abs(orig_sensor_val[0][0])
