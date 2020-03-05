import uuid
import copy
import numpy as np

import holodeck

configs = {
    "Uav": {
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
                "location": [0, 0, 9],
                "rotation": [0, 0, 0]
            }
        ]
    },

    "Android": {
        "name": "test_abuse_sensor",
        "world": "TestWorld",
        "main_agent": "android0",
        "agents": [
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
                "rotation": [0, 0, 0]
            }
        ]
    },

    "Turtle": {
        "name": "test_abuse_sensor",
        "world": "TestWorld",
        "main_agent": "turtle0",
        "agents": [
            {
                "agent_name": "turtle0",
                "agent_type": "TurtleAgent",
                "sensors": [
                    {
                        "sensor_type": "AbuseSensor",
                    }
                ],
                "control_scheme": 0,
                "location": [0, 0, 8],
                "rotation": [0, 0, 0]
            }
        ]
    },
}


def test_abuse_sensor(abuse_agent_type):
    """Iterates over every agent provided and tests if falling causes abuse
    and also runs relevant tests for the unique agent's abuse conditions.

    Args:
        abuse_agent_type (str):
            Parameterized input

    """

    # binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

    with holodeck.environments.HolodeckEnvironment(scenario=configs[abuse_agent_type],
                                                   # binary_path=binary_path,
                                                   show_viewport=True,
                                                   start_world=False,
                                                   # uuid=str(uuid.uuid4())) as env:
                                                   ) as env:
        abused = False
        for _ in range(100):
            if env.tick()["AbuseSensor"] == 1:
                abused = True
        assert abused

        if abuse_agent_type is "Uav":
            env.reset()
            env.agents["uav0"].teleport([0, 0, 1], [0, 180, 0])
            env.tick(20)
            assert env.tick()["AbuseSensor"] == 1
        elif abuse_agent_type is "Turtle":
            env.reset()
            env.agents["uav0"].teleport([0, 0, 1], [0, 180, 0])
            assert env.tick()["AbuseSensor"] == 1


