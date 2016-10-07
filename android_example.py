import Holodeck
import time
import threading
import math
import random as r
import json

if __name__ == "__main__":

    def android():
        print("Starting and waiting for Android to connect...")
        agent = Holodeck.AndroidAgent.AndroidAgent(hostname="localhost", port=8989, agentName="AndroidBlueprint",
                                                   global_state_sensors={"CameraSensorArray2D",
                                                                         "PressureSensor",
                                                                         "JointRotationSensor",
                                                                         "RelativeSkeletalPositionSensor",
                                                                         "IMUSensor"}).waitFor("Connect")
        print("Connected to Android.")

        # Note: this command will affect ALL agents in the world
        print("Setting the simulator to pause every 1 frame after a command")
        agent.worldCommand().setAllowedTicksBetweenCommands(1).send()\
        agent.configure().setCollisionsVisible(False).send()
        
        #some other example world commands
        #agent.worldCommand().restartLevel().send()
        #agent.worldCommand().loadLevel("MyNextLevel").send()

        def onState(data, type=None):
            #print("i just got your state message")
            print("Message from " + type)
            print(data)

        #agent.subscribe('State', onState)
        agent.subscribe('CameraSensorArray2D', onState)
        agent.subscribe("PressureSensor",onState)
        agent.subscribe("JointRotationSensor",onState)
        agent.subscribe("RelativeSkeletalPositionSensor",onState)
        agent.subscribe("IMUSensor",onState)

        for i in range(1000):
            command = [0, 0, 0, 1,              # head           s1, tw, s2
                       0, 1,                    # neck_01        s1,   ,
                       0, 0, 1,                 # spine_02       s1, tw,
                       0, 0, 0, 1,              # spine_01       s1, tw, s2
                       0, 0, math.sin(i/10), 1, # upperarm_l     s1, tw, s2
                       0, 1,                    # lowerarm_l     s1,   ,
                       0, 0, 0, 1,              # hand_l         s1, tw, s2
                       1, 0, 1,                 # thumb_01_l     s1,   , s2
                       0, 1,                    # thumb_02_l     s1,   ,
                       0, 1,                    # thumb_03_l     s1,   ,
                       1, 0, 1,                 # index_01_l     s1,   , s2
                       0, 1,                    # index_02_l     s1,   ,
                       0, 1,                    # index_03_l     s1,   ,
                       1, 0, 1,                 # middle_01_l    s1,   , s2
                       0, 1,                    # middle_02_l    s1,   ,
                       0, 1,                    # middle_03_l    s1,   ,
                       1, 0, 1,                 # ring_01_l      s1,   , s2
                       0, 1,                    # ring_02_l      s1,   ,
                       0, 1,                    # ring_03_l      s1,   ,
                       1, 0, 1,                 # pinky_01_l     s1,   , s2
                       0, 1,                    # pinky_02_l     s1,   ,
                       0, 1,                    # pinky_03_l     s1,   ,
                       0, 0, math.sin(i/10), 1, # upperarm_r     s1, tw, s2
                       0, 1,                    # lowerarm_r     s1,   ,
                       0, 0, 0, 1,              # hand_r         s1, tw, s2
                       1, 0, 1,                 # thumb_01_r     s1,   , s2
                       0, 1,                    # thumb_02_r     s1,   ,
                       0, 1,                    # thumb_03_r     s1,   ,
                       1, 0, 1,                 # index_01_r     s1,   , s2
                       0, 1,                    # index_02_r     s1,   ,
                       0, 1,                    # index_03_r     s1,   ,
                       1, 0, 1,                 # middle_01_r    s1,   , s2
                       0, 1,                    # middle_02_r    s1,   ,
                       0, 1,                    # middle_03_r    s1,   ,
                       1, 0, 1,                 # ring_01_r      s1,   , s2
                       0, 1,                    # ring_02_r      s1,   ,
                       0, 1,                    # ring_03_r      s1,   ,
                       1, 0, 1,                 # pinky_01_r     s1,   , s2
                       0, 1,                    # pinky_02_r     s1,   ,
                       0, 1,                    # pinky_03_r     s1,   ,
                       1, 0, 0, 1,             # thigh_l        s1, tw, s2
                       -.5, 1,                  # calf_l         s1,   ,
                       -1, 0, 1,                # foot_l         s1,   , s2
                       0, 0, 1,                 # ball_l         s1, tw,
                       1, 0, 0, 1,             # thigh_r        s1, tw, s2
                       -.5, 1,                  # calf_r         s1,   ,
                       -1, 0, 1,                # foot_r         s1,   , s2
                       0, 0, 1,                 # ball_r         s1, tw,
                       ]

            agent.command().setJointRotationAndForce(command).send()

            time.sleep(.1)

        print("Killing the Android")
        agent.kill()
        print("Android killed.")

    android()
