"""
Verify that as the agent navigates through MazeWorld, that the reward increases throughout
"""

LENGTH = 55
REWARD_INTERVAL = 0.5
EXPECTED_REWARD = LENGTH / REWARD_INTERVAL


def test_reward_is_given(complete_mazeworld_states):
    """Make sure the total reward received for completing the maze is about what is expected
    (tests Interval)

    Args:
        complete_mazeworld_states:list of every state from finishing mazeworld

    """
    total_reward = 0.0
    for _, reward, _, _ in complete_mazeworld_states:
        total_reward += reward

    assert EXPECTED_REWARD * 0.90 <= total_reward <= EXPECTED_REWARD * 1.10, \
        "The reward received was {} but we expected within 10% of {}".format(total_reward, EXPECTED_REWARD)


def test_reward_valid_value(complete_mazeworld_states):
    """Makes sure that the reward returned is discrete

    Args:
        complete_mazeworld_states: list of every state from finishing mazeworld

    """
    for _, reward, _, _ in complete_mazeworld_states:
        assert reward == 0.0 or reward == 1.0, \
            "Expected a 1 or a 0, instead got a {}".format(reward)
