"""Definitions for different agents that can be controlled from Holodeck"""
import numpy as np
from functools import reduce

from holodeck.spaces import ContinuousActionSpace, DiscreteActionSpace
from holodeck.sensors import *
from holodeck.command import AddSensorCommand, RemoveSensorCommand


class ControlSchemes(object):
    """All allowed control schemes.

    Attributes:
        ANDROID_TORQUES (int): Default Android control scheme. Specify a torque for each joint.
        CONTINUOUS_SPHERE_DEFAULT (int): Default ContinuousSphere control scheme. Takes two commands,
            [forward_delta, turn_delta].
        DISCRETE_SPHERE_DEFAULT (int): Default DiscreteSphere control scheme. Takes a value, 0-4, which corresponds
            with forward, backward, right, and left.
        NAV_TARGET_LOCATION (int): Default NavAgent control scheme. Takes a target xyz coordinate.
        UAV_TORQUES (int): Default UAV control scheme. Takes torques for roll, pitch, and yaw, as well as thrust.
        UAV_ROLL_PITCH_YAW_RATE_ALT (int): Control scheme for UAV. Takes roll, pitch, yaw rate, and altitude targets.
    """
    # UAV Control Schemes
    ANDROID_TORQUES = 0

    # Sphere Agent Control Schemes
    SPHERE_DISCRETE = 0
    SPHERE_CONTINUOUS = 1

    # Nav Agent Control Schemes
    NAV_TARGET_LOCATION = 0

    # UAV Control Schemes
    UAV_TORQUES = 0
    UAV_ROLL_PITCH_YAW_RATE_ALT = 1


class HolodeckAgent(object):
    """Holodeck Agents are agents that can act, receive rewards, and receive observations from sensors on them.
       Examples include the Android, UAV, and SphereRobot

    Args:
        client (:obj:`HolodeckClient`): The HolodeckClient that this agent belongs with.
        name (str, optional): The name of the agent. Must be unique from other agents in the same environment.
        sensors (dict of (string, HolodeckSensor)): A list of HolodeckSensors to read from this agent.

    Attributes:
        name (str): The name of the agent.
        sensors (dict of (string, HolodeckSensor)): List of HolodeckSensors on this agent.
        agent_state_dict (dict): A dictionary that maps sensor names to sensor observation data.
    """

    def __init__(self, client, name="DefaultAgent", sensors=None):
        self.name = name
        self._client = client
        self.sensors = sensors
        self.agent_state_dict = dict()
        for _, sensor in sensors.items():
            self.agent_state_dict[sensor.name] = sensor.sensor_data

        self._num_control_schemes = len(self.control_schemes)
        self._max_control_scheme_length = max(map(lambda x: reduce(lambda i, j: i * j, x[1].buffer_shape),
                                                  self.control_schemes))

        self._action_buffer = self._client.malloc(name, [self._max_control_scheme_length], np.float32)
        # Teleport flag: 0: do nothing, 1: teleport, 2: rotate, 3: teleport and rotate
        self._teleport_type_buffer = self._client.malloc(name + "_teleport_flag", [1], np.uint8)
        self._teleport_buffer = self._client.malloc(name + "_teleport_command", [12], np.float32)
        self._control_scheme_buffer = self._client.malloc(name + "_control_scheme", [1],
                                                          np.uint8)
        self._current_control_scheme = 0
        self.set_control_scheme(0)

        self._ticks_per_capture = 1
        self.set_ticks_per_capture(1)
        self.get_ticks_per_capture()

    def act(self, action):
        """Sets the command for the agent. Action depends on the agent type and current control scheme.

        Args:
            action(np.ndarray): The action to take.
        """
        self.__act__(action)

    def set_control_scheme(self, index):
        """Sets the control scheme for the agent. See :obj:`ControlSchemes`.

        Args:
            index (int): The control scheme to use. Should be set with an enum from :obj:`ControlSchemes`.
        """
        self._current_control_scheme = index % self._num_control_schemes
        self._control_scheme_buffer[0] = self._current_control_scheme

    def set_ticks_per_capture(self, ticks_per_capture):
        """Sets the ticks per capture for the agent's rgb camera.

        Args:
            ticks_per_capture (int): The ticks per capture for the agent's rgb camera
        """
        self._ticks_per_capture = ticks_per_capture

    def get_ticks_per_capture(self):
        """Gets the ticks per capture for the agent's rgb camera.

        Returns:
            ticks_per_capture (int): The ticks per capture for the agent's rgb camera
        """
        return self._ticks_per_capture

    def teleport(self, location=None, rotation=None):
        """Teleports the agent to a specific location, with a specific rotation.

        Args:
            location (np.ndarray, optional): An array with three elements specifying the target world coordinate in meters.
            If None, keeps the current location. Defaults to None.
            rotation (np.ndarray, optional): An array with three elements specifying the target rotation of the agent.
            If None, keeps the current rotation. Defaults to None.

        Returns:
            None
        """
        val = 0
        if location is not None:
            val += 1
            np.copyto(self._teleport_buffer[0:3], location)
        if rotation is not None:
            np.copyto(self._teleport_buffer[3:6], rotation)
            val += 2
        self._teleport_type_buffer[0] = val

    def set_state(self, location, rotation, velocity, angular_velocity):
        val = 15
        np.copyto(self._teleport_buffer[0:3], location)
        np.copyto(self._teleport_buffer[3:6], rotation)
        np.copyto(self._teleport_buffer[6:9], velocity)
        np.copyto(self._teleport_buffer[9:12], angular_velocity)
        self._teleport_type_buffer[0] = val

    def add_existing_sensors(self, sensor_defs):
        """Adds a sensor to a particular agent object. This only works if the world you are running also includes
        that particular sensor on the agent.

        Args:
            sensor_defs (:obj:`HolodeckSensor` or list of :obj:`HolodeckSensor`): Sensors to add to the agent.
                Should be objects that inherit from :obj:`HolodeckSensor`.
        """
        if not isinstance(sensor_defs, list):
            sensor_defs = [sensor_defs]

        for sensor_def in sensor_defs:
            self.sensors[sensor_def.name] = SensorFactory.build_sensor(self._client, sensor_def)

    def add_new_sensors(self, sensor_defs):
        """Adds a sensor to a particular agent object and attaches an instance of the sensor to the agent in the world.

        Args:
            sensor_defs (:obj:`HolodeckSensor` or list of :obj:`HolodeckSensor`): Sensors to add to the agent.
                Should be objects that inherit from :obj:`HolodeckSensor`.
        """
        if not isinstance(sensor_defs, list):
            sensor_defs = [sensor_defs]

        for sensor_def in sensor_defs:
            sensor = SensorFactory.build_sensor(self._client, sensor_def)
            self.sensors[sensor_def.sensor_name] = sensor
            self.agent_state_dict[sensor_def.sensor_name] = sensor.sensor_data
            command_to_send = AddSensorCommand(self.name, sensor_def.sensor_name, sensor_def.type.sensor_type,
                                               socket=sensor_def.socket)
            self._client.command_center.enqueue_command(command_to_send)

    def remove_sensors(self, sensor_defs):
        """Removes a sensor from a particular agent object and detaches it from the agent in the world.

        Args:
            sensor_defs (:obj:`HolodeckSensor` or list of :obj:`HolodeckSensor`): Sensors to add to the agent.
                Should be objects that inherit from :obj:`HolodeckSensor`.
        """
        if not isinstance(sensor_defs, list):
            sensor_defs = [sensor_defs]

        for sensor_def in sensor_defs:
            self.sensors.pop(sensor_def.sensor_name, None)
            self.agent_state_dict.pop(sensor_def.sensor_name, None)
            command_to_send = RemoveSensorCommand(self.name, sensor_def.sensor_name)
            self._client.command_center.enqueue_command(command_to_send)

    @property
    def action_space(self):
        """Gets an :obj:ActionSpace object for the particular agent and control scheme.

        Returns:
            :obj:ActionSpace child object: The action space for this agent and control scheme."""
        return self.control_schemes[self._current_control_scheme][1]

    @property
    def control_schemes(self):
        """A list of all control schemes for the agent. Each list element is a 2-tuple, with the
        first element containing a short description of the control scheme, and the second
        element containing the :obj:`ActionSpace` for the control scheme.

        Returns:
            list of tuples: 2-tuples of short description and :obj:`ActionSpace`
        """
        raise NotImplementedError("Child class must implement this function")

    def __act__(self, action):
        # The default act function is to copy the data,
        # but if needed it can be overridden
        np.copyto(self._action_buffer, action)

    def __repr__(self):
        return self.name


class UavAgent(HolodeckAgent):
    """A UAV (quadcopter) agent
    Action Space: Has two possible continuous action control schemes
    (0) [pitch_torque, roll_torque, yaw_torque, thrust] and
    (1) [pitch_target, roll_target, yaw_rate_target, altitude_target]
    Sensors: RGBCamera, OrientationSensor, LocationSensor, VelocitySensor, IMUSensor
    Inherits from :obj:`HolodeckAgent`."""

    agent_type = "UAV"

    @property
    def control_schemes(self):
        return [("[pitch_torque, roll_torque, yaw_torque, thrust]",
                 ContinuousActionSpace([4])),
                ("[pitch_target, roll_target, yaw_rate_target, altitude_target]",
                 ContinuousActionSpace([4]))]

    def __repr__(self):
        return "UavAgent " + self.name


class SphereAgent(HolodeckAgent):
    """A basic sphere robot that moves on a plane.
    Action Space: Has two possible control schemes, one discrete and one continuous:
    (0) Discrete control scheme of the form [choice] where choice is
    0: Move forward
    1: Move backward
    2: Turn right
    3: Turn left
    (1) Continuous control scheme of the form [forward_speed, rot_speed]
    Sensors: RGBCamera, OrientationSensor, LocationSensor
    Inherits from :obj:`HolodeckAgent`."""

    agent_type = "SphereRobot"

    @property
    def control_schemes(self):
        return [("[forward_movement, rotation]", ContinuousActionSpace([2])),
                ("0: Move forward\n1: Move backward\n2: Turn right\n3: Turn left",
                 DiscreteActionSpace([1], 0, 4, buffer_shape=[2]))]

    def __act__(self, action):
        if self._current_control_scheme is ControlSchemes.SPHERE_DISCRETE:
            np.copyto(self._action_buffer, action)
        elif self._current_control_scheme is ControlSchemes.SPHERE_CONTINUOUS:
            actions = np.array([[2, 0], [-2, 0], [0, 2], [0, -2]])
            to_act = np.array(actions[action, :])
            np.copyto(self._action_buffer, to_act)

    def __repr__(self):
        return "SphereAgent " + self.name


class AndroidAgent(HolodeckAgent):
    """An android agent that can be controlled via torques supplied to its joints.
    Action Space: 94 dimensional vector of continuous values representing torques to be applied at each joint.
    The layout of joints can be found <a href="https://github.com/BYU-PCCL/holodeck/blob/master/holodeck/agents.py">here</a>
    Sensors: RGBCamera, OrientationSensor, LocationSensor, VelocitySensor, IMUSensor, JointRotationSensor,
    PressureSensor RelativeSkeletalPositionSensor
    Inherits from :obj:`HolodeckAgent`."""

    agent_type = "Android"

    @property
    def control_schemes(self):
        return [("[Bone Torques] * 94", ContinuousActionSpace([94]))]

    def __repr__(self):
        return "AndroidAgent " + self.name

    @staticmethod
    def joint_ind(joint_name):
        return AndroidAgent._joint_indices[joint_name]

    _joint_indices = {
        # Head, Spine, and Arm joints. Each has[swing1, swing2, twist]
        "head": 0,
        "neck_01": 3,
        "spine_02": 6,
        "spine_01": 9,
        "upperarm_l": 12,
        "lowerarm_l": 15,
        "hand_l": 18,
        "upperarm_r": 21,
        "lowerarm_r": 24,
        "hand_r": 27,

        # Leg Joints. Each has[swing1, swing2, twist]
        "thigh_l": 30,
        "calf_l": 33,
        "foot_l": 36,
        "ball_l": 39,
        "thigh_r": 42,
        "calf_r": 45,
        "foot_r": 48,
        "ball_r": 51,

        # First joint of each finger. Has only [swing1, swing2]
        "thumb_01_l": 54,
        "index_01_l": 56,
        "middle_01_l": 58,
        "ring_01_l": 60,
        "pinky_01_l": 62,
        "thumb_01_r": 64,
        "index_01_r": 66,
        "middle_01_r": 68,
        "ring_01_r": 70,
        "pinky_01_r": 72,

        # Second joint of each finger.Has only[swing1]
        "thumb_02_l": 74,
        "index_02_l": 75,
        "middle_02_l": 76,
        "ring_02_l": 77,
        "pinky_02_l": 78,
        "thumb_02_r": 79,
        "index_02_r": 80,
        "middle_02_r": 81,
        "ring_02_r": 82,
        "pinky_02_r": 83,

        # Third joint of each finger.Has only[swing1]
        "thumb_03_l": 84,
        "index_03_l": 85,
        "middle_03_l": 86,
        "ring_03_l": 87,
        "pinky_03_l": 88,
        "thumb_03_r": 89,
        "index_03_r": 90,
        "middle_03_r": 91,
        "ring_03_r": 92,
        "pinky_03_r": 93
    }


class NavAgent(HolodeckAgent):
    """A humanoid character that given a position in the world will try to run to that position
    Action Space: Continuous control scheme of the form [x_target, y_target, z_target]
    Sensors: RGBCamera, OrientationSensor, LocationSensor
    Inherits from :obj:`HolodeckAgent`."""

    agent_type = "NavAgent"

    @property
    def control_schemes(self):
        return [("[x_target, y_target, z_target]", ContinuousActionSpace([3]))]

    def __repr__(self):
        return "NavAgent " + self.name

    def __act__(self, action):
        np.copyto(self._action_buffer, np.array(action) * 100)


class TurtleAgent(HolodeckAgent):
    """A simple agent that can have forces applied to it and move around.
    Inherits from :obj:`HolodeckAgent`."""
    @property
    def control_schemes(self):
        return [("[forward_force, rot_force]", ContinuousActionSpace([2]))]

    def __repr__(self):
        return "TurtleAgent " + self.name

    def __act__(self, action):
        np.copyto(self._action_buffer, np.array(action))
        np.copyto(self._action_buffer, action)


class AgentDefinition:
    """A class for declaring what agents are expected or should be spawned in a particular holodeck Environment
    Args:
        agent_name (str): The name of the agent to control.
        agent_type (str or type): The type of HolodeckAgent to control, string or class reference.
        sensors (list of (SensorDefinition or class type (if no duplicate sensors)): A list of HolodeckSensors to read from this agent.
         Defaults to None. Must be a list of SensorDefinitions if there are more than one sensor of the same type
    """
    _type_keys = {
        "SphereAgent": SphereAgent,
        "UavAgent": UavAgent,
        "NavAgent": NavAgent,
        "AndroidAgent": AndroidAgent
    }

    def __init__(self, agent_name, agent_type, sensors=None):
        self.sensors = sensors or list()
        self.name = agent_name
        self.type = AgentDefinition._type_keys[agent_type] if isinstance(agent_type, str) else agent_type


class AgentFactory:
    @staticmethod
    def build_agent(client, agent_def):
        agent_sensors = dict()
        for sensor_def in agent_def.sensors:
            if not isinstance(sensor_def, SensorDefinition):
                sensor_def = SensorDefinition(agent_def.name, None, sensor_def)
            agent_sensors[sensor_def.sensor_name] = SensorFactory.build_sensor(client, sensor_def)

        return agent_def.type(client, agent_def.name, agent_sensors)
