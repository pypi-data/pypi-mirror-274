#!/usr/bin/env python
# -*- coding: utf-8 -*-
# -------------------------------------------------------------------------------
# Author:       kyzhangs
# Date:         2024/5/20
# -------------------------------------------------------------------------------
from setuptools import setup, find_packages


setup(
    name='pytest-collect-jmeter-report-tests',
    version='0.1.0',
    description='A simple plugin to use with pytest',
    author='kyzhangs',
    author_email='kyzhangs@foxmail.com',
    license="Apache License, Version 2.0",
    url='https://gitee.com/kyzhangs/pytest-collect-jmeter-report-tests',
    packages=find_packages(),
    install_requires=[
        'pytest',
    ],
    entry_points={
        'pytest11': [
            'pytest-collect-jmeter-report-tests = pytest_collect_jmeter_report_tests.plugin',
        ],
    }
)
