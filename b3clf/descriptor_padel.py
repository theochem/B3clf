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

import os
import sys

cwd = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(cwd, "padelpy"))

import pandas as pd
from rdkit import Chem
from padelpy import from_sdf

"""Compute PaDEL descriptors."""


def compute_descriptors(sdf_file,
                        # Change this to be an optional argument
                        excel_out="padel_descriptors.xlsx",
                        output_csv=None,
                        timeout=None,
                        time_per_molecule=-1,
                        ) -> pd.DataFrame:
    """Compute the chemical descriptors with PaDEL.

    Parameters
    ----------
    sdf_file : str
        Input SDF file name.
    excel_out : str, optional
        Excel file name to save PaDEL descriptors.
    timeout : float
        The maximum time, in seconds, for calculating the descriptors. When set to be None,
        this does not take effect.

    Returns
    -------
    df_desc : pandas.dataframe
        The computed pandas dataframe of PaDEL descriptors.

    """
    desc = from_sdf(sdf_file=sdf_file,
                    output_csv=output_csv,
                    descriptors=True,
                    fingerprints=False,
                    timeout=timeout,
                    maxruntime=time_per_molecule,
                    )
    df_desc = pd.DataFrame(desc)

    # add molecule names to dataframe
    suppl = Chem.SDMolSupplier(sdf_file,
                               sanitize=True,
                               removeHs=False,
                               strictParsing=True)
    mol_names = [mol.GetProp("_Name") for mol in suppl]
    df_desc.index = mol_names
    df_desc.index.name = "ID"

    # drop rows with nan values
    # todo: add imputation option
    df_desc.dropna(axis=0, inplace=True)

    # save results
    if excel_out is not None:
        df_desc.to_excel(excel_out, engine="openpyxl")

    return df_desc

    # Index will be the molecule's name
