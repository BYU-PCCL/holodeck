# Sensors

## Types
Currently in Holodeck we have the following sensors:
* [UHolodeckSensor](#uholodecksensor) - abstract base class for sensors in holodeck
* [UHolodeckViewportClientPublisher](#uholodeckviewportclientpublisher)- publishes data from the main camera (doesn't work in editor)
* [UPixelCamera](#upixelcamera) - small camera sensors that can be attached to agents
* [UIMUSensor](#uimusensor) - an 'inertial measurement unit' which measures forces and angular rates
* [UJointRotationSensor](#ujointrotationsensor) - a sensor for the Android agent which returns the rotations of all joints
* [UOrientationSensor](#uorientationsensor) - a sensor which gives forward, right, and up vectors for a static mesh
* [UPressureSensor](#upressuresensor) - a sensor which returns the location and force that the Android is touching something
* [URelativeSkeletalPositionSensor](#urelativeskeletalpositionsensor) - 

## UHolodeckSensor
UHolodeckSensor is the abstract base class for all other sensors.
It handles the publishing of sensor data.

Member Variables:
* Controller - the AHolodeckPawnController for this agent. It is looked for at begin play.
* ResultData - FHolodeckSensorData, the data which will be published

To extend this base class:
* Override SetDataType - e.g. `ResultData.Type = "IMUSensor";`
* Override TickSensorComponent - This is primary tick function for sensors, instead of TickComponent, which cannot be overridden.
* Ensure that in BeginPlay you call `Super::BeginPlay();`

## UHolodeckViewportClientPublisher
To get in python, add "PrimaryPlayerCamera" to state_sensors.
Attach UHolodeckViewportClientPublisher to an agent, and set the viewport for your project to be HolodeckViewport.
The returned image is whatever resolution you load your project in.

## UPixelCamera
This is a sensor that can be added to an agent to capture it's view. Just attach it and position it on your agent.

Default capture resolution si 256x256. Higher resolutions are possible, but greatly slow down Holodeck.

To access this sensor from python, add "PixelCamera" to the state_sensors. This will return 256x256x4 numpy array corresponding to the RGBA channels.

## UIMUSensor
An intertial measurement unit.
Returns a 1D numpy array of:
`[acceleration_x, acceleration_y, acceleration_z, velocity_roll, velocity_pitch, velocity_yaw]`
To access this sensor from python, add "IMUSensor" to the state_sensors.

## UJointRotationSensor
Only supported for the android agent. Returns a vector of length 94 for 48 joints. 
There are 18 joints with 3 DOF, 10 with 2 DOF, and 20 with 1 DOF.
The joints are returned in the following order:
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
To access this sensor from python, add "JointRotationSensor" to the state_sensors.

## UOrientationSensor
UOrientationSensor gets the forward, right, and up vector for whatever element it is attached to.
MUST be attached to a static mesh.
Returns a 2D numpy array of:
```
[[forward_x, forward_y, forward_z],
[right_x, right_y, right_z],
[up_x, up_y, up_z]]
Shape = [3, 3]
```
To access this sensor from python, add "OrientationSensor" to the state_sensors.

## UPressureSensor
Currently only supported for Android.
Returns a length 192 vector containing the [X_loc,Y_loc,Z_loc,Force] values for each of 48 joints. The order is the same as for the Joint Rotation Sensor above.

## URelativeSkeletalPositionSensor
Gets the position of each bone as a quaternion. Can be attached to any skeletal mesh.
The returned shape is [67, 4] for the android.
To use in python, add "RelativeSkeletalPositionSensor" to the state_sensors
