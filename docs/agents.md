# Holodeck Agents

Each environment contains an agent, and each agent has a specific number of sensors.
The default worlds currently contain 3 supported agents:
* UAV - A quad-copter which takes as input target values for roll, pitch, yaw rate, and altitude.
* DiscreteSphere - A basic robot that moves on a plane, with four moves: forward, backward, left, and right.
* Android - A humanoid android that has a full range of joint motion with 94 degrees of freedom.

To interact with the environment, you simply call `env.step(cmd)` where cmd is a command for the specific agent.
Each agent has a different action space, which are detailed below.
The step function returns a tuple of `(state, reward, terminal, info)`.
The state is a dictionary of sensor enum to sensor value.
Reward is the reward received from the previous action, and terminal indicates whether the current state is a terminal state.
Info contains additional environment specific information.
The sensors for each agent are also indicated below.

## UAV
The UAV's action space is:
```
[roll_target, pitch_target, yaw_rate_target, altitude_target]
```
It contains the following sensors:
* PixelCamera
* OrientationSensor
* LocationSensor
* VelocitySensor
* IMUSensor


## SphereRobot
The Sphere Robot action space is:
```
[forward_speed, rot_speed]
```

It contains the following sensors:
* PixelCamera
* OrientationSensor
* LocationSensor

## NavAgent
The NavAgent is a character that given a position in the world will try to get to that position. 
It's action space is:
```
[x_pos, y_pos, z_pos]
```

It contains the following sensors:
* PixelCamera
* OrientationSensor
* LocationSensor

## Android
The Android action space is a 94 dimensional vector containing values for the torques to be applied at each of the Android's 48 joints.
There are 18 joints with 3 DOF, 10 joints with 2 DOF, and 20 joints with just 1 DOF.

The Android has the following sensors:
* PixelCamera
* OrientationSensor
* LocationSensor
* VelocitySensor
* IMUSensor
* JointRotationSensor
* PressureSensor
* RelativeSkeletalPositionSensor

The order of joints is the following:

```
// Head, Spine, and Arm joints. Each has [swing1, swing2, twist]
	FName(TEXT("head")),
	FName(TEXT("neck_01")),
	FName(TEXT("spine_02")),
	FName(TEXT("spine_01")),
	FName(TEXT("upperarm_l")),
	FName(TEXT("lowerarm_l")),
	FName(TEXT("hand_l")),
	FName(TEXT("upperarm_r")),
	FName(TEXT("lowerarm_r")),
	FName(TEXT("hand_r")),

	// Leg Joints. Each has [swing1, swing2, twist]
	FName(TEXT("thigh_l")),
	FName(TEXT("calf_l")),
	FName(TEXT("foot_l")),
	FName(TEXT("ball_l")),
	FName(TEXT("thigh_r")),
	FName(TEXT("calf_r")),
	FName(TEXT("foot_r")),
	FName(TEXT("ball_r")),

	// First joint of each finger. Has only [swing1, swing2]
	FName(TEXT("thumb_01_l")),
	FName(TEXT("index_01_l")),
	FName(TEXT("middle_01_l")),
	FName(TEXT("ring_01_l")),
	FName(TEXT("pinky_01_l")),
	FName(TEXT("thumb_01_r")),
	FName(TEXT("index_01_r")),
	FName(TEXT("middle_01_r")),
	FName(TEXT("ring_01_r")),
	FName(TEXT("pinky_01_r")),

	// Second joint of each finger. Has only [swing1]
	FName(TEXT("thumb_02_l")),
	FName(TEXT("index_02_l")),
	FName(TEXT("middle_02_l")),
	FName(TEXT("ring_02_l")),
	FName(TEXT("pinky_02_l")),
	FName(TEXT("thumb_02_r")),
	FName(TEXT("index_02_r")),
	FName(TEXT("middle_02_r")),
	FName(TEXT("ring_02_r")),
	FName(TEXT("pinky_02_r")),

	// Third joint of each finger. Has only [swing1]
	FName(TEXT("thumb_03_l")),
	FName(TEXT("index_03_l")),
	FName(TEXT("middle_03_l")),
	FName(TEXT("ring_03_l")),
	FName(TEXT("pinky_03_l")),
	FName(TEXT("thumb_03_r")),
	FName(TEXT("index_03_r")),
	FName(TEXT("middle_03_r")),
	FName(TEXT("ring_03_r")),
	FName(TEXT("pinky_03_r")),
```
