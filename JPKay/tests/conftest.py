# coding=utf-8

import pytest
import os


@pytest.fixture(scope='session')
def java_prop():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "header.properties")


@pytest.fixture(scope='session')
def java_prop_dict():
    return os.path.join(os.path.dirname(os.path.abspath(__file__)), "data", "java_prop.json")
