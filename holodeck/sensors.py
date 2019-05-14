"""Definition of all of the sensor information"""
import numpy as np
import json
from holodeck.command import *


class HolodeckSensor(object):
    """Base class for a sensor

    Args:
        client (:class:`~holodeck.holodeckclient.HolodeckClient`): Client attached to a sensor
        agent_name (:obj:`str`): Name of the agent
        name (:obj:`str`): Name of the sensor
    """
    def __init__(self, client, agent_name=None, name="DefaultSensor", config=None):
        self.name = name
        self._client = client
        self.agent_name = agent_name
        self._buffer_name = self.agent_name + "_" + self.name

        self._sensor_data_buffer = self._client.malloc(self._buffer_name + "_sensor_data", self.data_shape, self.dtype)

        self.config = {} if config is None else config

    def set_sensor_enable(self, enable):
        """Enable or disable this sensor

        Args:
            enable (:obj:`bool`): State to set sensor to

        """
        command_to_send = SetSensorEnabledCommand(self.agent_name, self.name, enable)
        self._client.command_center.enqueue_command(command_to_send)

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


class DistanceTask(HolodeckSensor):

    sensor_type = "DistanceTask"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [2]


class LocationTask(HolodeckSensor):

    sensor_type = "LocationTask"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [2]


class FollowTask(HolodeckSensor):

    sensor_type = "FollowTask"

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
    """Captures agent's view.
    
    The default capture resolution is 256x256x256x4, corresponding to the RGBA channels.
    The resolution can be increased, but will significantly impact performance.

    **Configuration**

    The ``configuration`` block (see :ref:`configuration-block`) accepts the following
    options:

    - ``CaptureWidth``: Width of captured image
    - ``CaptureHeight``: Height of captured image

    Args:
        shape (:obj:`tuple`): Dimensions of the capture

    """

    sensor_type = "RGBCamera"

    def __init__(self, client, agent_name, name="RGBCamera", width=256, height=256, config=None):

        self.config = {} if config is None else config
        
        if "CaptureHeight" in self.config:
            height = self.config["CaptureHeight"]
        
        if "CaptureWidth" in self.config:
            width = self.config["CaptureWidth"]
        

        self.shape = (height, width, 4)

        super(RGBCamera, self).__init__(client, agent_name, name=name, config=config)

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

    +-------------------------------------+-----------------------+
    | **Head, Spine, and Arm joints**                             |
    |                                                             |
    | Each has ``[swing1, swing2, twist]``                        |
    +-------------------------------------+-----------------------+
    | ``0``                               | ``head``              |
    +-------------------------------------+-----------------------+
    | ``1``                               | ``neck_01``           |
    +-------------------------------------+-----------------------+
    | ``2``                               | ``spine_02``          |
    +-------------------------------------+-----------------------+
    | ``3``                               | ``spine_01``          |
    +-------------------------------------+-----------------------+
    | ``4``                               | ``upperarm_l``        |
    +-------------------------------------+-----------------------+
    | ``5``                               | ``lowerarm_l``        |
    +-------------------------------------+-----------------------+
    | ``6``                               | ``hand_l``            |
    +-------------------------------------+-----------------------+
    | ``7``                               | ``upperarm_r``        |
    +-------------------------------------+-----------------------+
    | ``8``                               | ``lowerarm_r``        |
    +-------------------------------------+-----------------------+
    | ``9``                               | ``hand_r``            |
    +-------------------------------------+-----------------------+
    | **Leg Joints**                                              |
    |                                                             |
    | Each has ``[swing1, swing2, twist]``                        |
    +-------------------------------------+-----------------------+
    | ``10``                              | ``thigh_l``           |
    +-------------------------------------+-----------------------+
    | ``11``                              | ``calf_l``            |
    +-------------------------------------+-----------------------+
    | ``12``                              | ``foot_l``            |
    +-------------------------------------+-----------------------+
    | ``13``                              | ``ball_l``            |
    +-------------------------------------+-----------------------+
    | ``14``                              | ``thigh_r``           |
    +-------------------------------------+-----------------------+
    | ``15``                              | ``calf_r``            |
    +-------------------------------------+-----------------------+
    | ``16``                              | ``foot_r``            |
    +-------------------------------------+-----------------------+
    | ``17``                              | ``ball_r``            |
    +-------------------------------------+-----------------------+
    | **First joint of each finger**                              |
    |                                                             |
    | Has only ``[swing1, swing2]``                               |
    +-------------------------------------+-----------------------+
    | ``18``                              | ``thumb_01_l``        |
    +-------------------------------------+-----------------------+
    | ``19``                              | ``index_01_l``        |
    +-------------------------------------+-----------------------+ 
    | ``20``                              | ``middle_01_l``       |
    +-------------------------------------+-----------------------+ 
    | ``21``                              | ``ring_01_l``         |
    +-------------------------------------+-----------------------+ 
    | ``22``                              | ``pinky_01_l``        |
    +-------------------------------------+-----------------------+ 
    | ``23``                              | ``thumb_01_r``        |
    +-------------------------------------+-----------------------+ 
    | ``24``                              | ``index_01_r``        |
    +-------------------------------------+-----------------------+ 
    | ``25``                              | ``middle_01_r``       |
    +-------------------------------------+-----------------------+ 
    | ``26``                              | ``ring_01_r``         |
    +-------------------------------------+-----------------------+ 
    | ``27``                              | ``pinky_01_r``        |
    +-------------------------------------+-----------------------+ 
    | **Second joint of each finger**                             |
    |                                                             |
    | Has only ``[swing1]``                                       |
    +-------------------------------------+-----------------------+
    | ``28``                              | ``thumb_02_l``        |
    +-------------------------------------+-----------------------+
    | ``29``                              | ``index_02_l``        |
    +-------------------------------------+-----------------------+   
    | ``30``                              | ``middle_02_l``       |
    +-------------------------------------+-----------------------+ 
    | ``31``                              | ``ring_02_l``         |
    +-------------------------------------+-----------------------+ 
    | ``32``                              | ``pinky_02_l``        |
    +-------------------------------------+-----------------------+
    | ``33``                              | ``thumb_02_r``        |
    +-------------------------------------+-----------------------+
    | ``34``                              | ``index_02_r``        |
    +-------------------------------------+-----------------------+   
    | ``35``                              | ``middle_02_r``       |
    +-------------------------------------+-----------------------+
    | ``36``                              | ``ring_02_r``         |
    +-------------------------------------+-----------------------+  
    | ``37``                              | ``pinky_02_r``        |
    +-------------------------------------+-----------------------+  
    | **Third joint of each finger**                              |
    |                                                             |
    | Has only ``[swing1]``                                       |
    +-------------------------------------+-----------------------+
    | ``38``                              | ``thumb_03_l``        |
    +-------------------------------------+-----------------------+
    | ``39``                              | ``index_03_l``        |
    +-------------------------------------+-----------------------+   
    | ``40``                              | ``middle_03_l``       |
    +-------------------------------------+-----------------------+ 
    | ``41``                              | ``ring_03_l``         |
    +-------------------------------------+-----------------------+ 
    | ``42``                              | ``pinky_03_l``        |
    +-------------------------------------+-----------------------+
    | ``43``                              | ``thumb_03_r``        |
    +-------------------------------------+-----------------------+
    | ``44``                              | ``index_03_r``        |
    +-------------------------------------+-----------------------+   
    | ``45``                              | ``middle_03_r``       |
    +-------------------------------------+-----------------------+
    | ``46``                              | ``ring_03_r``         |
    +-------------------------------------+-----------------------+  
    | ``47``                              | ``pinky_03_r``        |
    +-------------------------------------+-----------------------+

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
    """A class for new sensors and their parameters, to be used for adding new sensors.
    
    Args:
        agent_name (:obj:`str`): The name of the parent agent.
        sensor_name (:obj:`str`): The name of the sensor.
        sensor_type (:obj:`str` or :class:`HolodeckSensor`): The type of the sensor.
        socket (:obj:`str`, optional): The name of the socket to attach sensor to.
        location (Tuple of :obj:`float`, optional): x, y, and z coordinates to place sensor relative to agent (or socket).
        rotation (Tuple of :obj:`float`, optional): roll, pitch, and yaw to rotate sensor relative to agent.
        config (:obj:`dict`): Configuration dictionary for the sensor, to pass to engine
    """

    _sensor_keys_ = {"RGBCamera": RGBCamera,
                     "DistanceTask": DistanceTask,
                     "LocationTask": LocationTask,
                     "FollowTask": FollowTask,
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

    def get_config_json_string(self):
        """Gets the configuration dictionary as a string ready for transport

        Returns:
            (:obj:`str`): The configuration as an escaped json string

        """
        param_str = json.dumps(self.config)
        # Prepare configuration string for transport to the engine
        param_str = param_str.replace("\"", "\\\"") 
        return param_str

    def __init__(self, agent_name, sensor_name, sensor_type, socket="", location=(0,0,0), rotation=(0,0,0), config=None, existing=False):
        self.agent_name = agent_name
        self.sensor_name = sensor_name
        self.type = SensorDefinition._sensor_keys_[sensor_type] if isinstance(sensor_type, str) else sensor_type
        self.socket = socket
        self.location = location
        self.rotation = rotation
        self.config = {} if config is None else config
        self.existing = existing


class SensorFactory(object):
    @staticmethod
    def _default_name(sensor_class):
        return sensor_class.sensor_type

    @staticmethod
    def build_sensor(client, sensor_def):
        if sensor_def.sensor_name is None:
            sensor_def.sensor_name = SensorFactory._default_name(sensor_def.type)

        return sensor_def.type(client, sensor_def.agent_name, sensor_def.sensor_name, config=sensor_def.config)
