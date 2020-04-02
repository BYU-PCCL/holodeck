"""Definition of all of the sensor information"""
import json

import numpy as np
import holodeck

from holodeck.command import RGBCameraRateCommand, RotateSensorCommand, CustomCommand
from holodeck.exceptions import HolodeckConfigurationException


class HolodeckSensor:
    """Base class for a sensor

    Args:
        client (:class:`~holodeck.holodeckclient.HolodeckClient`): Client
            attached to a sensor
        agent_name (:obj:`str`): Name of the parent agent
        agent_type (:obj:`str`): Type of the parent agent
        name (:obj:`str`): Name of the sensor
        config (:obj:`dict`): Configuration dictionary to pass to the engine
    """
    default_config = {}

    def __init__(self, client, agent_name=None, agent_type=None,
                    name="DefaultSensor", config=None):
        self.name = name
        self._client = client
        self.agent_name = agent_name
        self.agent_type = agent_type
        self._buffer_name = self.agent_name + "_" + self.name

        self._sensor_data_buffer = \
            self._client.malloc(self._buffer_name + "_sensor_data",
                                self.data_shape, self.dtype)

        self.config = {} if config is None else config

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

    def rotate(self, rotation):
        """Rotate the sensor. It will be applied in approximately three ticks.
        :meth:`~holodeck.environments.HolodeckEnvironment.step` or
        :meth:`~holodeck.environments.HolodeckEnvironment.tick`.)

        This will not persist after a call to reset(). If you want a persistent rotation for a sensor,
        specify it in your scenario configuration.

        Args:
            rotation (:obj:`list` of :obj:`float`): rotation for sensor (see :ref:`rotations`).
        """
        command_to_send = RotateSensorCommand(self.agent_name, self.name, rotation)
        self._client.command_center.enqueue_command(command_to_send)


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


class AvoidTask(HolodeckSensor):

    sensor_type = "AvoidTask"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [2]


class CupGameTask(HolodeckSensor):
    sensor_type = "CupGameTask"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [2]

    def start_game(self, num_shuffles, speed=3, seed=None):
        """Start the cup game and set its configuration. Do not call if the config file contains a cup task configuration
        block, as it will override the configuration and cause undefined behavior.

        Args:
            num_shuffles (:obj:`int`): Number of shuffles
            speed (:obj:`int`): Speed of the shuffle. Works best between 1-10
            seed (:obj:`int`): Seed to rotate the cups the same way every time. If none is given, a seed will not be used.
        """
        use_seed = seed is not None
        if seed is None:
            seed = 0  # have to pass a value
        config_command = CustomCommand("CupGameConfig", num_params=[speed, num_shuffles, int(use_seed), seed])
        start_command = CustomCommand("StartCupGame")
        self._client.command_center.enqueue_command(config_command)
        self._client.command_center.enqueue_command(start_command)


class CleanUpTask(HolodeckSensor):
    sensor_type = "CleanUpTask"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [2]

    def start_task(self, num_trash, use_table=False):
        """Spawn trash around the trash can. Do not call if the config file contains a clean up task configuration
        block.

        Args:
            num_trash (:obj:`int`): Amount of trash to spawn
            use_table (:obj:`bool`, optional): If True a table will spawn next to the trash can, all trash will be on
                the table, and the trash can lid will be absent. This makes the task significantly easier. If False,
                all trash will spawn on the ground. Defaults to False.
        """

        if self.config is not None or self.config is not {}:
            raise HolodeckConfigurationException("Called CleanUpTask start_task when configuration block already \
                specified. Must remove configuration block before calling.")

        config_command = CustomCommand("CleanUpConfig", num_params=[num_trash, int(use_table)])
        self._client.command_center.enqueue_command(config_command)


class ViewportCapture(HolodeckSensor):
    """Captures what the viewport is seeing.

    The ViewportCapture is faster than the RGB camera, but there can only be one camera
    and it must capture what the viewport is capturing. If performance is
    critical, consider this camera instead of the RGBCamera.
    
    It may be useful
    to position the camera with
    :meth:`~holodeck.environments.HolodeckEnvironment.teleport_camera`.

    **Configuration**

    The ``configuration`` block (see :ref:`configuration-block`) accepts the following
    options:

    - ``CaptureWidth``: Width of captured image
    - ``CaptureHeight``: Height of captured image

    **THESE DIMENSIONS MUST MATCH THE VIEWPORT DIMENSTIONS**

    If you have configured the size of the  viewport (``window_height/width``), you must
    make sure that ``CaptureWidth/Height`` of this configuration block is set to the same
    dimensions.

    The default resolution is ``1280x720``, matching the default Viewport resolution.
    """
    sensor_type = "ViewportCapture"

    def __init__(self, client, agent_name, agent_type,
                 name="ViewportCapture", config=None):

        self.config = {} if config is None else config
        
        width = 1280
        height = 720

        if "CaptureHeight" in self.config:
            height = self.config["CaptureHeight"]

        if "CaptureWidth" in self.config:
            width = self.config["CaptureWidth"]

        self.shape = (height, width, 4)

        super(ViewportCapture, self).__init__(client, agent_name, agent_type, name=name, config=config)

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

    """

    sensor_type = "RGBCamera"

    def __init__(self, client, agent_name, agent_type, name="RGBCamera",  config=None):

        self.config = {} if config is None else config

        width = 256
        height = 256

        if "CaptureHeight" in self.config:
            height = self.config["CaptureHeight"]

        if "CaptureWidth" in self.config:
            width = self.config["CaptureWidth"]

        self.shape = (height, width, 4)

        super(RGBCamera, self).__init__(client, agent_name, agent_type, name=name, config=config)

    @property
    def dtype(self):
        return np.uint8

    @property
    def data_shape(self):
        return self.shape

    def set_ticks_per_capture(self, ticks_per_capture):
        """Sets this RGBCamera to capture a new frame every ticks_per_capture.

        The sensor's image will remain unchanged between captures.

        This method must be called after every call to env.reset.

        Args:
            ticks_per_capture (:obj:`int`): The amount of ticks to wait between camera captures.
        """
        if not isinstance(ticks_per_capture, int) or ticks_per_capture < 1:
            raise HolodeckConfigurationException("Invalid ticks_per_capture value " + str(ticks_per_capture))

        command_to_send = RGBCameraRateCommand(self.agent_name, self.name, ticks_per_capture)
        self._client.command_center.enqueue_command(command_to_send)

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

    ::`

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
    """Returns the state of the :class:`~holodeck.agents.AndroidAgent`'s or the 
    :class:`~holodeck.agents.HandAgent`'s joints.

    See :ref:`android-joints` or :ref:`hand-joints` for the indexes into this vector.

    """

    sensor_type = "JointRotationSensor"

    def __init__(self, client, agent_name, agent_type, name="RGBCamera", config=None):
        if holodeck.agents.AndroidAgent.agent_type in agent_type:
            # Should match AAndroid::TOTAL_DOF
            self.elements = 94
        elif agent_type == holodeck.agents.HandAgent.agent_type:
            # AHandAgent::TOTAL_JOINT_DOF
            self.elements = 23
        else:
            raise HolodeckConfigurationException("Attempting to use JointRotationSensor with unsupported" \
                                                 "agent type '{}'!".format(agent_type))

        super(JointRotationSensor, self).__init__(client, agent_name, agent_type, name, config)

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [self.elements]


class PressureSensor(HolodeckSensor):
    """For each joint on the :class:`~holodeck.agents.AndroidAgent` or the 
    :class:`~holodeck.agents.HandAgent`, returns the pressure on the
    joint.

    For each joint, returns ``[x_loc, y_loc, z_loc, force]``, in the order the joints are listed
    in :ref:`android-joints` or :ref:`hand-joints`.

    """

    sensor_type = "PressureSensor"

    def __init__(self, client, agent_name, agent_type, name="RGBCamera", config=None):
        if holodeck.agents.AndroidAgent.agent_type in agent_type:
            # Should match AAndroid::NUM_JOINTS
            self.elements = 48
        elif agent_type == holodeck.agents.HandAgent.agent_type:
            # AHandAgent::NUM_JOINTS
            self.elements = 16
        else:
            raise HolodeckConfigurationException("Attempting to use PressureSensor with unsupported" \
                                                 "agent type '{}'!".format(agent_type))

        super(PressureSensor, self).__init__(client, agent_name, agent_type, name, config)

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [self.elements*(3+1)]


class RelativeSkeletalPositionSensor(HolodeckSensor):
    """Gets the position of each bone in a skeletal mesh as a quaternion.

    Returns a numpy array with four entries for each bone (see 
    :ref:`android-bones` or :ref:`hand-bones` for the order used)
    """

    def __init__(self, client, agent_name, agent_type, name="RGBCamera", config=None):
        if holodeck.agents.AndroidAgent.agent_type in agent_type:
            # Should match AAndroid::NumBones
            self.elements = 60
        elif agent_type == holodeck.agents.HandAgent.agent_type:
            # AHandAgent::NumBones
            self.elements = 17
        else:
            raise HolodeckConfigurationException("Attempting to use RelativeSkeletalPositionSensor with unsupported" \
                                                 "agent type {}!".format(agent_type))
        super(RelativeSkeletalPositionSensor, self).__init__(client, agent_name, agent_type, name, config)

    sensor_type = "RelativeSkeletalPositionSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [self.elements, 4]


class LocationSensor(HolodeckSensor):
    """Gets the location of the agent in the world.

    Returns coordinates in ``[x, y, z]`` format (see :ref:`coordinate-system`)
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

    Returns ``[roll, pitch, yaw]`` (see :ref:`rotations`)
    """
    sensor_type = "RotationSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class VelocitySensor(HolodeckSensor):
    """Returns the x, y, and z velocity of the agent.
    
    """
    sensor_type = "VelocitySensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class CollisionSensor(HolodeckSensor):
    """Returns true if the agent is colliding with anything (including the ground).
    
    """

    sensor_type = "CollisionSensor"

    @property
    def dtype(self):
        return np.bool

    @property
    def data_shape(self):
        return [1]


class RangeFinderSensor(HolodeckSensor):
    """Returns distances to nearest collisions in the directions specified by
    the parameters. For example, if an agent had two range sensors at different
    angles with 24 lasers each, the LaserDebug traces would look something like
    this:

    .. image:: ../../docs/images/UAVRangeFinder.PNG

    **Configuration**

    The ``configuration`` block (see :ref:`configuration-block`) accepts the
    following options:

    - ``LaserMaxDistance``: Max Distance in meters of RangeFinder. (default 10)
    - ``LaserCount``: Number of lasers in sensor. (default 1)
    - ``LaserAngle``: Angle of lasers from origin. Measured in degrees. Positive angles point up. (default 0)
    - ``LaserDebug``: Show debug traces. (default false)
    """

    sensor_type = "RangeFinderSensor"
    
    def __init__(self, client, agent_name, agent_type, 
                 name="RangeFinderSensor", config=None):

        config = {} if config is None else config
        self.laser_count = config["LaserCount"] if "LaserCount" in config else 1

        super().__init__(client, agent_name, agent_type, name, config)

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [self.laser_count]


class WorldNumSensor(HolodeckSensor):
    """Returns any numeric value from the world corresponding to a given key. This is
    world specific.

    """

    sensor_type = "WorldNumSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [1]


class BallLocationSensor(WorldNumSensor):
    """For the CupGame task, returns which cup the ball is underneath.
    
    The cups are numbered 0-2, from the agents perspective, left to right. As soon
    as a swap begins, the number returned by this sensor is updated to the balls new
    position after the swap ends.
    
    Only works in the CupGame world.

    """

    default_config = {"Key": "BallLocation"}

    @property
    def dtype(self):
        return np.int8


class AbuseSensor(HolodeckSensor):
    """Returns True if the agent has been abused. Abuse is calculated differently for
    different agents. The Sphere and Hand agent cannot be abused. The Uav, Android,
    and Turtle agents can be abused by experiencing high levels of acceleration.
    The Uav is abused when its blades collide with another object, and the Turtle
    agent is abused when it's flipped over.

    **Configuration**

    - ``AccelerationLimit``: Maximum acceleration the agent can endure before
      being considered abused. The default depends on the agent, usually around 300 m/s^2.

    """

    sensor_type = "AbuseSensor"

    @property
    def dtype(self):
        return np.int8

    @property
    def data_shape(self):
        return [1]


class SensorDefinition:
    """A class for new sensors and their parameters, to be used for adding new sensors.

    Args:
        agent_name (:obj:`str`): The name of the parent agent.
        agent_type (:obj:`str`): The type of the parent agent
        sensor_name (:obj:`str`): The name of the sensor.
        sensor_type (:obj:`str` or :class:`HolodeckSensor`): The type of the sensor.
        socket (:obj:`str`, optional): The name of the socket to attach sensor to.
        location (Tuple of :obj:`float`, optional): ``[x, y, z]`` coordinates to place sensor
            relative to agent (or socket) (see :ref:`coordinate-system`).
        rotation (Tuple of :obj:`float`, optional): ``[roll, pitch, yaw]`` to rotate sensor
            relative to agent (see :ref:`rotations`)
        config (:obj:`dict`): Configuration dictionary for the sensor, to pass to engine
    """

    _sensor_keys_ = {
        "RGBCamera": RGBCamera,
        "DistanceTask": DistanceTask,
        "LocationTask": LocationTask,
        "FollowTask": FollowTask,
        "AvoidTask": AvoidTask,
        "CupGameTask": CupGameTask,
        "CleanUpTask": CleanUpTask,
        "ViewportCapture": ViewportCapture,
        "OrientationSensor": OrientationSensor,
        "IMUSensor": IMUSensor,
        "JointRotationSensor": JointRotationSensor,
        "RelativeSkeletalPositionSensor": RelativeSkeletalPositionSensor,
        "LocationSensor": LocationSensor,
        "RotationSensor": RotationSensor,
        "VelocitySensor": VelocitySensor,
        "PressureSensor": PressureSensor,
        "CollisionSensor": CollisionSensor,
        "RangeFinderSensor": RangeFinderSensor,
        "WorldNumSensor": WorldNumSensor,
        "BallLocationSensor": BallLocationSensor,
        "AbuseSensor": AbuseSensor,
    }

    def get_config_json_string(self):
        """Gets the configuration dictionary as a string ready for transport

        Returns:
            (:obj:`str`): The configuration as an escaped json string

        """
        param_str = json.dumps(self.config)
        # Prepare configuration string for transport to the engine
        param_str = param_str.replace("\"", "\\\"")
        return param_str

    def __init__(self, agent_name, agent_type, sensor_name, sensor_type, 
                 socket="", location=(0, 0, 0), rotation=(0, 0, 0), config=None, 
                 existing=False):
        self.agent_name = agent_name
        self.agent_type = agent_type
        self.sensor_name = sensor_name

        if isinstance(sensor_type, str):
            self.type = SensorDefinition._sensor_keys_[sensor_type]
        else:
            self.type = sensor_type

        self.socket = socket
        self.location = location
        self.rotation = rotation
        self.config = self.type.default_config if config is None else config
        self.existing = existing



class SensorFactory:
    """Given a sensor definition, constructs the appropriate HolodeckSensor object.

    """
    @staticmethod
    def _default_name(sensor_class):
        return sensor_class.sensor_type

    @staticmethod
    def build_sensor(client, sensor_def):
        """Constructs a given sensor associated with client

        Args:
            client (:obj:`str`): Name of the agent this sensor is attached to
            sensor_def (:class:`SensorDefinition`): Sensor definition to construct

        Returns:

        """
        if sensor_def.sensor_name is None:
            sensor_def.sensor_name = SensorFactory._default_name(sensor_def.type)

        return sensor_def.type(client, sensor_def.agent_name, sensor_def.agent_type,
                               sensor_def.sensor_name, config=sensor_def.config)
