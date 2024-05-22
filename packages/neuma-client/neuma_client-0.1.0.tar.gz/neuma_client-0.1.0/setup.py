#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from setuptools import find_packages, setup

setup(
    packages=find_packages(
		 include=['neuma-client*'], 
        exclude=["*.tests", "*.tests.*", "tests.*", "tests"],
    ),
	include_package_data=True
)
