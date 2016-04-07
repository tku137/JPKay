# coding=utf-8

import pytest
import json

from JPKay.data_io.property_reader import Properties


# noinspection PyShadowingNames
@pytest.mark.usefixtures("java_prop", "java_prop_dict")
class TestXmlConversion:

    def test_load_java_props(self, java_prop, java_prop_dict):
        props = Properties(file_path=java_prop)
        loaded_props = props.java_props.get_property_dict()
        with open(java_prop_dict) as infile:
            original_props = json.load(infile)
        assert original_props == loaded_props

    # noinspection PyPep8Naming
    def test_get_vDeflection_channel_number(self, java_prop):
        props = Properties(file_path=java_prop)
        channel = props.get_vDeflection_channel_number()
        assert channel == "1"

    def test_extract_factors(self, java_prop):
        props = Properties(file_path=java_prop)
        props.extract_conversion_factors()
        assert props.conversion_factors["vDeflection"]["raw multiplier"] == "5.525411033343059E-9"
        assert props.conversion_factors["vDeflection"]["raw offset"] == "-6.075877326676198E-4"
        assert props.conversion_factors["vDeflection"]["distance multiplier"] == "7.730641603896163E-8"
        assert props.conversion_factors["vDeflection"]["distance offset"] == "0.0"
        assert props.conversion_factors["vDeflection"]["force multiplier"] == "0.01529211140472191"
        assert props.conversion_factors["vDeflection"]["force offset"] == "0.0"

    def test_extract_specs(self, java_prop):
        props = Properties(file_path=java_prop)
        props.extract_specs()
        assert props.units["vDeflection"] == "N"
