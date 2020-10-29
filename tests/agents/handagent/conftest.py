import holodeck
import pytest
import uuid


base_handagent_config = {
    "name": "test_handagent",
    "world": "TestWorld",
    "main_agent": "hand0",
    "agents": [
        {
            "agent_name": "hand0",
            "agent_type": "HandAgent",
            "sensors": [{"sensor_type": "LocationSensor",}],
            "control_scheme": 2,
            "location": [0, 0, 1],
        }
    ],
}


def pytest_generate_tests(metafunc):
    if "env" in metafunc.fixturenames:
        metafunc.parametrize("env", [base_handagent_config], indirect=True)


shared_env = None


@pytest.fixture(scope="package", autouse=True)
def env_cleanup():
    global shared_env

    yield

    if callable(getattr(shared_env, "__on_exit__", None)):
        shared_env.__on_exit__()


@pytest.fixture
def env(request):
    global shared_env

    if shared_env is None:
        cfg = request.param
        binary_path = holodeck.packagemanager.get_binary_path_for_package(
            "DefaultWorlds"
        )
        shared_env = holodeck.environments.HolodeckEnvironment(
            scenario=cfg,
            binary_path=binary_path,
            show_viewport=False,
            uuid=str(uuid.uuid4()),
        )

    shared_env.reset()
    return shared_env
