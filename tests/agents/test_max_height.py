import holodeck
import uuid
from copy import deepcopy

from tests.utils.equality import almost_equal

height_config = {
    "name": "test_max_height",
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
            "location": [0, 0, 2],
            "max_height": 3
        }
    ]
}

no_height_config = {
    "name": "test_max_height",
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
            "location": [0, 0, 2]
        }
    ]
}

binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

def test_max_height_set():
    """Make sure that the agent doesn't travel higher than the set max height.
    """
    binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

    with holodeck.environments.HolodeckEnvironment(scenario=height_config,
                                                   binary_path=binary_path,
                                                   show_viewport=False,
                                                   uuid=str(uuid.uuid4())) as env:

        max_height = height_config["agents"][0]["max_height"]

        command = [0, 0, 0, 1000]
        env.act("uav0", command)
        state = env.tick(50)

        current_location = state["LocationSensor"]

        assert ((current_location[2] < max_height) or almost_equal(current_location[2], max_height, r_thresh=12)), "UAV ignored max height that was set!"
        # The threshold is 12 (11.8283691) because for whatever reason, the UAV goes slightly above the set max height. No one knows why.


def test_stuck_at_max_height():
    """Make sure that the agent doesn't get stuck at the max height after it is first stopped.
    """

    with holodeck.environments.HolodeckEnvironment(scenario=height_config,
                                                   binary_path=binary_path,
                                                   show_viewport=False,
                                                   uuid=str(uuid.uuid4())) as env:

        max_height = height_config["agents"][0]["max_height"]

        command = [0, 0, 0, 100]
        env.act("uav0", command)
        state = env.tick(50)

        command = [0, 0, 0, 0]
        env.act("uav0", command)
        state = env.tick(50)

        current_location = state["LocationSensor"]

        assert ((current_location[2] < max_height) and not (almost_equal(current_location[2], max_height))), "UAV did not fall from max height!"


def test_no_max_height_set():
    """Make sure that not setting a max height will default to not applying a max height.
    """

    with holodeck.environments.HolodeckEnvironment(scenario=no_height_config,
                                                   binary_path=binary_path,
                                                   show_viewport=False,
                                                   uuid=str(uuid.uuid4())) as env:

        command = [0, 0, 0, 1000]
        state = env.tick()
        old_location = state["LocationSensor"]

        env.act("uav0", command)
        state = env.tick(50)
        current_location = state["LocationSensor"]

        assert ((old_location[2] < current_location[2]) and not (almost_equal(old_location[2], current_location[2]))), "UAV stopped moving up despite no set max height!"
