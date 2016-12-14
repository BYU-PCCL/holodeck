from holodeck_environment import HolodeckEnvironment
import numpy as np
import time

def main():
    print("Connecting to environment")
    env = HolodeckEnvironment("UAV", agent_name="UAVNoCamera")
    action = np.array([[0, 0, 0.5, 0]])

    for i in range(100000):
        print("Acting" + str(i))
        env.act(action)
        #time.sleep(1)

    print("Finished")

if __name__=="__main__":
    main()