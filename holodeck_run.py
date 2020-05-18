import random
from holodeck import environments


config = {
    "name": "TestRun",
    "world": "TestWorld",
    "main_agent": "sphere0",
    "agents": [
        {
            "agent_name": "sphere0",
            "agent_type": "SphereAgent",
            "sensors": [{"sensor_type": "LocationSensor"}],
            "control_scheme": 0,  # Max Torque control scheme
            "location": [0, 0, 5],
        }
    ],
}


def test_android_constraints():
    binary_path = (
        "C:\\Users\\Danny\\repos\\holodeck-engine\\"
        "Binaries\\Win64\\Holodeck-Win64-DebugGame.exe"
    )

    with environments.HolodeckEnvironment(
        scenario=config,
        binary_path=binary_path,
        show_viewport=False,
        uuid="holodeck_debug",
        start_world=False,
    ) as env:
        env.reset()
        for _ in range(1000):
            action = random.randint(0, 3)
            state, reward, done, _ = env.step(action)
            print(reward)


if __name__ == "__main__":
    test_android_constraints()
