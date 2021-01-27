import uuid
import holodeck
import numpy as np
import pytest
from tests.utils.equality import almost_equal

turtle_config = {
    "name": "test_location_sensor",
    "world": "TestWorld",
    "main_agent": "turtle0",
    "agents": [
        {
            "agent_name": "turtle0",
            "agent_type": "TurtleAgent",
            "sensors": [
                {
                    "sensor_type": "RotationSensor",
                },
                {
                    "sensor_type": "LocationSensor",
                },
                {
                    "sensor_type": "VelocitySensor",
                },
            ],
            "control_scheme": 0,
            "location": [0.95, -1.75, 0.5],
        }
    ],
}

SHARED_SET_PHYSICS_STATE_ENV = None


@pytest.fixture(scope="module")
def set_physics_state_env():
    """test_rgb_camera_ticks_per_capture shares an environment with different
    instances of the same test
    """

    global SHARED_SET_PHYSICS_STATE_ENV

    if SHARED_SET_PHYSICS_STATE_ENV is None:

        binary_path = holodeck.packagemanager.get_binary_path_for_package(
            "DefaultWorlds"
        )

        SHARED_SET_PHYSICS_STATE_ENV = holodeck.environments.HolodeckEnvironment(
            scenario=turtle_config,
            binary_path=binary_path,
            show_viewport=False,
            uuid=str(uuid.uuid4()),
        )

    with SHARED_SET_PHYSICS_STATE_ENV:
        yield SHARED_SET_PHYSICS_STATE_ENV


def test_set_physics_state_loc_and_rot(set_physics_state_env):
    """Validates that the set_physics_state function correctly sets the location
    and rotation of the agent."""

    set_physics_state_env.reset()

    new_loc = np.array([0, 0, 100])
    new_rot = np.array([90, 10, 10])

    # This should change the location and the rotation of the agent.
    set_physics_state_env.agents["turtle0"].set_physics_state(
        new_loc, new_rot, [0, 0, 0], [0, 0, 0]
    )

    new_state = set_physics_state_env.tick()
    sensed_loc = new_state["LocationSensor"]
    sensed_rot = new_state["RotationSensor"]

    # Check to see if the newly sensed loc and rot are what we wanted to set them too.
    assert almost_equal(new_loc, sensed_loc), "The location was not set correctly!"
    assert almost_equal(new_rot, sensed_rot), "The rotation was not set correctly!"


def test_set_physics_state_vel(set_physics_state_env):
    """Validates that the set_physics_state function correctly sets the velocity of the agent."""

    set_physics_state_env.reset()

    new_vel = np.array([50, 0, 0])

    # This should change the velocity of the agent.
    set_physics_state_env.agents["turtle0"].set_physics_state(
        [0, 0, 0], [0, 0, 0], new_vel, [0, 0, 0]
    )

    new_state = set_physics_state_env.tick()
    sensed_vel = new_state["VelocitySensor"]

    # Check to see that the newly sensed vel is what we wanted to set it too.
    assert almost_equal(
        new_vel, sensed_vel, 0.0, 0.3
    ), "The velocity was not set correctly!"


def test_set_physics_state_ang_vel(set_physics_state_env):
    """Validates that the set_physics_state function correctly sets the angular velocity of
    the agent. There is no angular velocity sensor so it checks to see if the agent is spinning
    (rotation changes) after changing the angular velocity.

    """

    set_physics_state_env.reset()

    state = set_physics_state_env.tick()
    new_ang_vel = np.array([90, 0, 0])
    start_rot = state["RotationSensor"]

    # This should change the angular velocity of the agent.
    set_physics_state_env.agents["turtle0"].set_physics_state(
        [0, 0, 0], start_rot, [0, 0, 0], new_ang_vel
    )

    new_state = set_physics_state_env.tick()
    sensed_rot = new_state["RotationSensor"]

    # Check to see if the agent changes rotation, if angular velocity was set
    # correctly the rotation should change.
    assert not almost_equal(
        start_rot, sensed_rot
    ), "Angular Velocity was not set correctly!"


def test_set_physics_state_collision(set_physics_state_env):
    """Validates that the agent will collide with something and not finish teleporting when using
    the set_physics_state function if there is an obstacle in the way.
    The teleport function of the agent will do a sweep and thus stopping whenever an obstacle
    is encountered.

    """

    set_physics_state_env.reset()

    state = set_physics_state_env.tick()
    start_loc = state["LocationSensor"]
    new_loc = np.array([100, 0, 0])

    # This should not work, the agent should collide with wall and not teleport completely.
    set_physics_state_env.agents["turtle0"].set_physics_state(
        new_loc, [0, 0, 0], [0, 0, 0], [0, 0, 0]
    )

    new_state = set_physics_state_env.tick()
    sensed_loc = new_state["LocationSensor"]

    # Checking the collision by validating that it did not teleport to the desire location.
    assert not almost_equal(
        start_loc, sensed_loc
    ), "The location was not set correctly!"
    assert not almost_equal(new_loc, sensed_loc), "The location was not set correctly!"
