import holodeck
import uuid
from copy import deepcopy

from tests.utils.equality import almost_equal

uav_config = {
    "name": "test_max_height",
    "world": "TestWorld",
    "main_agent": "uav3",
    "agents": [
        {
            "agent_name": "uav3",
            "agent_type": "UavAgent",
            "sensors": [
                {
                    "sensor_type": "LocationSensor",
                }
            ],
            "control_scheme": 0,
            "location": [0, 0, 2],
            "max_height": 5 # in centimeters
        }
    ]
}


def test_not_stuck_at_mh():
    """Make sure the location sensor updates after a teleport. Also verifies that the coordinates for the teleport
    command match the coordinates used by the location sensor
    """
    # binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

    with holodeck.environments.HolodeckEnvironment(scenario=uav_config,
                                                   # binary_path=binary_path,
                                                   show_viewport=False,
                                                   start_world=False
                                                   # uuid=str(uuid.uuid4()) 
                                                   )as env:

        max_height = uav_config["agents"][0]["max_height"]
        command = [0, 0, 0, 100]
        env.act("uav3", command)
        state = env.tick(50)
        command = [0, 0, 0, 0]
        env.act("uav3", command)
        state = env.tick(50)

        sensed_loc = state["LocationSensor"]
        print(sensed_loc[2])

        assert ((sensed_loc[2] < max_height) and not (almost_equal(sensed_loc[2], max_height))), "UAV did not fall from max height!"
