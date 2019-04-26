
def almost_equal(item1, item2, thresh=0.01):
    if len(item1) != len(item2):
        return False
    else:
        for i in range(len(item1)):
            if abs(item1[i] - item2[i]) > thresh*item1[i]:
                return False
    return True
