#!/usr/bin/env python3

from setuptools import setup

setup(name='emailaddressvalidator',
		version='1.1',
		description='Little library for email format validation',
		author='Roman Klesel',
		author_email='roman.klesel@noris.de',
		url='https://github.com/noris-network/emailaddressvalidator',
		packages=['.'],
		test_suite='tests',
		setup_requires=['pytest-runner'],
		tests_require=['pytest'],
     )
