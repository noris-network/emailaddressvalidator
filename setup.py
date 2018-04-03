#!/usr/bin/env python3

from setuptools import setup

setup(name='emailaddressvalidator',
		version='1.0',
		description='Little library for email format validation',
		author='Roman Klesel',
		author_email='roman.klesel@noris.de',
		url='https://www.noris.de/email_validator',
		packages=['.'],
		test_suite='tests',
		setup_requires=['pytest-runner'],
		tests_require=['pytest'],
     )
