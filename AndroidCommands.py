import Holodeck
import time
import threading
import math
import random as r
import json
"""
class Current_State:

    def __init__(self, testing_name="ignore me"):
        self.name = testing_name
        self.cameras = None
        self.joint_angles = None
        self.imu = None
        self.pressure = None

    def set_pressure(self, new_pressure):
        self.pressure = new_pressure
        print "New Pressure recieved and set"
"""
if __name__ == "__main__":

    """state = Current_State("its me")
    state.set_pressure(162)
    state.pressure = 162

    state.new_var = "foo"
    """

    foot_l_correct = [0,0,0]
    foot_r_correct = [0,0,0]
    foot_l_current = [0,0,0]
    foot_r_current = [0,0,0]
    countdown = 6
    armswing_postition = 0 #should be between 0 and 1

    def get_foot_l_correct():
        global foot_l_correct
        return foot_l_correct

    def set_foot_l_correct(arg):
        global foot_l_correct
        foot_l_correct = arg

    def get_foot_r_correct():
        global foot_l_correct
        return foot_l_correct

    def set_foot_r_correct(arg):
        global foot_l_correct
        foot_l_correct = arg

    def get_foot_l_current():
        global foot_l_current
        return foot_l_current

    def set_foot_l_current(arg):
        global foot_l_current
        foot_l_current = arg

    def get_foot_r_current():
        global foot_l_current
        return foot_l_current

    def set_foot_r_current(arg):
        global foot_l_current
        foot_l_current = arg

    def get_countdown():
        global countdown
        return countdown

    def set_countdown(arg):
        global countdown
        countdown = arg

    def get_armswing_position():
        global armswing_postition
        return armswing_postition

    def set_armswing_position(arg):
        global armswing_postition
        armswing_postition = arg

    def android():
        print ("Starting and waiting for Android to connect...")
        agent = Holodeck.AndroidAgent.AndroidAgent(hostname="localhost", port=8989, agentName="AndroidBlueprint").waitFor("Connect")
        print ("Connected to Android.")

        # Note: this command will affect ALL agents in the world
        print ("Setting the simulator to pause every 1 frame after a command")
        agent.worldCommand().setAllowedTicksBetweenCommands(0).send()
        agent.configure().setCollisionsVisible(False).send()

        def onCamera(data):
            pass#print ("onCamera")#(data)

        def onHit(data):
            pass#print ("onHit")#(data)

        def onJointRotation(data):
            pass#print('JointRotation')
            parsed = json.loads(data)
            
            for joint in parsed:
                if joint['Bone'] == "foot_r":
                    """print ("OUTPUT:" + str('%10f' % joint['Swing1']) + ", "
                           + str('%10f' % joint['Twist']) + ", "
                           + str('%10f' % joint['Swing2']))"""
                    #print (foot_r_correct)
                    #print (countdown)

                    set_foot_r_current([joint['Swing1'],joint['Twist'],joint['Swing2']])
                    if get_countdown() == 0:
                        set_foot_r_correct([joint['Swing1'],joint['Twist'],joint['Swing2']])
                        
                if joint['Bone'] == "foot_l":
                    set_foot_l_current([joint['Swing1'],joint['Twist'],joint['Swing2']])
                    if get_countdown() == 0:
                        print("HEYHEYHEYHEY SWING1: " + str(joint['Swing1']))
                        set_foot_l_correct([joint['Swing1'],joint['Twist'],joint['Swing2']])
                        set_countdown(get_countdown()-1)
                    elif get_countdown() > 0:
                        set_countdown(get_countdown()-1)

                    
        def onRelativePosition(data):
            """"\trQuat: X=" + '%10f' % printableResultQuat[0] +\
                           ", Y=" + '%10f' % printableResultQuat[1] +\
                           ", Z=" + '%10f' % printableResultQuat[2] +\
                           ", W=" + '%10f' % printableResultQuat[3])                     
                    #printableResultQuat = [joint['Quaternion']['X'],\
                    #                             joint['Quaternion']['Y'],\
                    #                             joint['Quaternion']['Z'],\
                    #                             joint['Quaternion']['W']]
                    """
            pass
            """parsed = json.loads(data)
            for joint in parsed:
                if joint['Bone'] == "upperarm_r":
                    eulerComponent = quatToEuler(joint['Quaternion']['X'],\
                                                 joint['Quaternion']['Y'],\
                                                 joint['Quaternion']['Z'],\
                                                 joint['Quaternion']['W'])
                    print ("Euler: " +\
                           '%10f' % eulerComponent[0] + ", " +\
                           '%10f' % eulerComponent[1] + ", " +\
                           '%10f' % eulerComponent[2])"""

        def onIMU(data):
            pass#print('IMU')
            """parsed = json.loads(data)
            print("  X: " + '%10f' % parsed['x_accel'] +\
                  "  Y: " + '%10f' % parsed['y_accel'] +\
                  "  Z: " + '%10f' % parsed['z_accel'] +\
                  "  roll: " + '%10f' % parsed['roll_vel'] +\
                  "  pitch: " + '%10f' % parsed['pitch_vel'] +\
                  "  yaw: " + '%10f' % parsed['yaw_vel'])"""

        # Subscribe the function onCamera to the CameraSensorArray2D sensor messages
        agent.subscribe("CameraSensorArray2D", onCamera)

        # Subscribe the function onHit to the PressureSensor messages
        agent.subscribe("PressureSensor", onHit)

        # Subscribe the function onJointRotation to the onJointRotationSensor messages
        agent.subscribe("JointRotationSensor", onJointRotation)

        # Subscribe the function onRelativePosition to the RelativePositionSensor messages
        agent.subscribe("RelativeSkeletalPositionSensor", onRelativePosition)

        # Subscribe the function onRelativePosition to the RelativePositionSensor messages
        agent.subscribe("IMUSensor", onIMU)

        def quatToEuler(qz, qy, qx, qw):
            if(qx*qy+qz*qw == 0.5):
                return [0,
                        math.asin(2*qx*qy+2*qz*qw),
                        2*math.atan2(qx,qw)]

            elif(qx*qy+qz*qw == -0.5):
                return [0,
                        math.asin(2*qx*qy+2*qz*qw),
                        -2*math.atan2(qx,qw)]

            else:
                return [math.atan2(2*qx*qw - 2*qy*qz, 1 - 2*(qx**2) - 2*(qz**2)),
                        math.asin(2*qx*qy + 2*qz*qw),
                        math.atan2(2*qy*qw - 2*qx*qz, 1 - 2*(qy**2) - 2*(qz**2))]

        def eulerToQuat(roll, pitch, yaw):
            c1 = math.cos(pitch / 2)
            s1 = math.sin(pitch / 2)
            c2 = math.cos(yaw / 2)
            s2 = math.sin(yaw / 2)
            c3 = math.cos(roll / 2)
            s3 = math.sin(roll / 2)
            c1c2 = c1*c2
            s1s2 = s1*s2
            w = c1c2*c3 - s1s2*s3
            x = c1c2*s3 + s1s2*c3
            z = s1*c2*c3 + c1*s2*s3
            y = c1*s2*c3 - s1*c2*s3
            return [x, y, z, w]

        
        upperarm_l_balance = 0
        upperarm_r_balance = 0
        
        for i in range(1000):

            if get_countdown() == -1:
                print('====================')
                print('foot_l_correct: ' + str(get_foot_l_correct()[0]))
                print('foot_l_current: ' + str(get_foot_l_current()[0]))
                print('upperarm_l_balance: ' + str(upperarm_l_balance))
                print("countdown " + str(get_countdown()))
                upperarm_l_balance = -((get_foot_l_correct()[0] - get_foot_l_current()[0]))
                if upperarm_l_balance > 1:
                    upperarm_l_balance = 1
                elif upperarm_l_balance < -1:
                    upperarm_l_balance = -1

                upperarm_r_balance = -((get_foot_r_correct()[0] - get_foot_r_current()[0]))
                if upperarm_r_balance > 1:
                    upperarm_r_balance = 1
                elif upperarm_r_balance < -1:
                    upperarm_r_balance = -1


            upperarms = swing_arms_to_balance(math.tanh(3*(upperarm_l_balance+upperarm_r_balance)))
            
            
            command = [0,0,0,1, #head           s1,tw,s2 
                       0,1,     #neck_01        s1,tw,s2 
                       0,0,1,   #spine_02       s1,  ,   
                       0,0,0,1, #spine_03       s1,tw,s2 
                       upperarms[0],0,upperarms[2],1, #upperarm_l     s1,tw,s2 
                       0,1,     #lowerarm_l     s1,  ,   
                       0,0,0,1, #hand_l         s1,tw,s2 
                       0,0,1,   #thumb_01_l     s1,  ,s2 
                       0,1,     #thumb_02_l     s1,  ,   
                       0,1,     #thumb_03_l     s1,  ,   
                       0,0,1,   #index_01_l     s1,  ,s2
                       0,1,     #index_02_l     s1,  ,  
                       0,1,     #index_03_l     s1,  ,
                       0,0,1,   #middle_01_l    s1,  ,s2
                       0,1,     #middle_02_l    s1,  ,
                       0,1,     #middle_03_l    s1,  ,
                       0,0,1,   #ring_01_l      s1,  ,s2
                       0,1,     #ring_02_l      s1,  ,
                       0,1,     #ring_03_l      s1,  ,
                       0,0,1,   #pinky_01_l     s1,  ,s2
                       0,1,     #pinky_02_l     s1,  ,
                       0,1,     #pinky_03_l     s1,  ,
                       upperarms[0],0,upperarms[2],1, #upperarm_r     s1,tw,s2
                       0,1,     #lowerarm_r     s1,  ,
                       0,0,0,1, #hand_r         s1,tw,s2
                       0,0,1,   #thumb_01_r     s1,  ,s2
                       0,1,     #thumb_02_r     s1,  ,
                       0,1,     #thumb_03_r     s1,  ,
                       0,0,1,   #index_01_r     s1,  ,s2
                       0,1,     #index_02_r     s1,  ,
                       0,1,     #index_03_r     s1,  ,
                       0,0,1,   #middle_01_r    s1,  ,s2
                       0,1,     #middle_02_r    s1,  ,
                       0,1,     #middle_03_r    s1,  ,
                       0,0,1,   #ring_01_r      s1,  ,s2
                       0,1,     #ring_02_r      s1,  ,
                       0,1,     #ring_03_r      s1,  ,
                       0,0,1,   #pinky_01_r     s1,  ,s2
                       0,1,     #pinky_02_r     s1,  ,
                       0,1,     #pinky_03_r     s1,  ,
                       .5,0,0,1, #thigh_l        s1,tw,s2
                       -.2,1,     #calf_l         s1,  ,
                       -1,0,1,   #foot_l         s1,  ,s2
                       0,0,1,   #ball_l         s1,tw,
                       .5,0,0,1, #thigh_r        s1,tw,s2
                       -.2,1,     #calf_r         s1,  ,
                       -1,0,1,   #foot_r         s1,  ,s2
                       0,0,1,   #ball_r         s1,tw,
                       ]

            """
            if i % 1 == 0:
                printableCommandQuat = eulerToQuat(1.57080*command[13], 0.872665*command[14], 1.187304*command[15])
                print ("===================================\ncEuler: " +\
                       '%10f' % (1.57080*command[13]) + ", " +\
                       '%10f' % (0.872665*command[14]) + ", " +\
                       '%10f' % (1.187304*command[15]) +\
                       "\tcQuat: X=" + '%10f' % printableCommandQuat[0] +\
                       ", Y=" + '%10f' % printableCommandQuat[1] +\
                       ", Z=" + '%10f' % printableCommandQuat[2] +\
                       ", W=" + '%10f' % printableCommandQuat[3] + "\n" + "===================================")"""
            
                
            sendAndroidCommand(command, agent)
            time.sleep(.1)

        #time.sleep(100)
        print ("Killing the Android")
        agent.kill()
        print ("Android killed.")

    def sendAndroidCommand(cmd_v, agent):#cmd_v is the commandVector.
        #Each of the 122 values is between -1 and 1
        force = 3000000
        finger_force = 30000
        foot_force = 3000000
        leg_force = 3000000
        agent.command()\
            .setBoneConstraint("head",\
                                cmd_v[0],\
                                cmd_v[1],\
                                cmd_v[2],\
                                0,\
                                cmd_v[3])\
            .setBoneConstraint("neck_01",\
                                cmd_v[4],\
                                0,\
                                0,\
                                0,\
                                cmd_v[5])\
            .setBoneConstraint("spine_02",\
                                0,\
                                cmd_v[6],\
                                cmd_v[7],\
                                0,\
                                cmd_v[8])\
            .setBoneConstraint("spine_01",\
                                cmd_v[9],\
                                cmd_v[10],\
                                cmd_v[11],\
                                0,\
                                cmd_v[12])\
            .setBoneConstraint("upperarm_l",\
                                cmd_v[13],
                                cmd_v[14],
                                cmd_v[15],
                                0,\
                                cmd_v[16])\
            .setBoneConstraint("lowerarm_l",\
                                cmd_v[17],\
                                0,\
                                0,\
                                0,\
                                cmd_v[18])\
            .setBoneConstraint("hand_l",\
                                cmd_v[19],\
                                cmd_v[20],\
                                cmd_v[21],\
                                0,\
                                cmd_v[22])\
            .setBoneConstraint("thumb_01_l",\
                                cmd_v[23],\
                                0,\
                                cmd_v[24],\
                                0,\
                                cmd_v[25])\
            .setBoneConstraint("thumb_02_l",\
                                cmd_v[26],\
                                0,\
                                0,\
                                0,\
                                cmd_v[27])\
            .setBoneConstraint("thumb_03_l",\
                                cmd_v[28],\
                                0,\
                                0,\
                                0,\
                                cmd_v[29])\
            .setBoneConstraint("index_01_l",\
                                cmd_v[30],\
                                0,\
                                cmd_v[31],\
                                0,\
                                cmd_v[32])\
            .setBoneConstraint("index_02_l",\
                                cmd_v[33],\
                                0,\
                                0,\
                                0,\
                                cmd_v[34])\
            .setBoneConstraint("index_03_l",\
                                cmd_v[35],\
                                0,\
                                0,\
                                0,\
                                cmd_v[36])\
            .setBoneConstraint("middle_01_l",\
                                cmd_v[37],\
                                0,\
                                cmd_v[38],\
                                0,\
                                cmd_v[39])\
            .setBoneConstraint("middle_02_l",\
                                cmd_v[40],\
                                0,\
                                0,\
                                0,\
                                cmd_v[41])\
            .setBoneConstraint("middle_03_l",\
                                cmd_v[42],\
                                0,\
                                0,\
                                0,\
                                cmd_v[43])\
            .setBoneConstraint("ring_01_l",\
                                cmd_v[44],\
                                0,\
                                cmd_v[45],\
                                0,\
                                cmd_v[46])\
            .setBoneConstraint("ring_02_l",\
                                cmd_v[47],\
                                0,\
                                0,\
                                0,\
                                cmd_v[48])\
            .setBoneConstraint("ring_03_l",\
                                cmd_v[49],\
                                0,\
                                0,\
                                0,\
                                cmd_v[50])\
            .setBoneConstraint("pinky_01_l",\
                                cmd_v[51],\
                                0,\
                                cmd_v[52],\
                                0,\
                                cmd_v[53])\
            .setBoneConstraint("pinky_02_l",\
                                cmd_v[54],\
                                0,\
                                0,\
                                0,\
                                cmd_v[55])\
            .setBoneConstraint("pinky_03_l",\
                                cmd_v[56],\
                                0,\
                                0,\
                                0,\
                                cmd_v[57])\
            .setBoneConstraint("upperarm_r",\
                                cmd_v[58],\
                                cmd_v[59],\
                                cmd_v[60],\
                                0,\
                                cmd_v[61])\
            .setBoneConstraint("lowerarm_r",\
                                cmd_v[62],\
                                0,\
                                0,\
                                0,\
                                cmd_v[63])\
            .setBoneConstraint("hand_r",\
                                cmd_v[64],\
                                cmd_v[65],\
                                cmd_v[66],\
                                0,\
                                cmd_v[67])\
            .setBoneConstraint("thumb_01_r",\
                                cmd_v[68],\
                                0,\
                                cmd_v[69],\
                                0,\
                                cmd_v[70])\
            .setBoneConstraint("thumb_02_r",\
                                cmd_v[71],\
                                0,\
                                0,\
                                0,\
                                cmd_v[72])\
            .setBoneConstraint("thumb_03_r",\
                                cmd_v[73],\
                                0,\
                                0,\
                                0,\
                                cmd_v[74])\
            .setBoneConstraint("index_01_r",\
                                cmd_v[75],\
                                0,\
                                cmd_v[76],\
                                0,\
                                cmd_v[77])\
            .setBoneConstraint("index_02_r",\
                                cmd_v[78],\
                                0,\
                                0,\
                                0,\
                                cmd_v[79])\
            .setBoneConstraint("index_03_r",\
                                cmd_v[80],\
                                0,\
                                0,\
                                0,\
                                cmd_v[81])\
            .setBoneConstraint("middle_01_r",\
                                cmd_v[82],\
                                0,\
                                cmd_v[83],\
                                0,\
                                cmd_v[84])\
            .setBoneConstraint("middle_02_r",\
                                cmd_v[85],\
                                0,\
                                0,\
                                0,\
                                cmd_v[86])\
            .setBoneConstraint("middle_03_r",\
                                cmd_v[87],\
                                0,\
                                0,\
                                0,\
                                cmd_v[88])\
            .setBoneConstraint("ring_01_r",\
                                cmd_v[89],\
                                0,\
                                cmd_v[90],\
                                0,\
                                cmd_v[91])\
            .setBoneConstraint("ring_02_r",\
                                cmd_v[92],\
                                0,\
                                0,\
                                0,\
                                cmd_v[93])\
            .setBoneConstraint("ring_03_r",\
                                cmd_v[94],\
                                0,\
                                0,\
                                0,\
                                cmd_v[95])\
            .setBoneConstraint("pinky_01_r",\
                                cmd_v[96],\
                                0,\
                                cmd_v[97],\
                                0,\
                                cmd_v[98])\
            .setBoneConstraint("pinky_02_r",\
                                cmd_v[99],\
                                0,\
                                0,\
                                0,\
                                cmd_v[100])\
            .setBoneConstraint("pinky_03_r",\
                                cmd_v[101],\
                                0,\
                                0,\
                                0,\
                                cmd_v[102])\
            .setBoneConstraint("thigh_l",\
                                cmd_v[103],\
                                cmd_v[104],\
                                cmd_v[105],\
                                0,\
                                cmd_v[106])\
            .setBoneConstraint("calf_l",\
                                cmd_v[107],\
                                0,\
                                0,\
                                0,\
                                cmd_v[108])\
            .setBoneConstraint("foot_l",\
                                cmd_v[109],\
                                0,\
                                cmd_v[110],\
                                0,\
                                cmd_v[111])\
            .setBoneConstraint("ball_l",\
                                cmd_v[112],\
                                cmd_v[113],\
                                0,\
                                0,\
                                cmd_v[114])\
            .setBoneConstraint("thigh_r",\
                                cmd_v[115],\
                                cmd_v[116],\
                                cmd_v[117],\
                                0,\
                                cmd_v[118])\
            .setBoneConstraint("calf_r",\
                                cmd_v[119],\
                                0,\
                                0,\
                                0,\
                                cmd_v[120])\
            .setBoneConstraint("foot_r",\
                                cmd_v[121],\
                                0,\
                                cmd_v[122],\
                                0,\
                                cmd_v[123])\
            .setBoneConstraint("ball_r",\
                                cmd_v[124],\
                                cmd_v[125],\
                                0,\
                                0,\
                                cmd_v[126])\
            .send()



    #positive means the android is falling backwards, negative means the android is falling foreward.
    def swing_arms_to_balance(speed):
        current_armswing_position = get_armswing_position()
        new_armswing_position = (current_armswing_position + speed)%(4*math.pi)
        set_armswing_position(new_armswing_position)
        return [math.cos(new_armswing_position),0,math.sin(new_armswing_position)]


    def uav():
        print ("Starting and waiting for UAV to connect...")
        agent = Holodeck.UAVAgent(hostname="localhost", port=8989, agentName="UAV").waitFor("Connect")
        print ("Connected to UAV.")
        # Note: this command will affect ALL agents in the world
        print ("Setting the simulator to not pause at all after a command")
        agent.worldCommand()\
            .setAllowedTicksBetweenCommands(0)\
            .send()

        def onCamera(data):
            print (data)

        # Subscribe the function onCamera to the CameraSensorArray2D sensor messages
        agent.subscribe("CameraSensorArray2D", onCamera)

        for _ in range(10):
            print ("Commanding the UAV to rotate")
            agent.command()\
                .setLocalRotation(5,5,5)\
                .send()
            time.sleep(1)

        print ("Killing the UAV")
        agent.kill()
        print ("UAV killed.")

    android()
    #uav()
