# coding=utf-8

import re

from pyjavaprops.javaproperties import JavaProperties


class Properties:

    def __init__(self, file_path):

        self.file_path = file_path

        self.java_props = JavaProperties()
        self.load_java_props()

        self.vDeflection_channel_number = self.get_vDeflection_channel_number()

        self.conversion_factors = {}
        self.extract_conversion_factors()

        self.units = {}
        self.extract_specs()

    def load_java_props(self):
        with open(self.file_path, encoding='utf-8') as property_file:
            self.java_props.load(property_file)

    # noinspection PyPep8Naming
    def get_vDeflection_channel_number(self):
        vertical_deflection_channel = None
        for key, value in self.java_props.get_property_dict().items():
            if value == "vDeflection":
                vertical_deflection_channel = re.search(r'(?<=lcd-info\.)\d(?=\.channel.name)', key).group()
        return vertical_deflection_channel

    def extract_conversion_factors(self):
        channel = "lcd-info.{}.".format(self.vDeflection_channel_number)
        encoder = "{}encoder.scaling.".format(channel)
        conversion = "{}conversion-set.conversion.".format(channel)

        self.conversion_factors["vDeflection"] = {}
        self.conversion_factors["vDeflection"]["raw multiplier"] = \
            self.java_props["{}multiplier".format(encoder)]
        self.conversion_factors["vDeflection"]["raw offset"] = \
            self.java_props["{}offset".format(encoder)]
        self.conversion_factors["vDeflection"]["distance multiplier"] = \
            self.java_props["{}distance.scaling.multiplier".format(conversion)]
        self.conversion_factors["vDeflection"]["distance offset"] = \
            self.java_props["{}distance.scaling.offset".format(conversion)]
        self.conversion_factors["vDeflection"]["force multiplier"] = \
            self.java_props["{}force.scaling.multiplier".format(conversion)]
        self.conversion_factors["vDeflection"]["force offset"] = \
            self.java_props["{}force.scaling.offset".format(conversion)]

    # noinspection SpellCheckingInspection
    def extract_specs(self):
        self.units["vDeflection"] = self.java_props["lcd-info.1.conversion-set.conversion.force.scaling.unit.unit"]
