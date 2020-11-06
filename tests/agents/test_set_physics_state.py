import holodeck
import uuid
import numpy as np
from holodeck import packagemanager as pm
from holodeck.environments import HolodeckEnvironment

from tests.utils.equality import almost_equal



sphere_config = {
    "name": "test_location_sensor",
    "world": "TestWorld",
    "main_agent": "turtle0",
    "agents": [
        {
            "agent_name": "turtle0",
            "agent_type": "TurtleAgent",
            "sensors": [
                {
                    "sensor_type": "RotationSensor",
                },
                {
                    "sensor_type": "LocationSensor",
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



def test_set_physics_state_loc_and_rot():

    binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

    env = holodeck.environments.HolodeckEnvironment(scenario=sphere_config,
                                                   binary_path=binary_path,
                                                   show_viewport=False,
                                                   uuid=str(uuid.uuid4()))

    

    state = env.tick(100)


    newLocation = np.array([0,100,0])
    newRotation = np.array([90,10,10])
   
    env.agents["turtle0"].set_physics_state(newLocation, newRotation, [0,0,0], [0,0,0])
    
    newState = env.tick(50)
    sensed_loc = newState["LocationSensor"]
    sensed_rot = newState["RotationSensor"]
   
   


    print("The sensed location: ")
    print(sensed_loc)
    print("The expected location: ")
    print(newLocation)
    print("The sensed rotation: ")
    print(sensed_rot)
    print("The expected rotation: ")
    print(newRotation)
    


    assert almost_equal(newLocation, sensed_loc), "The location was not set correctly!"
    assert almost_equal(newRotation, sensed_rot), "The rotation was not set correctly!"
   

def test_set_physics_state_vel():

    binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

    env = holodeck.environments.HolodeckEnvironment(scenario=sphere_config,
                                                   binary_path=binary_path,
                                                   show_viewport=False,
                                                   uuid=str(uuid.uuid4()))

    
    state = env.tick(50)
   
    new_vel = np.array([50,0,0])

    env.agents["turtle0"].set_physics_state([0,0,0], [0,0,0], new_vel, [0,0,0])

    newState = env.tick(50)
    sensed_vel = newState["VelocitySensor"]


    assert almost_equal(new_vel, sensed_vel), "The velocity was not set correctly!"
