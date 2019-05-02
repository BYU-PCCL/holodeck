"""Definition of all of the sensor information"""
import numpy as np
from holodeck.command import *


class HolodeckSensor(object):
    """Base class for a sensor

    Args:
        client (:class:`~holodeck.holodeckclient.HolodeckClient`): Client attached to a sensor
        agent_name (:obj:`str`): Name of the agent
        name (:obj:`str`): Name of the sensor
    """
    def __init__(self, client, agent_name=None, name="DefaultSensor"):
        self.name = name
        self._client = client
        self.agent_name = agent_name
        self._buffer_name = self.agent_name + "_" + self.name

        self._sensor_data_buffer = self._client.malloc(self._buffer_name + "_sensor_data", self.data_shape, self.dtype)

    def set_sensor_enable(self, enable):
        """Enable or disable this sensor

        Args:
            enable (:obj:`bool`): State to set sensor to

        """
        command_to_send = SetSensorEnabledCommand(self.agent_name, self.name, enable)
        self._client.command_center.enque_command(command_to_send)

    @property
    def sensor_data(self):
        """Get the sensor data buffer

        Returns:
            :obj:`np.ndarray` of size :obj:`self.data_shape`: Current sensor data

        """
        return self._sensor_data_buffer

    @property
    def dtype(self):
        """The type of data in the sensor

        Returns:
            numpy dtype: Type of sensor data
        """
        raise NotImplementedError("Child class must implement this property")

    @property
    def data_shape(self):
        """The shape of the sensor data

        Returns:
            :obj:`tuple`: Sensor data shape
        """
        raise NotImplementedError("Child class must implement this property")


class TaskSensor(HolodeckSensor):

    sensor_type = "TaskSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [2]


class ViewportCapture(HolodeckSensor):
    sensor_type = "ViewportCapture"

    def __init__(self, client, agent_name, name="ViewportCapture", shape=(512, 512, 4)):
        """Represents a viewport capture.

        Args:
            shape (:obj:`tuple`): Dimensions of the capture
        """
        self.shape = shape
        super(ViewportCapture, self).__init__(client, agent_name, name=name)

    @property
    def dtype(self):
        return np.uint8

    @property
    def data_shape(self):
        return self.shape


class RGBCamera(HolodeckSensor):
    sensor_type = "RGBCamera"

    def __init__(self, client, agent_name, name="RGBCamera", shape=(256, 256, 4)):
        """Captures agent's view.
        The default capture resolution is 256x256x256x4, corresponding to the RGBA channels.
        The resolution can be increased, but will significantly impact performance.

        Args:
            shape (:obj:`tuple`): Dimensions of the capture

        """
        self.shape = shape
        super(RGBCamera, self).__init__(client, agent_name, name=name)

    @property
    def dtype(self):
        return np.uint8

    @property
    def data_shape(self):
        return self.shape


class OrientationSensor(HolodeckSensor):
    """Gets the forward, right, and up vector for the agent.
    Returns a 2D numpy array of

    ::

       [ [forward_x, forward_y, forward_z],
         [right_x,   right_y,   right_z  ],
         [up_x,      up_y,      up_z     ] ]

    """

    sensor_type = "OrientationSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3, 3]


class IMUSensor(HolodeckSensor):
    """Inertial Measurement Unit sensor.

    Returns a 2D numpy array of

    ::

       [ [acceleration_x, acceleration_y, acceleration_z],
         [velocity_roll,  velocity_pitch, velocity_yaw]   ]

    """

    sensor_type = "IMUSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [2, 3]


class JointRotationSensor(HolodeckSensor):
    """Returns the state of the :class:`~holodeck.agents.AndroidAgent`'s joints.

    Is a vector of length 94 for 48 joints.

    Returned in the following order:

    ::
    
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

    """

    sensor_type = "JointRotationSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [94]


class RelativeSkeletalPositionSensor(HolodeckSensor):
    """Gets the position of each bone in a skeletal mesh as a quaternion.

    Returns a numpy array of size (67, 4)
    """

    sensor_type = "RelativeSkeletalPositionSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [67, 4]


class LocationSensor(HolodeckSensor):
    """Gets the location of the agent in the world.

    Returns a 3-tuple.
    """

    sensor_type = "LocationSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class RotationSensor(HolodeckSensor):
    """Gets the rotation of the agent in the world.

    Returns a 3-tuple.
    """
    sensor_type = "RotationSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class VelocitySensor(HolodeckSensor):

    sensor_type = "VelocitySensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class CollisionSensor(HolodeckSensor):

    sensor_type = "CollisionSensor"

    @property
    def dtype(self):
        return np.bool

    @property
    def data_shape(self):
        return [1]


class PressureSensor(HolodeckSensor):
    """For each joint on the :class:`~holodeck.agents.AndroidAgent`, returns the pressure on the joint.

    For each joint, returns ``[x_loc, y_loc, z_loc, force]``, in the order of the :class:`JointRotationSensor`.

    """

    sensor_type = "PressureSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [48*(3+1)]


class SensorDefinition(object):
    """Used to initialize the type of sensor on an agent
    """
    __sensor_keys__ = {"RGBCamera": RGBCamera,
                       "TaskSensor": TaskSensor,
                       "ViewportCapture": ViewportCapture,
                       "OrientationSensor": OrientationSensor,
                       "IMUSensor": IMUSensor,
                       "JointRotationSensor": JointRotationSensor,
                       "RelativeSkeletalPositionSensor": RelativeSkeletalPositionSensor,
                       "LocationSensor": LocationSensor,
                       "RotationSensor": RotationSensor,
                       "VelocitySensor": VelocitySensor,
                       "PressureSensor": PressureSensor,
                       "CollisionSensor": CollisionSensor}

    def __init__(self, agent_name, sensor_name, sensor_type, socket=""):
        self.agent_name = agent_name
        self.sensor_name = sensor_name
        self.type = SensorDefinition.__sensor_keys__[sensor_type] if isinstance(sensor_type, str) else sensor_type
        self.socket = socket


class SensorFactory(object):
    @staticmethod
    def _default_name(sensor_class):
        return sensor_class.sensor_type

    @staticmethod
    def build_sensor(client, sensor_def):
        if sensor_def.sensor_name is None:
            sensor_def.sensor_name = SensorFactory._default_name(sensor_def.type)

        return sensor_def.type(client, sensor_def.agent_name, sensor_def.sensor_name)
