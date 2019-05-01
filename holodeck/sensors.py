"""Definition of all of the sensor information"""
import numpy as np
from holodeck.command import *


class HolodeckSensor(object):
    """Base class for a sensor in Holodeck
    """
    def __init__(self, client, agent_name=None, name="DefaultSensor", custom_shape=None):
        self.name = name
        self._client = client
        self.agent_name = agent_name
        self._buffer_name = self.agent_name + "_" + self.name

        self._sensor_data_buffer = self._client.malloc(self._buffer_name + "_sensor_data", self.data_shape, self.dtype)

    def set_sensor_enable(self, enable):
        command_to_send = SetSensorEnabledCommand(self.agent_name, self.name, enable)
        self._client.command_center.enque_command(command_to_send)

    @property
    def sensor_data(self):
        return self._sensor_data_buffer

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
        self.shape = shape
        super(RGBCamera, self).__init__(client, agent_name, name=name)

    @property
    def dtype(self):
        return np.uint8

    @property
    def data_shape(self):
        return self.shape


class OrientationSensor(HolodeckSensor):

    sensor_type = "OrientationSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3, 3]


class IMUSensor(HolodeckSensor):

    sensor_type = "IMUSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [2, 3]


class JointRotationSensor(HolodeckSensor):

    sensor_type = "JointRotationSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [94]


class RelativeSkeletalPositionSensor(HolodeckSensor):

    sensor_type = "RelativeSkeletalPositionSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [67, 4]


class LocationSensor(HolodeckSensor):

    sensor_type = "LocationSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class RotationSensor(HolodeckSensor):

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

    sensor_type = "PressureSensor"

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [48*(3+1)]


class SensorDefinition(object):
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
