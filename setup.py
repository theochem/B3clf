#!/usr/bin/env python3
# B3clf is an input and output module for quantum chemistry.
# Copyright (C) 2021 The B3clf Development Team
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
# --
"""Installation script for B3clf.

Directly calling this script is only needed by B3clf developers in special
circumstances. End users are recommended to install B3clf with pip.
"""

import os

from setuptools import setup


def get_version_info():
    """Read __version__ and DEV_CLASSIFIER from version.py, using exec, not import."""
    fn_version = os.path.join("B3clf", "_version.py")
    if os.path.isfile(fn_version):
        myglobals = {}
        with open(fn_version, "r") as f:
            exec(f.read(), myglobals)  # pylint: disable=exec-used
        return myglobals["__version__"], myglobals["DEV_CLASSIFIER"]
    return "0.0.0.post0", "Development Status :: 2 - Pre-Alpha"


def get_readme():
    """Load README.md."""
    with open("README.md") as fhandle:
        return fhandle.read()


VERSION, DEV_CLASSIFIER = get_version_info()

setup(
    name="B3clf",
    version=VERSION,
    description="Models for blood-brain barrier classifications with resampling strategies.",
    long_description=get_readme(),
    author="Ayers Lab",
    author_email="ayersp@mcmaster.ca",
    url="https://github.com/theochem/B3clf",
    package_dir={"B3clf": "B3clf"},
    packages=["B3clf"],
    include_package_data=True,
    # todo: add support of this
    # entry_points={
    #     "console_scripts": ["B3clf-convert = B3clf.__main__:main"]
    # },
    classifiers=[
        DEV_CLASSIFIER,
        "Environment :: Console",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        # todo: check if it works in mac and windows
        "Operating System :: POSIX :: Linux",
        "Programming Language :: Python :: 3",
        "Topic :: Scientific/Engineering :: Chemistry",
        "Topic :: Scientific/Engineering :: Bio-Informatics",
        "Intended Audience :: Science/Research",
    ],
    python_requires=">=3.7.0",
    setup_requires=["numpy>=1.21.4", "scipy>=1.7.2"],
    install_requires=["numpy>=1.21.4", "scipy>=1.7.2", "scikit-learn==0.24.2"],
)
