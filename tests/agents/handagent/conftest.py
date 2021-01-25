import uuid
import holodeck
import pytest


base_handagent_config = {
    "name": "test_handagent",
    "world": "TestWorld",
    "main_agent": "hand0",
    "agents": [
        {
            "agent_name": "hand0",
            "agent_type": "HandAgent",
            "sensors": [
                {
                    "sensor_type": "LocationSensor",
                }
            ],
            "control_scheme": 2,
            "location": [0, 0, 1],
        }
    ],
}


def pytest_generate_tests(metafunc):
    if "env" in metafunc.fixturenames:
        metafunc.parametrize("env", [base_handagent_config], indirect=True)


SHARED_ENV = None


@pytest.fixture(scope="package", autouse=True)
def env_cleanup():
    global SHARED_ENV

    yield

    if callable(getattr(SHARED_ENV, "__on_exit__", None)):
        SHARED_ENV.__on_exit__()


@pytest.fixture
def env(request):
    global SHARED_ENV

    if SHARED_ENV is None:
        cfg = request.param
        binary_path = holodeck.packagemanager.get_binary_path_for_package(
            "DefaultWorlds"
        )
        SHARED_ENV = holodeck.environments.HolodeckEnvironment(
            scenario=cfg,
            binary_path=binary_path,
            show_viewport=False,
            uuid=str(uuid.uuid4()),
        )

    SHARED_ENV.reset()
    return SHARED_ENV
