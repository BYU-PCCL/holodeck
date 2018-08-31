"""This module provides orderly access to constants associated with each agent's hyperparameters.
To add another agent to this module of constants, make a class containing the expected index of all of its
hyperparameters in the array.  You must also specify the expected size of the array for the agent in
Hyperparameters._shape_dict.  This is all you must do to allow the client to access the hyperparameter information.  The
default expected size of the array is 1.
"""
from holodeck.agents import *


class Hyperparameters:
    """This class contains an easy way of accessing the expected size of the hyperparameter array for an agent."""
    _shape_dict = {
            UavAgent: [27]
    }

    @staticmethod
    def shape(agent_type):
        """Get the shape of the hyperparameter array for the specified agent"""
        return Hyperparameters._shape_dict[agent_type] if agent_type in Hyperparameters._shape_dict else [1]


class UAVHyperparameters:
    """This class contains the indices of the UAV's hyperparameters

    The variables appended with a P, I, or D apply to the proportional, integral, and derivative part of the internal
    PID controller of the UAV. The variables with TAU are the "Process Time Constants" - the value that we calculated
    (admittedly imperfectly) to be the amount of time (in seconds) for the UAV to reach 63.2% of its output in the
    respective aspect. Changing Tau will cause overshooting the target or arriving late to the target, depending.
    """
    NUMBER_OF_ELEMENTS = 0  # this is the first item in the buffer, not the actual number of elements
    UAV_MASS = 1
    UAV_MU = 2
    UAV_MAX_ROLL = 3
    UAV_MAX_PITCH = 4
    UAV_MAX_YAW_RATE = 5
    UAV_MAX_FORCE = 6
    UAV_TAU_UP_ROLL = 7
    UAV_TAU_UP_PITCH = 8
    UAV_TAU_UP_YAW_RATE = 9
    UAV_TAU_UP_FORCE = 10
    UAV_TAU_DOWN_ROLL = 11
    UAV_TAU_DOWN_PITCH = 12
    UAV_TAU_DOWN_YAW_RATE = 13
    UAV_TAU_DOWN_FORCE = 14
    UAV_ROLL_P = 15
    UAV_ROLL_I = 16
    UAV_ROLL_D = 17
    UAV_PITCH_P = 18
    UAV_PITCH_I = 19
    UAV_PITCH_D = 20
    UAV_YAW_P = 21
    UAV_YAW_I = 22
    UAV_YAW_D = 23
    UAV_ALT_P = 24
    UAV_ALT_I = 25
    UAV_ALT_D = 26
