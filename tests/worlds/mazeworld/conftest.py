from . import finish
import holodeck
import pytest

def generate_mazeworld_walkthrough():
    """Runs through Mazeworld and records state at every tic, so that tests can analyze the results
    without having to run through the maze multiple times

    Returns: list of 4tuples, output from step()
    """

    def on_step(state_reward_terminal_):
        on_step.states.append(state_reward_terminal_)

    on_step.states = list()

    env = holodeck.make("MazeWorld-FinishMazeSphere", show_viewport=False)

    finish.navigate(env, on_step)
    env.__on_exit__()

    return on_step.states


def pytest_generate_tests(metafunc):
    if 'complete_mazeworld_states' in metafunc.fixturenames:
        metafunc.parametrize('complete_mazeworld_states', ["mazeworld"], indirect=True)

states = None

@pytest.fixture
def complete_mazeworld_states(request):
    """Gets an environment for the scenario matching request.param. Creates the env
    or uses a cached one. Calls .reset() for you
    """
    global states
    if request.param == "mazeworld":
        if states is None:
            states = generate_mazeworld_walkthrough()

        return states
