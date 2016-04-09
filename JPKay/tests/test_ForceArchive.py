# coding=utf-8

import pytest

from zipfile import ZipInfo

from numpy import ndarray
from JPKay.core.data_structures import ForceArchive


# noinspection PyShadowingNames
@pytest.mark.usefixtures("sample_force_file")
class TestXmlConversion:

    def test_instantiation(self, sample_force_file):
        sample = ForceArchive(sample_force_file)
        assert sample.contents[0].filename == 'header.properties'
        assert isinstance(sample.contents[0], ZipInfo)

    def test_ls(self, sample_force_file):
        sample = ForceArchive(sample_force_file)
        assert sample.ls()[0].filename == 'header.properties'
        assert isinstance(sample.ls()[0], ZipInfo)

    def test_read_properties(self, sample_force_file):
        sample = ForceArchive(sample_force_file)
        # noinspection SpellCheckingInspection
        assert sample.read_properties('header.properties')['jpk-data-file'] == 'spm-forcefile'
        with pytest.raises(ValueError):
            sample.read_properties('false.file')

    def test_read_data(self, sample_force_file):
        sample = ForceArchive(sample_force_file)
        # noinspection SpellCheckingInspection
        assert isinstance(sample.read_data('segments/0/channels/vDeflection.dat'), ndarray)
        with pytest.raises(ValueError):
            sample.read_data('false.file')
        assert sample.read_data('segments/0/channels/vDeflection.dat').shape == (1000, 1)
