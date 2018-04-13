from holodeck.agents import *


class Hyperparameters:
        _shape_dict = {
                UAVAgent: [27]
        }

        @staticmethod
        def shape(agent_type):
                return Hyperparameters._shape_dict[agent_type] if agent_type in Hyperparameters._shape_dict else [1]


class UAVHyperparameters:
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
