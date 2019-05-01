import numpy as np


def state_almost_equal(state1, state2, thresh=0.01):
    if is_full_state(state1):
        for agent in state1:
            for sensor in state1[agent]:
                if not almost_equal(state1[agent][sensor], state2[agent][sensor], thresh, sensor):
                    print(sensor)
                    print(state1[agent][sensor], state2[agent][sensor])
                    return False
    else:
        for sensor in state1:
            if not almost_equal(state1[sensor], state2[sensor], thresh, sensor):
                print(sensor)
                print(state1[sensor], state2[sensor])
                return False
    return True


def almost_equal(item1, item2, thresh=0.01, sensor=""):
    if sensor == "RGBCamera":
        return True
    item1 = np.array(item1).flatten()
    item2 = np.array(item2).flatten()
    if len(item1) != len(item2):
        return False
    return all( np.isclose(item1, item2, rtol=thresh) )


def is_full_state(state):
    return isinstance(next(iter(state.values())), dict)
