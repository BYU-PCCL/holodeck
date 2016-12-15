from holodeck_environment import HolodeckEnvironment
import numpy as np
import time

def main():
    print("Connecting to environment")
    env = HolodeckEnvironment("UAV", agent_name="UAV")
    action = np.array([[0, 0, 5, 14.70]])

    for i in range(100000):
        a = np.random.normal(size=3).reshape([1,3])
        action = np.concatenate((a, np.random.normal(loc=13, size=1).reshape([1,1])), axis=1)
        print (action.shape)
        print("Acting" + str(i))
        env.act(action)
        time.sleep(0.05)

    print("Finished")

if __name__=="__main__":
    main()