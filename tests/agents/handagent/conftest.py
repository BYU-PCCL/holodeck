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
            "sensors": [
                {
                    "sensor_type": "LocationSensor",
                }
            ],
            "control_scheme": 2,
            "location": [0, 0, 1]
        }
    ]
}


def pytest_generate_tests(metafunc):
    if 'shared_env' in metafunc.fixturenames:
        metafunc.parametrize('shared_env', [base_handagent_config], indirect=True)


@pytest.fixture(scope="package")
def shared_env(request):
    cfg = request.param
    binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

    with holodeck.environments.HolodeckEnvironment(scenario=cfg,
                                                   binary_path=binary_path,
                                                   show_viewport=False,
                                                   uuid=str(uuid.uuid4())) as env:
        # resetting is handled by `env` and cleanup happens immediately after exiting
        # the module
        yield env


@pytest.fixture
def env(shared_env):
    shared_env.reset()
    return shared_env
