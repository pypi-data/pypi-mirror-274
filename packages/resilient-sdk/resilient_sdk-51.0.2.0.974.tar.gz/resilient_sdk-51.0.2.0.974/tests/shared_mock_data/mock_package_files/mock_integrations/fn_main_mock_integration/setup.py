#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
import glob
import ntpath


def get_module_name(module_path):
    """
    Return the module name of the module path
    """
    return ntpath.split(module_path)[1].split(".")[0]


def snake_to_camel(word):
    """
    Convert a word from snake_case to CamelCase
    """
    return ''.join(x.capitalize() or '_' for x in word.split('_'))


setup(
    name="fn_main_mock_integration",
    display_name="Main Mock Integration",
    version="1.0.0",
    license="<<insert here>>",
    author="<<your name here>>",
    author_email="you@example.com",
    url="https://ibm.com/mysupport",
    # url='https://ibm.biz/resilientcommunity',
    description="Resilient Circuits Components for 'fn_main_mock_integration'",
    long_description=u"""Resilient Circuits Components for 'fn_main_mock_integration'
    A mock description of mock_function_one with unicode:  ล ฦ ว ศ ษ ส ห ฬ อ""",
    install_requires=[
        "resilient_circuits>=30.0.0"
    ],
    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    classifiers=[
        "Programming Language :: Python",
    ],
    entry_points={
        "resilient.circuits.components": [
            # When setup.py is executed, loop through the .py files in the components directory and create the entry points.
            "{}FunctionComponent = fn_main_mock_integration.components.{}:FunctionComponent".format(snake_to_camel(get_module_name(filename)), get_module_name(filename)) for filename in glob.glob("./fn_main_mock_integration/components/[a-zA-Z]*.py")
        ],
        "resilient.circuits.configsection": ["gen_config = fn_main_mock_integration.util.config:config_section_data"],
        "resilient.circuits.customize": ["customize = fn_main_mock_integration.util.customize:customization_data"],
        "resilient.circuits.selftest": ["selftest = fn_main_mock_integration.util.selftest:selftest_function"]
    }
)
