# coding=utf-8

import re
from zipfile import ZipFile
import dateutil.parser as parser
import pytz


class Properties:
    """
    Object to automatically extract and conveniently use relevant JPK force file header information.

    This comprises things like conversion factors for raw data, units, and so on

    - **attributes**::

    vDeflection_channel_number: internal number of vDeflection channel raw data
    conversion_factors: dictionary containing important information
    units: dictionary containing channel units

    - **example usage**::
    >>> from JPKay.core.data_structures import Properties
    >>> force_file = r"path/to/jpk-force-file"
    >>> props = Properties(file_path=force_file)
    >>> print(props.units["vDeflection"])
    V
    >>> print(props.conversion_factors["vDeflection"]["force multiplier"])
    0.01529211140472191
    """

    def __init__(self, file_path):

        # parse file path to header.properties file
        self.file_path = file_path

        # load the property file (you have to instantiate and load subsequently)
        self.prop_dict = self.load_java_props()

        # set vDeflection channel number, always extract freshly because channel numbering seems to be inconsistent
        self.channel_numbers = self.get_channel_numbers()

        # extract raw conversion factors and other specifications like units and the lik
        self.conversion_factors = {}
        self.extract_conversion_factors()
        self.units = {}
        self.extract_specs()

    def load_java_props(self):
        """
        This actually loads the props file on disk from jpk-force zip-file. Parses all java-properties info and the
        timestamp from the header of the header.

        :return: props dictionary
        :rtype: dict
        """

        # load root header.properties file from zipfile
        with ZipFile(self.file_path) as zip_file:
            with zip_file.open('shared-data/header.properties') as prop_file:
                prop_content = [line.decode() for line in prop_file.read().splitlines()]

        # parse prop dictionary (without header date)
        props = {}
        for line in prop_content[1:]:
            key, value = line.split("=")
            props[key] = value

        # parse measurement date-time
        fmt = '%Y-%m-%d %H:%M:%S %Z%z'
        utc = pytz.utc
        props["timestamp"] = utc.localize(parser.parse(prop_content[0][1:], dayfirst=True)).strftime(fmt)

        return props

    # noinspection PyPep8Naming
    def get_channel_numbers(self):
        """
        Extracts the channel numbers for each channel.

        :return: dictionary with channel numbers
        :rtype: dict
        """
        channel_numbers = {"vDeflection": None, "hDeflection": None, "height": None, "capacitiveSensorHeight": None}
        for key, value in self.prop_dict.items():
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
            self.prop_dict["{}multiplier".format(encoder)]
        self.conversion_factors["vDeflection"]["raw offset"] = \
            self.prop_dict["{}offset".format(encoder)]
        self.conversion_factors["vDeflection"]["distance multiplier"] = \
            self.prop_dict["{}distance.scaling.multiplier".format(conversion)]
        self.conversion_factors["vDeflection"]["distance offset"] = \
            self.prop_dict["{}distance.scaling.offset".format(conversion)]
        self.conversion_factors["vDeflection"]["force multiplier"] = \
            self.prop_dict["{}force.scaling.multiplier".format(conversion)]
        self.conversion_factors["vDeflection"]["force offset"] = \
            self.prop_dict["{}force.scaling.offset".format(conversion)]

    # noinspection SpellCheckingInspection
    def extract_specs(self):
        """Extracts any kind of infos from the header, like units and the like"""
        self.units["vDeflection"] = self.prop_dict["lcd-info.1.conversion-set.conversion.force.scaling.unit.unit"]
