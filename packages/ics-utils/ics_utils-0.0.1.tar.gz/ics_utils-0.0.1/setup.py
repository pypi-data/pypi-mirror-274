# -*- coding: utf-8 -*-
"""
@author: hanyanling
@date: 2024/5/21 下午5:38
@email:
---------
@summary:
"""


from setuptools import setup, find_packages

packages = find_packages()


setup(
    name='ics_utils',
    version='0.0.1',
    author='hanyanling',
    url='https://github.com/StealDivinePower/ics_utils',
    packages=packages,
    python_requires='>=3.6'
)