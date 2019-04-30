import numpy as np

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
