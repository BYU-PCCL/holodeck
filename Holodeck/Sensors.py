import numpy as np


class Sensors:
    TERMINAL = 1
    REWARD = 2
    PRIMARY_PLAYER_CAMERA = 3   # default is 512 x 512 RGBA
    CAMERA_SENSOR_ARRAY_2D = 4  # default is 512 x 512 RGBA
    ORIENTATION_SENSOR = 5
    IMU_SENSOR = 6
    JOINT_ROTATION_SENSOR = 7
    RELATIVE_SKELETAL_POSITION_SENSOR = 8
    LOCATION_SENSOR = 9
    VELOCITY_SENSOR = 10

    # Sizes are the number of entries in the numpy array
    _shape_dict = {
        TERMINAL: [1],
        REWARD: [1],
        PRIMARY_PLAYER_CAMERA: [512, 512, 4],
        CAMERA_SENSOR_ARRAY_2D: [512, 512, 4],
        ORIENTATION_SENSOR: [3, 3],
        IMU_SENSOR: [6, 1],
        JOINT_ROTATION_SENSOR: [79, 1],
        RELATIVE_SKELETAL_POSITION_SENSOR: [67, 4],
        LOCATION_SENSOR: [3, 1],
        VELOCITY_SENSOR: [3, 1],
    }

    _type_dict = {
        TERMINAL: np.bool,
        REWARD: np.float32,
        PRIMARY_PLAYER_CAMERA: np.uint8,
        CAMERA_SENSOR_ARRAY_2D: np.float32,
        ORIENTATION_SENSOR: np.float32,
        IMU_SENSOR: np.float32,
        JOINT_ROTATION_SENSOR: np.float32,
        RELATIVE_SKELETAL_POSITION_SENSOR: np.float32,
        LOCATION_SENSOR: np.float32,
        VELOCITY_SENSOR: np.float32,
    }

    _name_dict = {
        TERMINAL: "Terminal",
        REWARD: "Reward",
        PRIMARY_PLAYER_CAMERA: "PrimaryPlayerCamera",
        CAMERA_SENSOR_ARRAY_2D: "CameraSensorArray2D",
        ORIENTATION_SENSOR: "OrientationSensor",
        IMU_SENSOR: "IMUSensor",
        JOINT_ROTATION_SENSOR: "JointRotationSensor",
        RELATIVE_SKELETAL_POSITION_SENSOR: "RelativeSkeletalPositionSensor",
        LOCATION_SENSOR: "LocationSensor",
        VELOCITY_SENSOR: "VelocitySensor",
    }

    _reverse_name_dict = {v: k for k, v in _name_dict.items()}

    @staticmethod
    def shape(sensor_type):
        return Sensors._shape_dict[sensor_type] if sensor_type in Sensors._shape_dict else None

    @staticmethod
    def name(sensor_type):
        return Sensors._name_dict[sensor_type] if sensor_type in Sensors._name_dict else None

    @staticmethod
    def dtype(sensor_type):
        return Sensors._type_dict[sensor_type] if sensor_type in Sensors._type_dict else None

    @staticmethod
    def name_to_sensor(sensor_name):
        return Sensors._reverse_name_dict[sensor_name] if sensor_name in Sensors._reverse_name_dict else None

    def __init__(self):
        print("No point in instantiating an object.")
