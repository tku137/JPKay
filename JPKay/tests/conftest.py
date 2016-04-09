# coding=utf-8

import pytest
import os


@pytest.fixture(scope='session')
def sample_force_file():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "sample.jpk-force")


@pytest.fixture(scope='session')
def general_prop_dict():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "general.json")


@pytest.fixture(scope='session')
def segments_prop_dict():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "segments.json")
