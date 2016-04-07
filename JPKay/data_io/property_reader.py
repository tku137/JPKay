# coding=utf-8

import re

from pyjavaprops.javaproperties import JavaProperties


class Properties:
    """
    Object to automatically extract and conveniently use relevant JPK force file header information.

    This comprises things like conversion factors for raw data, units, and so on

    - **attributes**::

    vDeflection_channel_number: internal number of vDeflection channel raw data
    conversion_factors: dictionary containing important information
    units: dictionary containing channel units

    - **example usage**::
    >>> from JPKay.data_io.property_reader import Properties
    >>> prop_file = r"path/to/header.properties"
    >>> props = Properties(file_path=prop_file)
    >>> print(props.units["vDeflection"])
    V
    >>> print(props.conversion_factors["vDeflection"]["force multiplier"])
    0.01529211140472191
    """

    def __init__(self, file_path):

        # parse file path to header.properties file
        self.file_path = file_path

        # load the property file (you have to instantiate and load subsequently)
        self.java_props = JavaProperties()
        self.load_java_props()

        # set vDeflection channel number, always extract freshly because channel numbering seems to be inconsistent
        self.channel_numbers = self.get_channel_numbers()

        # extract raw conversion factors and other specifications like units and the lik
        self.conversion_factors = {}
        self.extract_conversion_factors()
        self.units = {}
        self.extract_specs()

    def load_java_props(self):
        """This actually loads the props file on disk to the JavaProperties object"""
        with open(self.file_path, encoding='utf-8') as property_file:
            self.java_props.load(property_file)

    # noinspection PyPep8Naming
    def get_channel_numbers(self):
        """
        Extracts the channel numbers for each channel.

        :return: dictionary with channel numbers
        :rtype: dict
        """
        channel_numbers = {"vDeflection": None, "hDeflection": None, "height": None, "capacitiveSensorHeight": None}
        for key, value in self.java_props.get_property_dict().items():
            if value == "vDeflection":
                channel_numbers[value] = re.search(r'(?<=lcd-info\.)\d(?=\.channel.name)', key).group()
            if value == "hDeflection":
                channel_numbers[value] = re.search(r'(?<=lcd-info\.)\d(?=\.channel.name)', key).group()
            if value == "height":
                channel_numbers[value] = re.search(r'(?<=lcd-info\.)\d(?=\.channel.name)', key).group()
            if value == "capacitiveSensorHeight":
                channel_numbers[value] = re.search(r'(?<=lcd-info\.)\d(?=\.channel.name)', key).group()
        return channel_numbers

    def extract_conversion_factors(self):
        """
        Extracts all conversion factors for the raw data channels. Currently, only vDeflection channel is
        extracted, because it is the only one calibrated during AFM measurements
        """
        channel = "lcd-info.{}.".format(self.channel_numbers["vDeflection"])
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
        """Extracts any kind of infos from the header, like units and the like"""
        self.units["vDeflection"] = self.java_props["lcd-info.1.conversion-set.conversion.force.scaling.unit.unit"]
