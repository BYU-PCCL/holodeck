import holodeck
import uuid
from copy import deepcopy

from tests.utils.equality import almost_equal

uav_config = {
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
            "max_height": 500 - 11.8283691 # in centimeters
        }
    ]
}


def test_higher_than_mh():
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

        command = [0, 0, 0, 1000]
        max_height = 5 # in meters

        for _ in range(900):
            state, reward, terminal, _ = env.step(command)

        sensed_loc = state["LocationSensor"]
        print(sensed_loc[2])

        assert (sensed_loc[2] <= max_height), "IT TOO HIGH"
