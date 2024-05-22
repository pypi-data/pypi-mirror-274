#!/usr/bin/env python
# -*- encoding: utf-8 -*-

"""
@File        :   setup 
@Time        :   2023/9/14 15:51
@Author      :   Xuesong Chen
@Description :   
"""
from setuptools import setup, find_packages

setup(
    name='wuji',
    version='0.1.77',
    packages=find_packages(exclude=('tests', 'tests.*')),
    install_requires=[
        # list of dependencies, e.g., 'numpy>=1.18.5'
    ],
)
