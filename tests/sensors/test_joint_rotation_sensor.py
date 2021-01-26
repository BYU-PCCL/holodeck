import uuid
import copy
import numpy as np

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
                "control_scheme": 1,  # Max Torque control scheme
                "location": [0, 0, 1],
                "rotation": [90, 0, 0],
            }
        ],
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
                "location": [0, 0, 5],
            }
        ],
    },
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

    with holodeck.environments.HolodeckEnvironment(
        scenario=configs[agent_type],
        binary_path=binary_path,
        show_viewport=False,
        uuid=str(uuid.uuid4()),
    ) as env:

        # Let the Android collapse into a twitching mess on the ground
        for _ in range(200):
            env.tick()

        failures = list()

        num_joints = len(joints)
        num_steps = 10
        for i in range(num_joints):

            torque_backwards = np.zeros(num_joints)
            torque_backwards[i] = -1
            torque_forwards = np.zeros(num_joints)
            torque_forwards[i] = 1

            # Torque it in the opposite direction for a bit to make sure it wasn't
            # maxed out in the positive direction before
            for _ in range(num_steps):
                env.step(torque_backwards)

            # Sample the joint rotation before torquing it
            pre_rotation = env.step(torque_forwards)[0]["JointRotationSensor"][i]

            # Torque it for a few ticks
            for _ in range(num_steps):
                env.step(torque_forwards)

            # Sample it
            post_rotation_forward = env.step(torque_forwards)[0]["JointRotationSensor"][
                i
            ]

            # The joint should be at its maximum forward position. Now we should be able
            # to torque it backwards and get a different value.
            for _ in range(num_steps):
                env.step(torque_backwards)

            post_rotation_backward = env.step(torque_backwards)[0][
                "JointRotationSensor"
            ][i]

            # print("{} {}/{}".format(name, abs(pre_rotation - post_rotation_forward),
            # abs(pre_rotation - post_rotation_backward)))

            # if "foot" in name or name == "head_swing1":
            #    # Ugly, disgusting hack. Some joints behave strangely, I can't figure out why.
            #    # Skip them for now
            #    # BYU-PCCL/holodeck#297
            #    continue

            # Make sure the rotation is different

            # if there is a large-ish difference between after max pos torque and max neg
            # torque, we're fine
            if abs(abs(post_rotation_forward) - abs(post_rotation_backward)) < 1e-3:
                if abs(abs(pre_rotation) - abs(post_rotation_forward)) < 1e-3:
                    failures.append(
                        "{}: After applying positive max torque, before: {}, after: {}".format(
                            joints[i], pre_rotation, post_rotation_forward
                        )
                    )

                if abs(abs(pre_rotation) - abs(post_rotation_backward)) < 1e-3:
                    failures.append(
                        "{}: After applying negative max torque, before: {}, after: {}".format(
                            joints[i], pre_rotation, post_rotation_backward
                        )
                    )

            # Let things settle
            for _ in range(num_steps):
                env.tick()

        if failures:
            print("\nGot {} failures...".format(len(failures)))
            for fail in failures:
                print(fail)

        assert len(failures) == 0
