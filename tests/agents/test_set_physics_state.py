import holodeck
from holodeck import packagemanager as pm
from holodeck.environments import HolodeckEnvironment



def test_set_physics_state():
    env = holodeck.make("MazeWorld-FinishMazeSphere")

    print(env.tick())

    state = env.tick()
    curr_location = state["LocationSensor"]
    curr_rotation = state["RotationSensor"]
    curr_velocity = state["VelocitySensor"]
  
    env.set_physics_state([100,100,50], [50,50,50], [50,0,0], [90,0,0])

    newState = env.tick()

    assert curr_location == newState["LocationSensor"], "Location did not get set correctly!"
    assert curr_rotation == newState["RotationSensor"], "Rotation did not get set correctly!"
    assert curr_velocity == newState["VelocitySensor"], "Velocity did not get set correctly!"
