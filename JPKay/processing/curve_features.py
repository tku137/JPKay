# coding=utf-8

import numpy as np


def get_global_minimum(x, y):
    """
    Get global minimum, returning x and y values of the minimum and the index of the minimum.

    :param x: x data
    :type x: numpy.ndarray
    :param y: y data
    :type y: numpy.ndarray
    :return: x, y and index of minimum
    :rtype:
    """
    min_pos = np.nanargmin(y)
    return x[min_pos], y[min_pos], min_pos
