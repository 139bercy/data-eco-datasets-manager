#!/usr/bin/env python
# -*- coding: utf-8 -*-
from setuptools import setup, find_packages


with open("README.md") as readme_file:
    readme = readme_file.read()

requirements = [
    "Click>=8.0",
]

setup_requirements = [
    "pytest-runner",
]

test_requirements = [
    "pytest",
]

setup(
    author="tongyeouki",
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "Programming Language :: Python :: 3.11",
    ],
    description="Handle datasets using Opendatasoft API",
    entry_points={
        "console_scripts": [
            "app=cli:cli",
        ],
    },
    install_requires=requirements,
    long_description=readme,
    include_package_data=True,
    platforms="any",
    keywords="ods-datasets-manager",
    name="ods-datasets-manager",
    packages=find_packages("src"),
    package_dir={"": "src"},
    setup_requires=setup_requirements,
    test_suite="tests",
    tests_require=test_requirements,
    version="0.0.1",
    zip_safe=False,
)
