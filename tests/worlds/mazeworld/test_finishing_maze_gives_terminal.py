"""
Make sure that when completing MazeWorld, if the agent navigates to the end, the
state is marked as terminal at some point.

"""
import holodeck


def test_finishing_maze_gives_terminal(complete_mazeworld_states):
    for _, _, terminal, _ in complete_mazeworld_states:
        if terminal:
            return

    assert False, "No terminal state found"
