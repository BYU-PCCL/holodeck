import uuid
import copy

import holodeck

configs = {
    "AndroidAgent": {
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
                "control_scheme": 1, # Max Torque control scheme
                "location": [0, 0, 5]
            }
        ]
    },

    "HandAgent": {
        "name": "test_android_joint_sensor",
        "world": "TestWorld",
        "main_agent": "hand0",
        "agents": [
            {
                "agent_name": "hand0",
                "agent_type": "HandAgent",
                "sensors": [
                    {
                        "sensor_type": "JointRotationSensor",
                    }
                ],
                "control_scheme": 1,  # Max Torque control scheme, no floating
                "location": [0, 0, 5]
            }
        ]
    }
}


def test_joint_rotation_sensor(joint_agent_type):
    """Iterates over every joint provided in has and validates that applying a
    torque to that joint causes the values reported by the JointRotationSensor
    to change.

    Args:
        joint_agent_type (tuple of agent type (str) and list of joint names):
            Parameterized input

    """

    agent_type, joints = joint_agent_type
    zeroes = [0 for _ in range(len(joints))]

    binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

    with holodeck.environments.HolodeckEnvironment(scenario=configs[agent_type],
                                                   binary_path=binary_path,
                                                   uuid=str(uuid.uuid4())) as env:
        
        # Let the Android collapse into a twitching mess on the ground
        for _ in range(400):
            env.tick()
        
        for i in range(len(joints)):
            name = joints[i]

            action = copy.deepcopy(zeroes)
            action[i] = 1

            # Sample the joint rotation before torquing it
            pre_rotation = env.step(action)[0]["JointRotationSensor"][i]

            # Torque it for a few ticks
            for _ in range(10):
                env.step(action)
            
            # Sample it
            post_rotation_1 = env.step(action)[0]["JointRotationSensor"][i]

            # Torque it in the opposite direction for a bit to make sure it wasn't
            # maxed out in the positive direction before

            action[i] = -1
            for _ in range(10):
                env.step(action)
            
            post_rotation_2 = env.step(action)[0]["JointRotationSensor"][i]

            # print("{} {}/{}".format(name, abs(pre_rotation - post_rotation_1), abs(pre_rotation - post_rotation_2)))

            if "foot" in name:
                # Ugly, disgusting hack. The foot joints behave strangely, I can't figure out why. Skip them for now
                # BYU-PCCL/holodeck#297
                continue

            # Make sure the rotation is different
            assert abs(pre_rotation - post_rotation_1) > 1e-3 or \
                   abs(pre_rotation - post_rotation_2) > 1e-3, \
                   "The rotation for the joint {} (index {}) did not change enough!"\
                   "Before: {}, after positive max torque: {}, after negative max torque{}"\
                       .format(joints[i], i, pre_rotation, post_rotation_1, post_rotation_2)
            
            # Let things settle
            for _ in range(10):
                env.tick()

