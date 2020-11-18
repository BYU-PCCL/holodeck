import holodeck
import uuid
from copy import deepcopy

from tests.utils.equality import almost_equal

uav_config2 = {
    "name": "test_max_height",
    "world": "TestWorld",
    "main_agent": "uav1",
    "agents": [
        {
            "agent_name": "uav1",
            "agent_type": "UavAgent",
            "sensors": [
                {
                    "sensor_type": "LocationSensor",
                }
            ],
            "control_scheme": 0,
            "location": [0, 0, 2],
            # "max_height": 50 - 11.8283691 # in centimeters # If you uncomment this, you'll see that the test fails
        }
    ]
}

def test_default_height():
    """Make sure the location sensor updates after a teleport. Also verifies that the coordinates for the teleport
    command match the coordinates used by the location sensor
    """

    with holodeck.environments.HolodeckEnvironment(scenario=uav_config2,
                                                   show_viewport=False,
                                                   start_world=False
                                                   )as env:

        command = [0, 0, 0, 1000]
        
        state = env.tick()
        sensed_loc = state["LocationSensor"]
        env.act("uav1", command)
        state = env.tick(50)
        assert ((sensed_loc[2] < state["LocationSensor"][2]) and not (almost_equal(sensed_loc[2], state["LocationSensor"][2]))), "UAV stopped moving up despite no set max height!"
