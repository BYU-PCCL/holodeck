import numpy as np


def compare_states(state1, state2, thresh=0.01, is_close=True):
    if is_full_state(state1):
        for agent in state1:
            for sensor in state1[agent]:
                if sensor == "RGBCamera":
                    continue
                close = almost_equal(state1[agent][sensor], state2[agent][sensor], thresh)
                if is_close != close:
                    print(sensor)
                    return False
    else:
        for sensor in state1:
            if sensor == "RGBCamera":
                continue
            close = almost_equal(state1[sensor], state2[sensor], thresh)
            if is_close != close:
                print(sensor)
                return False
    return True


def almost_equal(item1, item2, thresh=0.01):
    item1 = np.array(item1).flatten()
    item2 = np.array(item2).flatten()
    if len(item1) != len(item2):
        return False
    return all(np.isclose(item1, item2, rtol=thresh,atol=1e-5))


def is_full_state(state):
    return isinstance(next(iter(state.values())), dict)
