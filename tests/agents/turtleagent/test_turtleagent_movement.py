import pytest
import holodeck


def test_turtleagent_falling(complete_mazeworld_states):
    """Makes sure that the TurtleBot is subject to gravity.

    Check that the z coordinates are smaller after 100 ticks
    """

    # Test to make sure the turtleagent falls
    s_1 = complete_mazeworld_states[0]
    s_2 = complete_mazeworld_states[100]

    assert (
        s_1[0]["LocationSensor"][2] - s_2[0]["LocationSensor"][2] >= 0.1
    ), "The TurtleAgent didn't seem to fall!"


@pytest.mark.skipif(
    holodeck.util.get_os_key() == "Linux",
    reason="TurtleAgent movement differs on Linux. See #336",
)
def test_turtleagent_movement(complete_mazeworld_states):
    """Validates that the TurtleAgent can climb slight inclines & moves as expected.

    Check to make sure the DistanceTask gives terminal. If it did, it means that
    the TurtleAgent made it close enough to the teapot.

    """

    for s in complete_mazeworld_states:
        _, _, terminal, _ = s

        if terminal:
            return

    assert False, "The TurtleAgent did not make it to the end of the maze!"
