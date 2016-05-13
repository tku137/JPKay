# coding=utf-8

import numpy as np
import numpy.testing as npt

from JPKay.processing.curve_features import get_global_minimum


class TestStepDetection:

    @staticmethod
    def generate_step_signal():
        np.random.seed(1)
        noise = np.random.normal(0, 1, 5000)
        noise[123] = -3
        noise[1000:2000] += 2
        noise[2000:3000] += 5
        noise[3000:] += 7
        return noise

    def test_get_step_curve(self):
        np.random.seed(1)
        signal = self.generate_step_signal()
        x = np.arange(5000)

        min_x, min_y, min_pos = get_global_minimum(x, signal)

        npt.assert_almost_equal(min_x, np.array(892), decimal=1)
        npt.assert_almost_equal(min_y, np.array(-3), decimal=1)
        npt.assert_almost_equal(min_pos, np.array(892), decimal=1)
