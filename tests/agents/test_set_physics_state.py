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
    """Validates that the set_physics_state function correctly sets the location and rotation of the agent.

    """

    binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

    with holodeck.environments.HolodeckEnvironment(scenario=sphere_config,
                                                   binary_path=binary_path,
                                                   show_viewport=False,
                                                   uuid=str(uuid.uuid4())) as env:

        new_loc = np.array([0,0,100])
        new_rot = np.array([90,10,10])

        #This should change the location and the rotation of the agent. 
        env.agents["turtle0"].set_physics_state(new_loc, new_rot, [0,0,0], [0,0,0])
        
        new_state = env.tick()
        sensed_loc = new_state["LocationSensor"]
        sensed_rot = new_state["RotationSensor"]

        #Check to see if the newly sensed loc and rot are what we wanted to set them too. 
        assert almost_equal(new_loc, sensed_loc), "The location was not set correctly!"
        assert almost_equal(new_rot, sensed_rot), "The rotation was not set correctly!"
    

def test_set_physics_state_vel():
    """Validates that the set_physics_state function correctly sets the velocity of the agent. 

    """

    binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

    with holodeck.environments.HolodeckEnvironment(scenario=sphere_config,
                                                   binary_path=binary_path,
                                                   show_viewport=False,
                                                   uuid=str(uuid.uuid4())) as env:

        new_vel = np.array([50,0,0])

        #This should change the velocity of the agent. 
        env.agents["turtle0"].set_physics_state([0,0,0], [0,0,0], new_vel, [0,0,0])

        new_state = env.tick()
        sensed_vel = new_state["VelocitySensor"]

        #Check to see that the newly sensed vel is what we wanted to set it too. 
        assert almost_equal(new_vel, sensed_vel,0.0,0.3), "The velocity was not set correctly!"


def test_set_physics_state_ang_vel():
    """Validates that the set_physics_state function correctly sets the angular velocity of the agent.
    There is no angular velocity sensor so it checks to see if the agent is spinning (rotation changes)
    after changing the angular velocity. 

    """

    binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

    with holodeck.environments.HolodeckEnvironment(scenario=sphere_config,
                                                   binary_path=binary_path,
                                                   show_viewport=False,
                                                   uuid=str(uuid.uuid4())) as env:

        state = env.tick()
        new_ang_vel = np.array([90,0,0])
        start_rot = state["RotationSensor"]

        #This should change the angular velocity of the agent.
        env.agents["turtle0"].set_physics_state([0,0,0], start_rot, [0,0,0], new_ang_vel)

        new_state = env.tick()
        sensed_rot = new_state["RotationSensor"]

        #Check to see if the agent changes rotation, if angular velocity was set correctly the rotation should change. 
        assert not almost_equal(start_rot, sensed_rot), "Angular Velocity was not set correctly!"


def test_set_physics_state_collision():
    """Validates that the agent will collide with something and not finish teleporting when using the set_physics_state
    function if there is an obstacle in the way. 
    The teleport function of the agent will do a sweep and thus stopping whenever an obstacle is encountered. 

    """

    binary_path = holodeck.packagemanager.get_binary_path_for_package("DefaultWorlds")

    with holodeck.environments.HolodeckEnvironment(scenario=sphere_config,
                                                   binary_path=binary_path,
                                                   show_viewport=False,
                                                   uuid=str(uuid.uuid4())) as env:

        state = env.tick()
        start_loc = state["LocationSensor"]
        new_loc = np.array([100,0,0])

        #This should not work, the agent should collide with wall and not teleport completely.
        env.agents["turtle0"].set_physics_state(new_loc,[0,0,0],[0,0,0],[0,0,0])

        new_state = env.tick()
        sensed_loc = new_state["LocationSensor"]

        #Checking the collision by validating that it did not teleport to the desire location. 
        assert not almost_equal(start_loc, sensed_loc), "The location was not set correctly!"
        assert not almost_equal(new_loc, sensed_loc), "The location was not set correctly!"
