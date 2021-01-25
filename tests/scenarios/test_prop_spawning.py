import uuid
import copy
import holodeck

from tests.utils.equality import almost_equal

no_prop_config = {
    "name": "test_prop_spawning",
    "world": "TestWorld",
    "main_agent": "uav0",
    "agents": [
        {
            "agent_name": "uav0",
            "agent_type": "UavAgent",
            "sensors": [
                {
                    "sensor_type": "LocationSensor",
                }
            ],
            "control_scheme": 0,
            "location": [0, 0, 5],
        }
    ],
}


def _util_test_platform(env):
    """Utility function. Ensures the Uav lands on a platform"""
    # get the initial location after the uav has settled
    init_location = env.tick(10)["LocationSensor"]

    # get the final location
    final_location = env.tick(50)["LocationSensor"]

    assert almost_equal(
        init_location, final_location
    ), "Uav \
        continued to fall despite spawning a platform underneath!"


def test_static_prop():
    """Tests whether spawning a box without sim_physics creates a static box that keeps
    the agent from falling.
    """

    binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

    with holodeck.environments.HolodeckEnvironment(
        scenario=no_prop_config,
        binary_path=binary_path,
        show_viewport=False,
        uuid=str(uuid.uuid4()),
    ) as env:

        # spawn a platform for the uav to rest on
        env.spawn_prop("box", location=[0, 0, 4.5], scale=[5, 5, 0.5])
        _util_test_platform(env)


def test_sim_physics_prop():
    """Tests whether spawning a sphere with simulated physics creates a sphere that falls
    and rams the agent.
    """

    binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

    with holodeck.environments.HolodeckEnvironment(
        scenario=no_prop_config,
        binary_path=binary_path,
        show_viewport=False,
        uuid=str(uuid.uuid4()),
    ) as env:

        env.agents["uav0"].teleport([0, 0, 0.1])

        # get the initial location after the uav has settled
        init_location = env.tick(20)["LocationSensor"]

        # spawn a ball to fall on top of the agent
        env.spawn_prop("sphere", location=[0, 0.1, 3], scale=3, sim_physics=True)

        # get the final location after the uav has been knocked over
        final_location = env.tick(100)["LocationSensor"]

        assert not almost_equal(
            init_location, final_location
        ), "Uav \
            wasn't hit by a spawned sphere!"


def test_static_prop_config():
    config = copy.deepcopy(no_prop_config)
    prop_config = [{"type": "box", "location": [0, 0, 4.5], "scale": [5, 5, 0.5]}]
    config["props"] = prop_config

    binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

    with holodeck.environments.HolodeckEnvironment(
        scenario=config,
        binary_path=binary_path,
        show_viewport=False,
        uuid=str(uuid.uuid4()),
    ) as env:
        _util_test_platform(env)


def test_tagged_prop_config():
    config = copy.deepcopy(no_prop_config)
    prop_config = [
        {
            "type": "sphere",
            "scale": [1, 1, 1],
            "location": [0, 0, 100],
            "sim_physics": True,
            "material": "grass",
            "tag": "ball",
        }
    ]
    task_config = {
        "sensor_type": "DistanceTask",
        "configuration": {"GoalActor": "ball", "3dDistance": True},
    }
    config["props"] = prop_config
    config["agents"][0]["sensors"].append(task_config)
    print(config)

    binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

    with holodeck.environments.HolodeckEnvironment(
        scenario=config,
        binary_path=binary_path,
        show_viewport=False,
        uuid=str(uuid.uuid4()),
    ) as env:
        env.agents["uav0"].teleport([0, 0, 0.1])

        cum_reward = 0
        for _ in range(50):
            cum_reward += env.tick()["DistanceTask"][0]
        print(cum_reward)
        assert cum_reward > 2, "Distance task did not get reference to tagged prop!"
