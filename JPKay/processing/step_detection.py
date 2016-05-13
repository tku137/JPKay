# coding=utf-8

import numpy as np

from skimage.feature import peak_local_max
from sklearn.isotonic import IsotonicRegression

from JPKay.processing.curve_features import get_global_minimum


def get_step_curve(x, y):
    """
    Calculate the transformed isotonic regression curve.

    Data is fitted and transformed using the
    `isotonic regression model <http://scikit-learn.org/stable/auto_examples/plot_isotonic_regression.html>`_ from
    `scikit-learn <http://scikit-learn.org/stable/index.html>`_.

    :param x: x data
    :type x: numpy.ndarray
    :param y: y data
    :type y: numpy.ndarray
    :return: transformed curve
    :rtype: numpy.ndarray
    """
    ir = IsotonicRegression()
    return ir.fit_transform(x, y)


def get_step_positions(x, y, threshold=0.3, min_distance=50):
    """
    Detect positions of steps in the provided curve. The step curve from :func:`get_step_curve` is further processed
    and physically relevant steps are filtered.

    :param x: x data
    :type x: numpy.ndarray
    :param y: y data
    :type y: numpy.ndarray
    :param threshold: step filter threshold
    :type threshold: float
    :param min_distance: minimum distance of steps
    :type min_distance: int
    :return: positions of steps
    :rtype: numpy.ndarray
    """

    step_curve = get_step_curve(x, y)
    gradient = np.diff(step_curve)
    gradient_normalized = gradient / np.max(gradient)

    steps = peak_local_max(gradient_normalized, threshold_abs=threshold, min_distance=min_distance)

    return steps.squeeze()


def get_retract_steps(x, y, threshold=0.3, min_distance=50):
    """
    Detect physically relevant steps in a retract curve.

    Steps are detected using :func:`get_step_positions` starting from the global minimum obtained using
    :func:`~JPKay.processing.curve_features.get_global_minimum`.

    :param x: x data
    :type x: numpy.ndarray
    :param y: y data
    :type y: numpy.ndarray
    :param threshold: step filter threshold
    :type threshold: float
    :param min_distance: minimum distance of steps
    :type min_distance: int
    :return: positions of steps
    :rtype: numpy.ndarray
    """

    min_x, min_y, min_pos = get_global_minimum(x, y)

    return get_step_positions(x[min_pos:], y[min_pos:], threshold, min_distance)
