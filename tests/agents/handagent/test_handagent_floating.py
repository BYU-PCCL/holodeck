"""
Validates the floating portion of the HAND_AGENT_MAX_TORQUES_FLOAT / UHandAgentMaxTorqueFloat
control scheme.

"""


def validate_movement(env, amount_to_move, expected_movement):
    action = [0 for _ in range(26)]

    last_location = env.tick()["LocationSensor"]

    # X Axis
    action[23] = amount_to_move
    env.step(action)
    new_location = env.tick()["LocationSensor"]
    d_x = abs(new_location[0] - last_location[0])

    assert abs(d_x - expected_movement) < 0.001

    last_location = new_location

    action[23] = 0

    # Y axis
    action[24] = amount_to_move
    env.step(action)
    new_location = env.tick()["LocationSensor"]
    d_y = abs(new_location[1] - last_location[1])

    assert (d_y - expected_movement) < 0.001

    last_location = new_location

    action[24] = 0

    # Z Axis
    action[25] = amount_to_move
    env.step(action)
    new_location = env.tick()["LocationSensor"]
    d_z = abs(new_location[2] - last_location[2])

    assert abs(d_z - expected_movement) < 0.001


def test_can_float(env):
    """Basic test to make sure the floating control scheme is working.
    Moves the HandAgent around and uses the
    LocationSensor to validate that it moved the expected amount

    """
    validate_movement(env, 0.25, 0.25)


def test_movement_capped(env):
    """The HandAgent should only be able to float a maximum of 0.5 meters in any direction.
    Try and move it more than that and verify that it was capped.

    """
    validate_movement(env, 2, 0.5)
