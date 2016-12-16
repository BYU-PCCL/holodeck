from holodeck_environment import HolodeckEnvironment
import numpy as np
import time
import cv2
from tqdm import tqdm

def main():
    print("Connecting to environment")
    env = HolodeckEnvironment("UAV", agent_name="UAV", global_state_sensors={"ViewportClient"})
    action = np.array([[0, 0, 5, 14.70]])

    for i in tqdm(range(100000)):
        a = np.random.normal(size=3).reshape([1,3])
        action = np.concatenate((a, np.random.normal(loc=13, size=1).reshape([1,1])), axis=1)
        state, reward, terminal = env.act(action)
        #cv2.imshow("test", state[0])
        #cv2.waitKey(1)
        #print(state[0].shape)
        #time.sleep(0.05)

    print("Finished")

if __name__=="__main__":
    main()