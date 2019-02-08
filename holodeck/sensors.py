"""Definition of all of the sensor information"""
import numpy as np
from holodeck.command import *


class SensorDefinition(object):

    def __init__(self, agent_name, sensor_name, sensor_type):
        self.agent_name = agent_name
        self.sensor_name = sensor_name
        self.type = sensor_type


class HolodeckSensor(object):

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

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [2]


class ViewportCapture(HolodeckSensor):

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

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3, 3]


class IMUSensor(HolodeckSensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [2, 3]


class JointRotationSensor(HolodeckSensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [94]


class RelativeSkeletalPositionSensor(HolodeckSensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [67, 4]


class LocationSensor(HolodeckSensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class RotationSensor(HolodeckSensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class VelocitySensor(HolodeckSensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [3]


class CollisionSensor(HolodeckSensor):

    @property
    def dtype(self):
        return np.bool

    @property
    def data_shape(self):
        return [1]


class PressureSensor(HolodeckSensor):

    @property
    def dtype(self):
        return np.float32

    @property
    def data_shape(self):
        return [48*(3+1)]


class SensorFactory(object):

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

    @staticmethod
    def _default_name(sensor_type):
        for k, v in SensorFactory.__sensor_keys__.items():
            if v is sensor_type:
                return k

    @staticmethod
    def build_sensor(client, sensor_def):
        if isinstance(sensor_def.type, str):
            sensor_def.type = SensorFactory.__sensor_keys__[sensor_def.type]
        if sensor_def.sensor_name is None:
            sensor_def.sensor_name = SensorFactory._default_name(sensor_def.type)

        return sensor_def.type(client, sensor_def.agent_name, sensor_def.sensor_name)
