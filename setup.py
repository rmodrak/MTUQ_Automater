from __future__ import print_function
import argparse
import os
import sys
import numpy
from setuptools import find_packages, setup, Extension
from setuptools.command.test import test as test_command


setup(
    name="mtuq_automater",
    version="0.2.0",
    license='BSD2',
    description="moment tensor (mt) uncertainty quantification (uq)",
    author="Ryan Modrak",
    url="https://github.com/uafgeotools/mtuq",
    packages=find_packages(),
    zip_safe=False,
    classifiers=[
        # complete classifier list:
        # http://pypi.python.org/pypi?%3Aaction=list_classifiers
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Science/Research",
        "Operating System :: Unix",
        "Operating System :: POSIX",
        "Operating System :: Microsoft :: Windows",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: Implementation :: CPython",
        "Topic :: Scientific/Engineering",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    keywords=[
        "seismology"
    ],
    python_requires='>=3',
    install_requires=[
        "numpy<2", 
        "scipy",
        "obspy",
        "instaseis",
        "pandas",
        "xarray",
        "netCDF4",
        "h5py",
        "tables",
        #"mpi4py",
        "retry",
        "flake8",
        "nose",
        "pytest",
    ],
)

