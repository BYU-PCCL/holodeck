import Holodeck
import time
import threading
import math
import random as r
import json
import numpy as np
import holodeck_environment as HolodeckEnvironment

def main(run_type):

	if run_type == "SPHERE":
		print("Connecting to SphereRobot")
		env = HolodeckEnvironment.HolodeckEnvironment("SPHERE",agent_name="BB-8",global_state_sensors={"CameraSensorArray2D","Score","Terminal"})

		action_dim = env.get_action_dim()
		state_dim = env.get_state_dim()

		#randomly act
		count = 0
		while count < 10:
			count += 1
			rand_int = r.randint(0,action_dim[1]-1)
			action = np.array([0 for x in xrange(action_dim[1])])
			action = np.reshape(action,[1,-1])
			action[0][rand_int] = 1
			
			state = env.act(action)
			print "Step: " + str(count)
			if "Score" in state:
				print("Score: " + state["Score"])
			time.sleep(1)

	elif run_type == "UAV":
		pass

	elif run_type == "ANDROID":
		env = HolodeckEnvironment.HolodeckEnvironment("ANDROID",agent_name="AndroidBlueprint",
			global_state_sensors={"CameraSensorArray2D","PressureSensor","JointRotationSensor","RelativeSkeletalPositionSensor","IMUSensor"})

		action_dim = env.get_action_dim()
		state_dim = env.get_state_dim()

		count = 0
		while count < 100:
			count += 1
			#action = np.array([r.random() for x in xrange(action_dim[1])])
			action = np.array([0, 0, 0, 1,0, 1,0, 0, 1, 0, 0, 0, 1, 0, 0, math.sin(count/10), 1,0, 1,0, 0, 0, 1,1, 0, 1,0, 1,0, 1,1, 0, 1,0, 1,0, 1,1, 0, 1,0, 1,0, 1,1, 0, 1,0, 1,0, 1,1, 0, 1,0, 1,0, 1,0, 0, math.sin(count/10), 1,0, 1,0, 0, 0, 1,1, 0, 1,0, 1,0, 1,1, 0, 1,0, 1,0, 1,1, 0, 1,0, 1,0, 1,1, 0, 1,0, 1,0, 1,1, 0, 1,0, 1,0, 1,1, 0, 0, 1,-.5, 1,-1, 0, 1,0, 0, 1,1, 0, 0, 1,-.5, 1,-1, 0, 1,0, 0, 1,])
			action = np.reshape(action,[1,-1])
			state = env.act(action)

			print "Step: " + str(count)
			print("State keys: " + str(state.keys()))
			print(state)
			time.sleep(.5)

if __name__ == "__main__":
	main("SPHERE")