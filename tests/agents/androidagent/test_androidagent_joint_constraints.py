import uuid
from holodeck import environments, packagemanager

config = {
    "name": "test_android_joint_sensor",
    "world": "TestWorld",
    "main_agent": "android0",
    "agents": [
        {
            "agent_name": "android0",
            "agent_type": "AndroidAgent",
            "sensors": [
                {
                    "sensor_type": "JointRotationSensor",
                }
            ],
            "control_scheme": 1,  # Max Torque control scheme
            "location": [0, 0, 5],
        }
    ],
}

known_constraints = {
    "upperarm_r": {"swing2_limit": 68.0275, "swing1_limit": 90, "twist_limit": 50},
    "spine_01": {"swing2_limit": 10, "swing1_limit": 35, "twist_limit": 20},
    "ball_l": {"swing2_limit": 10, "swing1_limit": 10, "twist_limit": 15},
    "spine_02": {"swing2_limit": 15, "swing1_limit": 5, "twist_limit": 25},
    "index_02_l": {"swing2_limit": 0, "swing1_limit": 60, "twist_limit": 2},
    "pinky_02_r": {"swing2_limit": 0, "swing1_limit": 60, "twist_limit": 2},
}


def test_android_constraints():
    binary_path = packagemanager.get_binary_path_for_package("DefaultWorlds")

    with environments.HolodeckEnvironment(
        scenario=config,
        binary_path=binary_path,
        show_viewport=False,
        uuid=str(uuid.uuid4()),
    ) as env:
        not_exist = env.get_joint_constraints("android0", "does_not_exist")
        assert not_exist is None

        for joint_name in known_constraints.keys():
            constraint = env.get_joint_constraints("android0", joint_name)
            assert constraint == known_constraints[joint_name]
