Holodeck is a simulator built for training reinforcement agents. It comes with several pre-made worlds.

GENERAL USAGE
-------------
To use Holodeck, you need a worlds folder in the directory you are working in, in which you download the necessary
world binary. You should also include the Holodeck folder.
To start, create a holodeck environment (lists are provided below on the details of different environments)

from Holodeck.HolodeckEnvironment import HolodeckUAVMazeEnvironment
env = HolodeckUAVMazeEnvironment

Then you can simply call the act function:
state, reward, terminal = env.act( ACTION )
to send an action to the agent.

There are currently 4 supported agents:
UAV - A quad-copter which takes for inputs roll, pitch, yaw rate, altitude
Android - A humanoid agent which takes commands for each joint
DiscreteSphere - A basic agent that can move forwards and turn 90 degrees.
ContinuousSphere - A basic agent that can move a specified amount forward and turn a specified number of degrees

For greater detail in configuration, please see the worlds list below:

UAV WORLDS
    i) Maze World - HolodeckUAVMazeWorldSmall, HolodeckUAVMazeWorldLarge

ANDROID WORLDS
    None

SPHERE ROBOT WORLDS
    i) Maze World - HolodeckDiscreteSphereMazeWorldSmall, HolodeckDiscreteSphereMazeWorldLarge
                    HolodeckContinousSphereMazeWorldSmall, HolodeckContinousSphereMazeWorldLarge


UAV WORLDS
i) Maze World
    Description: A basic maze world with a UAV. Reward is based on linear distance to the goal.
    Agent names: UAV0
    Sensors: PrimaryPlayerCamera
    Resolution: Large:512x512, Small:256x256

ANDROID WORLDS

SPHERE ROBOT WORLDS
i) Maze World
    Description: A basic maze world with a sphere robot. Reward is based on linear distance to the goal.
    Agent names: sphere0
    Sensors: PrimaryPlayerCamera
    Resolution: Large:512x512, Small:256x256



-------------------------OLD NOTES-------------------------------------------

In the UE4 Project Settings -> Physics, Substepping should be on,
Max Substep Delta Time should be as small as possible (I have it at 0.0013),
and Max Substeps should be as large as possible (I have it at 16). 
This stops the android from twitching unexpectedly.



        """self.joint_list = [
            "head",
            "neck_01",
            "spine_02",
            "spine_01",
            "upperarm_l",
            "lowerarm_l",
            "hand_l",
            "thumb_01_l",
            "thumb_02_l",
            "thumb_03_l",
            "index_01_l",
            "index_02_l",
            "index_03_l",
            "middle_01_",
            "middle_02_",
            "middle_03_",
            "ring_01_l",
            "ring_02_l",
            "ring_03_l",
            "pinky_01_l",
            "pinky_02_l",
            "pinky_03_l",
            "upperarm_r",
            "lowerarm_r",
            "hand_r",
            "thumb_01_r",
            "thumb_02_r",
            "thumb_03_r",
            "index_01_r",
            "index_02_r",
            "index_03_r",
            "middle_01_",
            "middle_02_",
            "middle_03_",
            "ring_01_r",
            "ring_02_r",
            "ring_03_r",
            "pinky_01_r",
            "pinky_02_r",
            "pinky_03_r",
            "thigh_l",
            "calf_l",
            "foot_l",
            "ball_l",
            "thigh_r",
            "calf_r",
            "foot_r",
            "ball_r"
        ]"""


The following code is best viewed in edit mode to maintain proper spacing:

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

So what does this ^^^ all mean? When spaced properly, there should be three columns and 43 rows. The first column is the actual input, and the second two columns (the commented ones) represent what those control inputs mean. The second column represents which joint is being controlled, and the third column represents what axis is controlled by each input.

In the first column, you will find between 2 and 4 floats. The floats should be between -1 and 1. The last float in the first column represents the amount of effort used by the android to move the joint to the desired destination. The desired destination is determined by the other floats in the column. For example, if one row looked like this:

1, 0, 0.5,                 # thumb_01_l     s1,   , s2

Then that tells the android to move the thumb_01_l joint to its maximum swing_1 and it's middle swing_2 with half of its maximum effort. The android cannot twist its thumb, so there is no "tw." 

TO DO:
Certain agents can only have certain sensors
Reward and terminal should always be returned
Make project PEP8 compliant
Add messages on initialize:
    Window Size
    What agent to spawn
Edit code so that there is only ever one holodeck controller and pawn, and make it so name doesn't matter
UAV continually spins
Tune up PID
