import numpy as np


def almost_equal(item1, item2, r_thresh=0.01, a_thresh=1e-4):
    item1 = np.array(item1).flatten()
    item2 = np.array(item2).flatten()
    if len(item1) != len(item2):
        return False

    return all(np.isclose(item1, item2, rtol=r_thresh,atol=a_thresh))