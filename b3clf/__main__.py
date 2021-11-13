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

"""Package for BBB predictions."""
import argparse

from .b3clf import b3clf

try:
    from .version import __version__
except ImportError:
    __version__ = "0.0.0.post0"


def main():
    # This might be needed later, for this point just build a simple interface
    # description = """B3clf Command-Line Interface"""
    # parser = argparse.ArgumentParser(prog="b3clf", description=description)

    parser = argparse.ArgumentParser()
    parser.add_argument("-mol",
                        default="input.sdf",
                        type=str,
                        help="Input file with descriptors.")
    parser.add_argument("-sep",
                        type=str,
                        default="\s+|\t+",
                        help="Separator for input file.")
    parser.add_argument("-clf",
                        type=str,
                        default="xgb",
                        help="Machine Learning classifier type.")
    parser.add_argument("-sampling",
                        type=str,
                        default="classic_ADASYN",  # Change it for best sampling of XGBoost
                        help="Machine Learning classifier type.")
    parser.add_argument("-output",
                        type=str,
                        default="B3clf_output.xlsx",
                        help="Name of XLSX output file.")
    args = parser.parse_args()

    # Input variables
    _ = b3clf(mol_in=args.mol,
              sep=args.sep,
              classification=args.clf,
              sampling=args.sampling,
              output=args.output,
              )


if __name__ == "__main__":
    """B3clf command-line interface."""
    main()
