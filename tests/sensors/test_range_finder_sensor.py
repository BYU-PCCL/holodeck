import holodeck
import uuid

from tests.utils.equality import almost_equal


sphere_config_count = {
    "name": "test_range_finder_sensor",
    "world": "TestWorld",
    "main_agent": "sphere0",
    "agents": [
        {
            "agent_name": "sphere0",
            "agent_type": "SphereAgent",
            "sensors": [
                {
                    "sensor_type": "RangeFinderSensor",
                    "configuration": {
                        "LazerCount": 4
                    }
                }
            ],
            "control_scheme": 0,
            "location": [.95, -1.75, .5]
        }
    ]
}


def test_range_finder_sensor_count():
    """Make sure the range sensor updates after specifying laxer count.
    """
    binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

    with holodeck.environments.HolodeckEnvironment(scenario=sphere_config_count,
                                                   binary_path=binary_path,
                                                   show_viewport=False,
                                                   uuid=str(uuid.uuid4())) as env:

        env.tick(10)

        state = env.tick()
        actual = state["RangeFinderSensor"]

        expected = sphere_config_count["agents"][0]["sensors"][0]["configuration"]["LazerCount"]

        assert len(actual) == expected, "Sensed range size did not match the expected size!"


sphere_config_max = {
    "name": "test_range_finder_sensor",
    "world": "TestWorld",
    "main_agent": "sphere0",
    "agents": [
        {
            "agent_name": "sphere0",
            "agent_type": "SphereAgent",
            "sensors": [
                {
                    "sensor_type": "RangeFinderSensor",
                    "configuration": {
                        "LazerMaxDistance": 1,
                        "LazerCount": 12
                    }
                }
            ],
            "control_scheme": 0,
            "location": [.95, -1.75, .5]
        }
    ]
}


def test_range_finder_sensor_max():
    """Make sure the range sensor set max distance correctly.
    """
    binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

    with holodeck.environments.HolodeckEnvironment(scenario=sphere_config_max,
                                                   binary_path=binary_path,
                                                   show_viewport=False,
                                                   uuid=str(uuid.uuid4())) as env:

        env.tick(10)

        state = env.tick()
        actual = state["RangeFinderSensor"]

        expected = sphere_config_max["agents"][0]["sensors"][0]["configuration"]["LazerMaxDistance"]

        assert all(x > 0 for x in actual), "Sensed range includes 0!"
        assert all(x <= expected for x in actual), "Sensed range includes value greater than 1!"


uav_config = {
    "name": "test_range_finder_sensor",
    "world": "TestWorld",
    "main_agent": "uav0",
    "agents": [
        {
            "agent_name": "uav0",
            "agent_type": "UavAgent",
            "sensors": [
                {
                    "sensor_type": "RangeFinderSensor",
                    "configuration": {
                        "LazerAngle": -90,
                        "LazerMaxDistance": 15
                    }
                }
            ],
            "control_scheme": 0,
            "location": [0, 0, 10]
        }
    ]
}


def test_range_finder_sensor_falling():
    """Makes sure that the range sensor updates as the UAV falls, and after it comes to a rest.
    """

    binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

    with holodeck.environments.HolodeckEnvironment(scenario=uav_config,
                                                   binary_path=binary_path,
                                                   show_viewport=False,
                                                   uuid=str(uuid.uuid4())) as env:

        last_range = env.tick()["RangeFinderSensor"][0]

        for _ in range(10):
            new_range = env.tick(4)["RangeFinderSensor"][0]
            assert new_range < last_range, "UAV's range sensor did not detect falling!"
            last_range = new_range

        # Give the UAV time to bounce and settle
        env.tick(80)

        # Make sure it is stationary now
        last_range = env.tick()["RangeFinderSensor"][0]
        new_range = env.tick()["RangeFinderSensor"][0]

        assert almost_equal(last_range, new_range), "The UAV did not seem to settle!"

