import uuid
import holodeck
import numpy as np
from tests.utils.equality import almost_equal


base_cfg = {
    "name": "test_orientation_sensor",
    "world": "TestWorld",
    "main_agent": "sphere0",
    "agents": [
        {
            "agent_name": "sphere0",
            "agent_type": "SphereAgent",
            "sensors": [
                {
                    "sensor_type": "OrientationSensor",
                }
            ],
            "control_scheme": 0,
            "location": [0.95, -1.75, 0.5],
        }
    ],
}


def test_orientation_sensor_after_teleport():
    """Make sure that the orientation sensor correctly updates after using a teleport command to
    rotate the agent
    """
    binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

    with holodeck.environments.HolodeckEnvironment(
        scenario=base_cfg,
        binary_path=binary_path,
        show_viewport=False,
        uuid=str(uuid.uuid4()),
    ) as env:

        for _ in range(10):
            env.tick()

        loc = [123, 3740, 1030]
        rot_deg = np.array([0, 90, 0])
        env.agents["sphere0"].teleport(loc, rot_deg)
        state = env.tick()
        sensed_orientation = state["OrientationSensor"]

        accurate_or = np.zeros((3, 3))
        accurate_or[0, 2] = 1
        accurate_or[1, 1] = -1
        accurate_or[2, 0] = -1

        assert almost_equal(
            accurate_or, sensed_orientation
        ), "Expected orientation did not match the expected orientation!"
