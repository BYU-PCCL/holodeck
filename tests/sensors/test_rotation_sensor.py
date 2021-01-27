import uuid
import holodeck
import numpy as np
from tests.utils.equality import almost_equal


base_cfg = {
    "name": "test_rotation_sensor",
    "world": "TestWorld",
    "main_agent": "sphere0",
    "agents": [
        {
            "agent_name": "sphere0",
            "agent_type": "SphereAgent",
            "sensors": [
                {
                    "sensor_type": "RotationSensor",
                }
            ],
            "control_scheme": 0,
            "location": [0.95, -1.75, 0.5],
        }
    ],
}


def test_rotation_sensor_after_teleport():
    """Make sure that the rotation sensor correctly updates after using a teleport command to
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
        rotation = env.tick()["RotationSensor"]

        assert almost_equal(
            rot_deg, rotation
        ), "The agent rotated in an unexpected manner!"
