import holodeck
import uuid
import numpy as np
from holodeck import packagemanager as pm
from holodeck.environments import HolodeckEnvironment

from tests.utils.equality import almost_equal



sphere_config = {
    "name": "test_location_sensor",
    "world": "TestWorld",
    "main_agent": "sphere0",
    "agents": [
        {
            "agent_name": "sphere0",
            "agent_type": "SphereAgent",
            "sensors": [
                {
                    "sensor_type": "LocationSensor",
                },
                {
                    "sensor_type": "RotationSensor",
                },
                {
                    "sensor_type": "VelocitySensor",
                },
            ],
            "control_scheme": 0,
            "location": [.95, -1.75, .5]
        }
    ]
}



def test_set_physics_state():

    binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

    env = holodeck.environments.HolodeckEnvironment(scenario=sphere_config,
                                                   binary_path=binary_path,
                                                   show_viewport=False,
                                                   uuid=str(uuid.uuid4()))

    print(env.tick())

    state = env.tick()

    newLocation = np.array([100,100,50])
    newRotation = np.array([75,75,50])
    newVelocity = np.array([60,60,0])

    env.agents["sphere0"].set_physics_state(newLocation, newRotation, newVelocity, [0,0,0])

    newState = env.tick()
    sensed_loc = newState["LocationSensor"]
    sensed_rot = newState["RotationSensor"]
    sensed_vel = newState["VelocitySensor"]

    print("The sensed location: ")
    print(sensed_loc)
    print("The expected location: ")
    print(newLocation)
    print("The sensed rotation: ")
    print(sensed_rot)
    print("The expected rotation: ")
    print(newRotation)
    print("the sensed velocity: ")
    print(sensed_vel)
    print("The expected velocity: ") 
    print(newVelocity)


    assert almost_equal(newLocation, sensed_loc), "The location was not set correctly!"
    assert almost_equal(newRotation, sensed_rot), "The rotation was not set correctly!"
    assert almost_equal(newVelocity, sensed_vel), "The velocity was not set correctly!"
    
