# coding=utf-8

import os
import re
from zipfile import ZipFile
import dateutil.parser as parser
import pytz
from struct import unpack
import numpy as np


class ForceArchive:
    """
    Object to handle reading contents of a jpk-force zipped file.

    - **Methods**::

    - ls: list archive contents
    - read_properties: read utf-8 string decoded content of a property file, one property per list entry
    - read_data: read encoded raw data, must be converted to appropriate physical quantity!
    """

    # noinspection SpellCheckingInspection
    def __init__(self, file_path):
        self._zip_file = ZipFile(file_path)
        if not self.read_properties('header.properties')['jpk-data-file'] == 'spm-forcefile':
            raise ValueError("not a valid spm-forcefile!")
        self.contents = self.ls()

    def ls(self):
        """List all files contained in this force-archive"""
        return self._zip_file.infolist()

    def read_properties(self, content_path):
        """
        Reads a property file form the force-archive.

        The contents of the property file are elements of a list. Each entry is already decoded to utf-8.

        :param content_path: internal path to the force-archive file
        :type content_path: str
        :return: property list
        :rtype: dict
        """

        if not os.path.basename(content_path).endswith(".properties"):
            raise ValueError("this content path is not a property file")

        try:
            with self._zip_file.open(content_path) as file:
                content = [line.decode('utf-8') for line in file.read().splitlines()]

            # parse prop dictionary (without header date)
            props = {}
            for line in content[1:]:
                key, value = line.split("=")
                props[key] = value

            # parse measurement date-time
            fmt = '%Y-%m-%d %H:%M:%S %Z%z'
            utc = pytz.utc
            props["timestamp"] = utc.localize(parser.parse(content[0][1:], dayfirst=True)).strftime(fmt)

            return props

        except IOError:
            print("can't read property file")

    def read_data(self, content_path):
        """
        Reads the raw integer-encoded data of the specified data file inside a force-archive.

        :param content_path: internal path to the force-archive file
        :type content_path: str
        :return: raw data
        :rtype: np.ndarray
        """

        if not os.path.basename(content_path).endswith(".dat"):
            raise ValueError("this content path is not a data file")

        try:
            # read binary data
            data = self._zip_file.read(content_path)

            # decode using big-endian integer
            result = []
            for i in range(int(len(data) / 4)):
                result.append(unpack('!i', data[i * 4:(i + 1) * 4]))

            # returning integer-encoded raw data vector
            return np.array(result)
        except IOError:
            print("can't read data file")


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
        self.general = self.load_general_props()
        self.segments = self.extract_segment_props()

        # set vDeflection channel number, always extract freshly because channel numbering seems to be inconsistent
        self.channel_numbers = self.get_channel_numbers()

        # extract raw conversion factors and other specifications like units and the lik
        self.conversion_factors = self.extract_conversion_factors()
        self.units = {}
        self.extract_specs()

    def load_general_props(self):
        """
        This actually loads the props file on disk from jpk-force zip-file. Parses all java-properties info and the
        timestamp from the header of the header.

        :return: props dictionary
        :rtype: dict
        """

        # load general and shared header.properties file from zipfile
        root = ForceArchive(self.file_path).read_properties('header.properties')
        shared = ForceArchive(self.file_path).read_properties('shared-data/header.properties')
        return {**root, **shared}

    # noinspection PyPep8Naming
    def get_channel_numbers(self):
        """
        Extracts the channel numbers for each channel.

        :return: dictionary with channel numbers
        :rtype: dict
        """
        channel_numbers = {"vDeflection": None, "hDeflection": None, "height": None, "capacitiveSensorHeight": None}
        for key, value in self.general.items():
            if value == "vDeflection":
                channel_numbers[value] = re.search(r'(?<=lcd-info\.)\d(?=\.channel.name)', key).group()
            if value == "hDeflection":
                channel_numbers[value] = re.search(r'(?<=lcd-info\.)\d(?=\.channel.name)', key).group()
            if value == "height":
                channel_numbers[value] = re.search(r'(?<=lcd-info\.)\d(?=\.channel.name)', key).group()
            if value == "capacitiveSensorHeight":
                channel_numbers[value] = re.search(r'(?<=lcd-info\.)\d(?=\.channel.name)', key).group()
        return channel_numbers

    # noinspection PyPep8Naming
    def extract_conversion_factors(self):
        """
        Extracts all conversion factors for the raw data channels. Currently, only vDeflection channel is
        extracted, because it is the only one calibrated during AFM measurements

        :return: dict with conversion factors
        :rtype: dict[np.ndarray]
        """

        # get some info to reduce ridiculously long java-prop names
        vDeflection_channel = "lcd-info.{}.".format(self.channel_numbers["vDeflection"])
        vDeflection_encoder = "{}encoder.scaling.".format(vDeflection_channel)
        vDeflection_conversion = "{}conversion-set.conversion.".format(vDeflection_channel)

        height_channel = "lcd-info.{}.".format(self.channel_numbers["height"])
        height_encoder = "{}encoder.scaling.".format(height_channel)
        height_conversion = "{}conversion-set.conversion.".format(height_channel)

        factors = {"vDeflection": {}, "height": {}}

        # parse vDeflection conversion factors
        factors["vDeflection"]["raw multiplier"] = \
            np.array(float(self.general["{}multiplier".format(vDeflection_encoder)]))
        factors["vDeflection"]["raw offset"] = np.array(float(self.general["{}offset".format(vDeflection_encoder)]))
        factors["vDeflection"]["distance multiplier"] = \
            np.array(float(self.general["{}distance.scaling.multiplier".format(vDeflection_conversion)]))
        factors["vDeflection"]["distance offset"] = \
            np.array(float(self.general["{}distance.scaling.offset".format(vDeflection_conversion)]))
        factors["vDeflection"]["force multiplier"] = \
            np.array(float(self.general["{}force.scaling.multiplier".format(vDeflection_conversion)]))
        factors["vDeflection"]["force offset"] = \
            np.array(float(self.general["{}force.scaling.offset".format(vDeflection_conversion)]))

        # parse height conversion factors
        factors["height"]["raw multiplier"] = np.array(float(self.general["{}multiplier".format(height_encoder)]))
        factors["height"]["raw offset"] = np.array(float(self.general["{}offset".format(height_encoder)]))
        factors["height"]["calibrated multiplier"] = \
            np.array(float(self.general["{}nominal.scaling.multiplier".format(height_conversion)]))
        factors["height"]["calibrated offset"] = \
            np.array(float(self.general["{}nominal.scaling.offset".format(height_conversion)]))

        return factors

    # noinspection SpellCheckingInspection,PyPep8Naming
    def extract_specs(self):
        """Extracts any kind of infos from the header, like units and the like"""
        vDeflection_unit = "lcd-info.{}.conversion-set.conversion.force.scaling.unit.unit".format(
            self.channel_numbers["vDeflection"])
        self.units["vDeflection"] = self.general[vDeflection_unit]

        height_unit = "lcd-info.{}.conversion-set.conversion.nominal.scaling.unit.unit".format(
            self.channel_numbers["height"])
        self.units["height"] = self.general[height_unit]

    def extract_segment_props(self):
        props = {}
        num_segments = int(self.general['force-scan-series.force-segments.count'])
        for segment in range(num_segments):
            segment_props = ForceArchive(self.file_path).read_properties(
                'segments/{}/segment-header.properties'.format(segment))
            # noinspection SpellCheckingInspection
            name_jpk = segment_props['force-segment-header.name.name'].replace('-cellhesion200', '')
            normal_name = self.convert_segment_name(name_jpk)
            props[normal_name] = segment_props
            props[normal_name]["name_jpk"] = name_jpk
            props[normal_name]["name"] = normal_name
            props[normal_name]["segment_number"] = str(segment)

        return props

    @staticmethod
    def convert_segment_name(jpk_name):

        if jpk_name == 'extend':
            real_name = 'approach'
        elif jpk_name == 'pause-at-end':
            real_name = 'contact'
        elif jpk_name == 'pause-at-start':
            real_name = 'pause'
        else:
            real_name = jpk_name

        return real_name
