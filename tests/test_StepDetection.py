# coding=utf-8

import numpy as np
import numpy.testing as npt

from JPKay.processing.step_detection import get_step_curve, get_step_positions, get_retract_steps


class TestStepDetection:

    @staticmethod
    def generate_step_signal():
        np.random.seed(1)
        noise = np.random.normal(0, 1, 5000)
        noise[1000:2000] += 2
        noise[2000:3000] += 5
        noise[3000:] += 7
        return noise

    def test_get_step_curve(self):
        np.random.seed(1)
        signal = self.generate_step_signal()
        x = np.arange(5000)

        test_steps = get_step_curve(x, signal)

        npt.assert_almost_equal(np.mean(test_steps[400:600]), np.array(0), decimal=1)
        npt.assert_almost_equal(np.mean(test_steps[1400:1600]), np.array(2), decimal=1)
        npt.assert_almost_equal(np.mean(test_steps[2400:2600]), np.array(5), decimal=1)

    def test_get_step_positions(self):
        np.random.seed(1)
        signal = self.generate_step_signal()
        x = np.arange(5000)
        steps = get_step_positions(x, signal)

        npt.assert_almost_equal(steps, np.array([1001, 1999, 2999]), decimal=1)

    def test_get_retract_steps(self):
        np.random.seed(1)
        signal = self.generate_step_signal()
        signal[5] += -1
        x = np.arange(5000)
        steps = get_retract_steps(x, signal)

        npt.assert_almost_equal(steps, np.array([1994, 2994]), decimal=1)
