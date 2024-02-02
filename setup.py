# -*- coding: utf-8 -*-
# The B3clf library computes the blood-brain barrier (BBB) permeability
# of organic molecules with resampling strategies.
#
# Copyright (C) 2021 The Ayers Lab
#
# This file is part of B3clf.
#
# B3clf is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 3
# of the License, or (at your option) any later version.
#
# B3clf is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program; if not, see <http://www.gnu.org/licenses/>
#
# --

"""Installation script for B3clf.

Directly calling this script is only needed by B3clf developers in special
circumstances. End users are recommended to install B3clf with pip.
"""

import os

from setuptools import find_packages, setup


def get_version_info():
    """Read __version__ and DEV_CLASSIFIER from version.py, using exec, not import."""
    fn_version = os.path.join("b3clf", "version.py")
    if os.path.isfile(fn_version):
        myglobals = {}
        with open(fn_version, "r") as f:
            exec(f.read(), myglobals)  # pylint: disable=exec-used
        return myglobals["__version__"]
    return "0.0.0.post0"


def get_readme():
    """Load README.md."""
    with open("README.md") as fhandle:
        return fhandle.read()


VERSION = get_version_info()

setup(
    name="b3clf",
    version=VERSION,
    description="Models for blood-brain barrier classifications with resampling strategies.",
    long_description=get_readme(),
    author="Ayers Lab",
    author_email="ayersp@mcmaster.ca",
    url="https://github.com/theochem/B3clf",
    package_dir={"B3clf": "b3clf"},
    # packages=["b3clf"],
    packages=find_packages(),
    include_package_data=True,
    entry_points={
        "console_scripts": ["b3clf = b3clf.__main__:main"]
    },
    classifiers=[
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        # todo: check if it works in mac and windows
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Science/Engineering :: Molecular Science",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Intended Audience :: Science/Research",
    ],
    python_requires=">=3.7.0",
    setup_requires=["numpy>=1.21.4", "scipy>=1.7.2"],
    install_requires=["numpy>=1.21.4", "scipy>=1.7.2", "scikit-learn==1.0.1"],
)
