import numpy as np


def state_almost_equal(state1, state2, thresh=0.1):
    if isinstance(state1[next(iter(state1))], dict):
        for agent in state1:
            for sensor in state1[agent]:
                if not almost_equal(state1[agent][sensor], state2[agent][sensor], thresh):
                    return False
    else:
        for sensor in state:
            if not almost_equal(state1[sensor], state2[sensor]):
                return False
    return True


def almost_equal(item1, item2, thresh=0.01):

    item1 = np.array(item1).flatten()
    item2 = np.array(item2).flatten()
    if len(item1) != len(item2):
        return False
    else:
        for i, val1 in enumerate(item1):
            if abs(val1 - item2[i]) > thresh*val1 and val1 > 0.01:
                return False
    return True
