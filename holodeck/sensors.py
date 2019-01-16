"""Definition of all of the sensor information"""
import numpy as np
from holodeck.exceptions import HolodeckException
from holodeck.sensors import *


class SensorDef(object):

    def __init__(self, agent_name, sensor_name, sensor_type):
        self.agent_name = agent_name
        self.sensor_name = sensor_name
        self.type = sensor_type


class SensorFactory(object):

    __sensor_keys__ = {"RGBCamera": RGBCamera,
                       "Terminal": Terminal,
                       "Reward": Reward,
                       "ViewportCapture": ViewportCapture,
                       "OrientationSensor": OrientationSensor,
                       "IMUSensor": IMUSensor,
                       "JointRotationSensor": JointRotationSensor,
                       "RelativeSkeletalPositionSensor": RelativeSkeletalPositionSensor,
                       "Location": LocationSensor,
                       "RotationSensor": RotationSensor,
                       "VelocitySensor": VelocitySensor,
                       "PressureSensor": PressureSensor,
                       "ColisionSensor": CollisionSensor}

    __default_names__ = {v: k for k, v in __sensor_keys__.items()}

    @staticmethod
    def build_sensor(client, sensor_def):
        if sensor_def.sensor_name is None:
            sensor_def.name = SensorFactory.__default_names__[sensor_def.type]
        if isinstance(sensor_def.type, str):
            sensor_def.type = SensorFactory.__sensor_keys__[sensor_def.type]

        return sensor_def.type(client, sensor_def.agent_name, sensor_def.sensor_name)


class Sensor(object):

    def __init__(self, client, agent_name=None, name="DefaultSensor"):
        self.name = name
        self._client = client
        self.agent_name = agent_name
        self._buffer_name = self.agent_name + "_" + self.name

        self._on_bool_buffer = self._client.malloc(self._buffer_name + "_sensor_on_flag", [1], np.uint8)
        self._sensor_data_buffer = self._client.malloc(self._buffer_name + "_sensor_data", self.data_shape, self.dtype)

    def set_sensor_enable(self, enable):
        self._on_bool_buffer = enable

    @property
    def dtype(self):
        """The type of data in the sensor

        Returns:
            numpy dtype of sensor data
        """
        raise NotImplementedError("Child class must implement this property")

    @property
    def data_shape(self):
        """The shape of the sensor data

        Returns:
            tuple representing sensor data shape
        """
        raise NotImplementedError("Child class must implement this property")


class Terminal(Sensor):

    @property
    def dtype(self):
        return np.bool

    @property
    def data_shape(self):
        return [1]


class Reward(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [1]


class ViewportCapture(Sensor):

    def __init__(self, client, name="ViewportCapture", shape=(512, 512, 4)):
        super(ViewportCapture, self).__init__(client, name=name)
        self.shape = shape

    @property
    def dtype(self):
        return np.uint8

    @property
    def data_shape(self):
        return self.shape


class RGBCamera(Sensor):

    def __init__(self, client, name="ViewportCapture", shape=(256, 256, 4)):
        super(RGBCamera, self).__init__(client, name=name)
        self.shape = shape

    @property
    def dtype(self):
        return np.uint8

    @property
    def data_shape(self):
        return self.shape


class OrientationSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3, 3]


class IMUSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [2, 3]


class JointRotationSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [94]


class RelativeSkeletalPositionSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [67, 4]


class LocationSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class RotationSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class VelocitySensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class CollisionSensor(Sensor):

    @property
    def dtype(self):
        return np.bool

    @property
    def data_shape(self):
        return [1]


class PressureSensor(Sensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [48*(3+1)]

    @staticmethod
    def shape(sensor_type):
        """Gets the shape of a particular sensor.

        Args:
            sensor_type (int): The type of the sensor.

        Returns:
            List of int: The shape of the sensor data.
        """
        return Sensors._shape_dict[sensor_type] if sensor_type in Sensors._shape_dict else None

    @staticmethod
    def name(sensor_type):
        """Gets the human readable name for a sensor.

        Args:
            sensor_type (int): The type of the sensor.

        Returns:
            str: The name of the sensor.
        """
        return Sensors._name_dict[sensor_type] if sensor_type in Sensors._name_dict else None

    @staticmethod
    def dtype(sensor_type):
        """Gets the data type of the sensor data (the dtype of the numpy array).

        Args:
            sensor_type (int): The type of the sensor.

        Returns:
            type: The type of the sensor data.
        """
        return Sensors._type_dict[sensor_type] if sensor_type in Sensors._type_dict else None

    @staticmethod
    def name_to_sensor(sensor_name):
        """Gets the index value of a sensor from its human readable name.

        Args:
            sensor_name (str): The human readable name of the sensor.

        Returns:
            int: The index value for the sensor.
        """
        if sensor_name in Sensors._reverse_name_dict:
            return Sensors._reverse_name_dict[sensor_name]
        else:
            raise HolodeckException(
                "Unable to find sensor ID for '{}', are your binaries out of date?".format(sensor_name)
                )


    @staticmethod
    def set_primary_cam_size(height, width):
        """Sets the primary camera size for this world. Should only be called by environment.

        Args:
            height (int): New height value.
            width (int): New width value.
        """
        Sensors._shape_dict[Sensors.VIEWPORT_CAPTURE] = [height, width, 4]

    @staticmethod
    def set_pixel_cam_size(height, width):
        """Sets the pixel camera size for this world. Should only be called by Environment.

        Args:
            height (int): New height value.
            width (int): New width value.
        """
        Sensors._shape_dict[Sensors.RGB_CAMERA] = [height, width, 4]

    def __init__(self):
        print("No point in instantiating an object.")
