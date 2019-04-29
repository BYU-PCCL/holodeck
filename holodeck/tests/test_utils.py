
def almost_equal(item1, item2, thresh=0.01):
    if len(item1) != len(item2):
        return False
    else:
        for i, val1 in enumerate(item1):
            if abs(val1 - item2[i]) > thresh*val1:
                return False
    return True
