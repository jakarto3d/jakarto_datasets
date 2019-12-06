#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup, find_packages
from importlib.machinery import SourceFileLoader

module = SourceFileLoader("jakarto_datasets", "./src/jakarto_datasets/__init__.py").load_module()

with open('README.md') as readme_file:
    readme = readme_file.read()

with open('requirements.txt') as requirements_file:
    requirements = requirements_file.read().splitlines()

with open('requirements.test.txt') as requirements_file:
    test_requirements = requirements_file.read().splitlines()

setup(
    name='jakarto_datasets',
    description="Jakarto datasets containing realworld 3d data from lidar sensors.",
    version=module.__version__,
    long_description=readme,
    long_description_content_type="text/markdown",
    author="Loïc Messal",
    author_email='loic.messal@jakarto.com',
    url='https://github.com/jakarto3d/jakarto_datasets',
    packages=find_packages(where='src'),
    package_dir={'': 'src'},
    install_requires=requirements,
    setup_requires=test_requirements,
    tests_require=test_requirements,
    test_suite='tests',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    license="MIT License",
)
