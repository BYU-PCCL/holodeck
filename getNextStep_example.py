import Holodeck
import time
import math

if __name__ == "__main__":

    def main():

        # initialize agent
        print("Starting and waiting for Android to connect...")
        agent = Holodeck.AndroidAgent.AndroidAgent(hostname="localhost", port=8989, agentName="AndroidBlueprint",
                                                   global_state_sensors={"CameraSensorArray2D",
                                                                         "PressureSensor",
                                                                         "JointRotationSensor",
                                                                         "RelativeSkeletalPositionSensor",
                                                                         "IMUSensor"}).waitFor("Connect")
        print("Connected to Android.")

        # set any agent or world settings
        agent.configure().setCollisionsVisible(False).send()
        # set allowedticks to 1 to have least possible time passed between states
        agent.worldCommand().setAllowedTicksBetweenCommands(1).send()

        for i in range(20):

            # get state
            output = agent.getNextState()

            print("------   State " + str(i) + "   ------")
            print("Joint Rotation Sensor:")
            print(output["JointRotationSensor"])
            print("RelativeSkeletalPositionSensor:")
            print(output["RelativeSkeletalPositionSensor"])
            print("IMUSensor:")
            print(output["IMUSensor"])
            print("PressureSensor:")
            print(output["PressureSensor"])
            print("Printing CameraSensorArray2D images to file . . .")
            with open("lefteye.jpg", "wb") as f:
                f.write(output["CameraSensorArray2D"][0])
            with open("righteye.jpg", "wb") as f:
                f.write(output["CameraSensorArray2D"][1])

            time.sleep(0.2)

            # respond to state
            command = [0, 0, 0, 1,              # head           s1, tw, s2
                       0, 1,                    # neck_01        s1,   ,
                       0, 0, 1,                 # spine_02       s1, tw,
                       0, 0, 0, 1,              # spine_01       s1, tw, s2
                       0, 0, math.sin(i/10), 1,  # upperarm_l     s1, tw, s2
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
                       0, 0, math.sin(i/10), 1,  # upperarm_r     s1, tw, s2
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
                       0, 0, 1 ]                 # ball_r         s1, tw,
            agent.command().setJointRotationAndForce(command).send()

        print("Killing the Android")
        agent.kill()
        print("Android killed.")

    main()
