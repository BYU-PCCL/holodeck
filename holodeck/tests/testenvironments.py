import holodeck
from holodeck import agents
from holodeck.environments import *
from holodeck.sensors import Sensors
import cv2

def basic_test(env, agent_name, command):

    # Test basic control and pixel_camera
    for i in range(2):
        env.reset()

        for j in range(300):
            state, reward, terminal, _ = env.step(command)

            # To access specific sensor data:
            pixels = state[Sensors.PIXEL_CAMERA]
            if j < 5:
                cv2.imwrite("Image" + str(j) + ".jpg", pixels[:, :, 0:3])
            velocity = state[Sensors.VELOCITY_SENSOR]

def spawn_test(env, agent_name, command):

    # Test spawn, teleport agent and teleport camera
    for i in range(2):
        env.reset()

        state, reward, terminal, _ = env.step(command)
        main_loc = state[Sensors.LOCATION_SENSOR]

        sensors = [Sensors.LOCATION_SENSOR, Sensors.VELOCITY_SENSOR]
        agent = AgentDefinition("uav1", agents.UavAgent, sensors)
        env.spawn_agent(agent, [1, 1, 5])
        env.tick()
        env.set_control_scheme("uav1", ControlSchemes.UAV_ROLL_PITCH_YAW_RATE_ALT)

        env.act("uav0", command)
        env.act("uav1", command)

        for j in range(50):
            env.tick()

        env.teleport_camera([10, 10, 10], [0, 0, 0]) ### Seems to be moving 

        for j in range(500):
            env.tick()


if __name__ == "__main__":

    env = holodeck.make("UrbanCity")
    env.set_control_scheme("uav0", ControlSchemes.UAV_ROLL_PITCH_YAW_RATE_ALT)
    spawn_test(env, "uav0", [0, 0, 1, 10])
