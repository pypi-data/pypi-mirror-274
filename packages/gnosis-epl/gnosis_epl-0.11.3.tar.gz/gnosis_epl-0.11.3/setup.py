#!/usr/bin/env python
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

with open('README.md') as readme_file:
    readme = readme_file.read()


with open('requirements.txt') as requirements_file:
    requirements = [r for r in requirements_file.readlines()]


test_requirements = [
]
setup(
    name='gnosis_epl',
    version='0.11.3',
    description="Gnosis EPL python package",
    long_description=readme,
    author="Felipe Arruda Pontes",
    author_email='felipe.arruda.pontes@insight-centre.org',
    packages=find_packages(),
    package_dir={'gnosis_epl':
                 'gnosis_epl'},
    include_package_data=True,
    install_requires=requirements,
    zip_safe=False,
    license='Apache License, Version 2.0',
    test_suite='tests',
    tests_require=test_requirements
)
