# coding=utf-8

import pytest

import numpy.testing as npt
from numpy import array
import pandas.util.testing as pdt
import pandas as pd

from JPKay.core.data_structures import JPKForce


# noinspection PyShadowingNames,PyPep8Naming
@pytest.mark.usefixtures("sample_force_file")
class TestJpkForce:
    def test_load_encoded_data_segment(self, sample_force_file):
        sample = JPKForce(sample_force_file)
        segment = 'retract'
        vDef, height = sample.load_encoded_data_segment(segment)

        assert vDef[0] == -4454604
        assert height[0] == 468876141
        assert vDef.shape == (1000, 1)
        assert height.shape == (1000, 1)

    def test_load_data(self, sample_force_file):
        sample = JPKForce(sample_force_file)
        assert sample.data.shape == (1000, 8)

        iterable = [['approach', 'contact', 'retract', 'pause'], ['force', 'height']]
        index = pd.MultiIndex.from_product(iterable, names=['segment', 'channel'])
        data = array([-2.98158446715e-11, 3.90831266155e-05])
        df = pd.DataFrame(columns=index)
        df.loc[0, 'retract'] = data
        pdt.assert_almost_equal(sample.data.loc[0], df.loc[0])

    def test_convert_data(self, sample_force_file):
        sample = JPKForce(sample_force_file)
        conv_1 = sample.convert_data('vDeflection', array(-4454604))
        conv_2 = sample.convert_data('height', array(468876141))

        npt.assert_almost_equal(conv_1, array(-2.98158446715e-11), decimal=20)
        npt.assert_almost_equal(conv_2, array(3.90831266155e-05), decimal=15)

    def test_construct_df(self, sample_force_file):
        sample = JPKForce(sample_force_file)
        df = sample.construct_df()

        iterable = [['approach', 'contact', 'retract', 'pause'], ['force', 'height']]
        index = pd.MultiIndex.from_product(iterable, names=['segment', 'channel'])
        pdt.assert_frame_equal(df, pd.DataFrame(columns=index))
