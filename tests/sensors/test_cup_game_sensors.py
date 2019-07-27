import holodeck
import uuid

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
                        "sensor_type": "CupGameTask",
                        "configuration": {
                            "Speed": 3,
                            "NumShuffles": 3,
                            "Seed": 0
                        }
                    },
                    {
                        "sensor_type": "BallLocationSensor"
                    }
                ],
                "control_scheme": 0,
                "location": [-.4, -.9, 1.8],
                "rotation": [0, 0, 90]
            }
        ],
        "window_width": 1024,
        "window_height": 1024
    }


def test_cup_game_sensors():
    """Drop the UAV, make sure the z velocity is increasingly negative as it falls.
    Make sure it zeros out after it hits the ground, and then goes positive on takeoff
    """

    # binary_path = holodeck.packagemanager.get_binary_path_for_package("Dexterity")

    with holodeck.environments.HolodeckEnvironment(scenario=cfg,
                                                   # binary_path=binary_path,
                                                   # show_viewport=False,
                                                   start_world=False,
                                                   uuid=str(uuid.uuid4())) as env:
        env.reset()
        for _ in range(500):
            _ = env.tick()
        env.teleport("sphere0", [-.4, -.9, 1.8], [0, 0, 90])
        state = None
        reward = 0
        for _ in range(30):
            state, reward, terminal, _ = env.step([0])
        assert reward == 50 and state["BallLocationSensor"] == 2

# TODO: Test other axises
