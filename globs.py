from typing import Union

W, H = 1200, 720

def find3d(target, lst, comp='=='):
    """

    :param target:
    :param lst:
    :param comp: not built yet
    :return: int() index of row where target was found
    """
    for x in range(len(lst)):
        for y in lst[x]:
            if y == target:
                return x
    else:
        return False
