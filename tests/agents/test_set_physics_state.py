import holodeck
from holodeck import packagemanager as pm
from holodeck.environments import HolodeckEnvironment



def test_set_physics_state():
    env = holodeck.make("MazeWorld-FinishMazeSphere")

    curr_location = holodeck.sensors.LocationSensor(env)
    curr_rotation = holodeck.sensors.RotationSensor(env)
    curr_velocity = holodeck.sensors.VelocitySensor(env)
  
    env.test_set_physics_state([100,100,50], [50,50,50], [50,0,0], [90,0,0])

    assert curr_location == holodeck.sensors.LocationSensor(env), "Location did not get set correctly!"
    assert curr_rotation == holodeck.sensors.RorationSensor(env), "Rotation did not get set correctly!"
    assert curr_velocity == holodeck.sensors.VelocitySensor(env), "Velocity did not get set correctly!"
