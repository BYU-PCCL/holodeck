import uuid
import pytest
import holodeck


def pytest_generate_tests(metafunc):
    """Iterate over every scenario"""
    if "resolution" in metafunc.fixturenames:
        metafunc.parametrize("resolution", [256, 512, 1024, 2048])
    elif "1024_env" in metafunc.fixturenames:
        metafunc.parametrize("env_1024", [1024], indirect=True)
    elif "ticks_per_capture" in metafunc.fixturenames:
        metafunc.parametrize("ticks_per_capture", [30, 15, 10, 5, 2])
    elif "joint_agent_type" in metafunc.fixturenames:
        metafunc.parametrize(
            "joint_agent_type",
            [("AndroidAgent", android_joints), ("HandAgent", handagent_joints)],
        )
    elif "abuse_world" in metafunc.fixturenames:
        metafunc.parametrize("abuse_world", ["abuse_world"], indirect=True)
    elif "rotation_env" in metafunc.fixturenames:
        metafunc.parametrize("rotation_env", ["rotation_env"], indirect=True)
    elif "agent_abuse_world" in metafunc.fixturenames:
        metafunc.parametrize(
            "agent_abuse_world", ["turtle0", "uav0", "android0"], indirect=True
        )


shared_1024_env = None
shared_rotation_env = None
shared_abuse_env = None


@pytest.fixture(scope="package", autouse=True)
def env_cleanup():
    global shared_1024_env, shared_rotation_env, shared_abuse_env

    yield

    shared_envs = [shared_1024_env, shared_rotation_env, shared_abuse_env]

    for env in filter(
        lambda env: callable(getattr(env, "__on_exit__", None)), shared_envs
    ):
        env.__on_exit__()


@pytest.fixture
def env_1024(request):
    """Shares the 1024x1024 configuration for use in two tests"""
    cfg = {
        "name": "test_viewport_capture",
        "world": "TestWorld",
        "main_agent": "sphere0",
        "agents": [
            {
                "agent_name": "sphere0",
                "agent_type": "SphereAgent",
                "sensors": [
                    {
                        "sensor_type": "ViewportCapture",
                        "configuration": {"CaptureWidth": 1024, "CaptureHeight": 1024},
                    }
                ],
                "control_scheme": 0,
                "location": [0.95, -1.75, 0.5],
            }
        ],
        "window_width": 1024,
        "window_height": 1024,
    }

    global shared_1024_env

    if shared_1024_env is None:
        binary_path = holodeck.packagemanager.get_binary_path_for_package(
            "DefaultWorlds"
        )
        shared_1024_env = holodeck.environments.HolodeckEnvironment(
            scenario=cfg,
            binary_path=binary_path,
            show_viewport=False,
            uuid=str(uuid.uuid4()),
        )

    shared_1024_env.reset()
    return shared_1024_env


def get_abuse_world():
    global shared_abuse_env
    if shared_abuse_env is None:
        binary_path = holodeck.packagemanager.get_binary_path_for_package(
            "DefaultWorlds"
        )
        shared_abuse_env = holodeck.environments.HolodeckEnvironment(
            scenario=abuse_config,
            binary_path=binary_path,
            show_viewport=False,
            uuid=str(uuid.uuid4()),
        )
    shared_abuse_env.reset()
    return shared_abuse_env


@pytest.fixture
def abuse_world(request):
    return get_abuse_world()


@pytest.fixture
def agent_abuse_world(request):
    env = get_abuse_world()
    return request.param, env


@pytest.fixture
def rotation_env(request):
    """Shares the RotationSensor configuration"""
    cfg = {
        "name": "test_rotation_sensor",
        "world": "TestWorld",
        "main_agent": "sphere0",
        "agents": [
            {
                "agent_name": "sphere0",
                "agent_type": "SphereAgent",
                "sensors": [{"sensor_type": "RGBCamera", "rotation": [0, -90, 0]}],
                "control_scheme": 0,
                "location": [0.95, -1.75, 0.5],
            }
        ],
    }

    global shared_rotation_env

    if shared_rotation_env is None:
        binary_path = holodeck.packagemanager.get_binary_path_for_package(
            "DefaultWorlds"
        )
        shared_rotation_env = holodeck.environments.HolodeckEnvironment(
            scenario=cfg,
            binary_path=binary_path,
            show_viewport=False,
            uuid=str(uuid.uuid4()),
        )

    shared_rotation_env.reset()
    return shared_rotation_env


abuse_config = {
    "name": "test_abuse_sensor",
    "world": "TestWorld",
    "main_agent": "uav0",
    "agents": [
        {
            "agent_name": "uav0",
            "agent_type": "UavAgent",
            "sensors": [
                {
                    "sensor_type": "AbuseSensor",
                }
            ],
            "control_scheme": 0,
            "location": [1.5, 0, 9],
            "rotation": [0, 0, 0],
        },
        {
            "agent_name": "android0",
            "agent_type": "AndroidAgent",
            "sensors": [
                {
                    "sensor_type": "AbuseSensor",
                }
            ],
            "control_scheme": 0,
            "location": [0, 0, 10],
            "rotation": [0, 0, 0],
        },
        {
            "agent_name": "turtle0",
            "agent_type": "TurtleAgent",
            "sensors": [
                {
                    "sensor_type": "AbuseSensor",
                }
            ],
            "control_scheme": 0,
            "location": [2, 1.5, 8],
            "rotation": [0, 0, 0],
        },
    ],
}

android_joints = [
    "head_swing1",
    "head_swing2",
    "head_twist",
    "neck_01_swing1",
    "neck_01_swing2",
    "neck_01_twist",
    "spine_02_swing1",
    "spine_02_swing2",
    "spine_02_twist",
    "spine_01_swing1",
    "spine_01_swing2",
    "spine_01_twist",
    "upperarm_l_swing1",
    "upperarm_l_swing2",
    "upperarm_l_twist",
    "lowerarm_l_swing1",
    "lowerarm_l_swing2",
    "lowerarm_l_twist",
    "hand_l_swing1",
    "hand_l_swing2",
    "hand_l_twist",
    "upperarm_r_swing1",
    "upperarm_r_swing2",
    "upperarm_r_twist",
    "lowerarm_r_swing1",
    "lowerarm_r_swing2",
    "lowerarm_r_twist",
    "hand_r_swing1",
    "hand_r_swing2",
    "hand_r_twist",
    "thigh_l_swing1",
    "thigh_l_swing2",
    "thigh_l_twist",
    "calf_l_swing1",
    "calf_l_swing2",
    "calf_l_twist",
    "foot_l_swing1",
    "foot_l_swing2",
    "foot_l_twist",
    "ball_l_swing1",
    "ball_l_swing2",
    "ball_l_twist",
    "thigh_r_swing1",
    "thigh_r_swing2",
    "thigh_r_twist",
    "calf_r_swing1",
    "calf_r_swing2",
    "calf_r_twist",
    "foot_r_swing1",
    "foot_r_swing2",
    "foot_r_twist",
    "ball_r_swing1",
    "ball_r_swing2",
    "ball_r_twist",
    "thumb_01_l_swing1",
    "thumb_01_l_swing2",
    "index_01_l_swing1",
    "index_01_l_swing2",
    "middle_01_l_swing1",
    "middle_01_l_swing2",
    "ring_01_l_swing1",
    "ring_01_l_swing2",
    "pinky_01_l_swing1",
    "pinky_01_l_swing2",
    "thumb_01_r_swing1",
    "thumb_01_r_swing2",
    "index_01_r_swing1",
    "index_01_r_swing2",
    "middle_01_r_swing1",
    "middle_01_r_swing2",
    "ring_01_r_swing1",
    "ring_01_r_swing2",
    "pinky_01_r_swing1",
    "pinky_01_r_swing2",
    "thumb_02_l_swing1",
    "index_02_l_swing1",
    "middle_02_l_swing1",
    "ring_02_l_swing1",
    "pinky_02_l_swing1",
    "thumb_02_r_swing1",
    "index_02_r_swing1",
    "middle_02_r_swing1",
    "ring_02_r_swing1",
    "pinky_02_r_swing1",
    "thumb_03_l_swing1",
    "index_03_l_swing1",
    "middle_03_l_swing1",
    "ring_03_l_swing1",
    "pinky_03_l_swing1",
    "thumb_03_r_swing1",
    "index_03_r_swing1",
    "middle_03_r_swing1",
    "ring_03_r_swing1",
    "pinky_03_r_swing1",
]


handagent_joints = [
    "hand_r_swing1",
    "hand_r_swing2",
    "hand_r_twist",
    "thumb_01_r_swing1",
    "thumb_01_r_swing2",
    "index_01_r_swing1",
    "index_01_r_swing2",
    "middle_01_r_swing1",
    "middle_01_r_swing2",
    "ring_01_r_swing1",
    "ring_01_r_swing2",
    "pinky_01_r_swing1",
    "pinky_01_r_swing2",
    "thumb_02_r_swing1",
    "index_02_r_swing1",
    "middle_02_r_swing1",
    "ring_02_r_swing1",
    "pinky_02_r_swing1",
    "thumb_03_r_swing1",
    "index_03_r_swing1",
    "middle_03_r_swing1",
    "ring_03_r_swing1",
    "pinky_03_r_swing1",
]
