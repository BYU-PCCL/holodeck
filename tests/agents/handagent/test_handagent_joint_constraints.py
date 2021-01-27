import uuid
from holodeck import environments, packagemanager

config = {
    "name": "test_hand_agent_joint_sensor",
    "world": "TestWorld",
    "main_agent": "hand_agent0",
    "agents": [
        {
            "agent_name": "hand_agent0",
            "agent_type": "HandAgent",
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
    "thumb_01_r": {"swing2_limit": 35.0, "swing1_limit": 30.0, "twist_limit": 2.0},
    "pinky_01_r": {"swing2_limit": 45.0, "swing1_limit": 10, "twist_limit": 2.0},
    "ring_01_r": {"swing2_limit": 45.0, "swing1_limit": 10.0, "twist_limit": 2.0},
    "pinky_02_r": {"swing2_limit": 60.0, "swing1_limit": 0.0, "twist_limit": 2.0},
    "middle_03_r": {"swing2_limit": 40.0, "swing1_limit": 0.0, "twist_limit": 0.0},
    "hand_r": {"swing2_limit": 170.0, "swing1_limit": 170.0, "twist_limit": 170.0},
}


def test_hand_agent_joint_constraints():
    binary_path = packagemanager.get_binary_path_for_package("DefaultWorlds")

    with environments.HolodeckEnvironment(
        scenario=config,
        binary_path=binary_path,
        show_viewport=False,
        uuid=str(uuid.uuid4()),
    ) as env:
        not_exist = env.get_joint_constraints("hand_agent0", "does_not_exist")
        assert not_exist is None

        for joint_name in known_constraints.keys():
            constraint = env.get_joint_constraints("hand_agent0", joint_name)
            assert constraint == known_constraints[joint_name]
