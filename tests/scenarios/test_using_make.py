from holodeck import make

base_conf = {
    "name": "test_randomization",
    "world": "TestWorld",
    "package_name": "DefaultWorlds",
    "main_agent": "sphere0",
    "agents": [
        {
            "agent_name": "sphere0",
            "agent_type": "SphereAgent",
            "sensors": [
                {
                    "sensor_type": "LocationSensor"
                },
                {
                    "sensor_type": "RotationSensor"
                }
            ],
            "control_scheme": 0,
            "location": [0.95, -1.75, 0.5],
            "rotation": [1.0, 2.0, 3.0],
            "location_randomization": [0.6, 0.5, 0.5],
            "rotation_randomization": [0.4, 0.3, 0.6]
        }
    ]
}


def test_using_make_to_create_worlds():

    # TODO: We need some way of communicating with the engine to verify that the expected level was loaded.
    # If the level isn't found, then Unreal just picks a default one, so we're missing that case

    with make(scenario_cfg=base_conf) as env:
        for _ in range(0, 10):
            env.tick()

    conf = base_conf
    conf["world"] = "CyberPunkCity"
    with make(scenario_cfg=conf) as env:
        for _ in range(0, 10):
            env.tick()

    conf["world"] = "EuropeanForest"
    with make(scenario_cfg=conf) as env:
        for _ in range(0, 10):
            env.tick()

    conf["world"] = "InfiniteForest"
    with make(scenario_cfg=conf) as env:
        for _ in range(0, 10):
            env.tick()



