class Settings:
    def __init__(self):
        print("No point in instantiating an object.")


class UAV(Settings):
    def __init__(self):
        Settings.__init__(self)
        print("No point in instantiating an object.")

    UAV_MASS = 0
    UAV_MU = 1
    UAV_MAX_ROLL = 2
    UAV_MAX_PITCH = 3
    UAV_MAX_YAW_RATE = 4
    UAV_MAX_FORCE = 5
    UAV_TAU_UP_ROLL = 6
    UAV_TAU_UP_PITCH = 7
    UAV_TAU_UP_YAW_RATE = 8
    UAV_TAU_UP_FORCE = 9
    UAV_TAU_DOWN_ROLL = 10
    UAV_TAU_DOWN_PITCH = 11
    UAV_TAU_DOWN_YAW_RATE = 12
    UAV_TAU_DOWN_FORCE = 13
    UAV_ROLL_P = 14
    UAV_ROLL_I = 15
    UAV_ROLL_D = 16
    UAV_PITCH_P = 17
    UAV_PITCH_I = 18
    UAV_PITCH_D = 19
    UAV_YAW_P = 20
    UAV_YAW_I = 21
    UAV_YAW_D = 22
    UAV_ALT_P = 23
    UAV_ALT_I = 24
    UAV_ALT_D = 25
