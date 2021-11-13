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

"""
Main B3clf Script.

Usage: b3clf molecules.sdf -clf xgb -sampling borderline_SMOTE
----------
ToDo: Store and delete temporal files (sdf & PaDel features)    
ToDo: Enable b3clf prediction without PaDeL calculation from PaDeL descriptor input
"""

from .descriptor_padel import compute_descriptors
from .geometry_opt import geometry_optimize
from .utils import (get_descriptors, get_clf, select_descriptors, scale_descriptors,
                    predict_permeability)

__all__ = [
    "b3clf",
]


def b3clf(mol_in,
          sep,
          classification,
          sampling,
          output,
          ):
    """Use B3clf for BBB classifications."""

    features_out = "internal_padel_descriptors.xlsx"
    internal_sdf = "internal.sdf"

    # Geometry optimization
    # Input:
    # * Either an SDF file with molecular geometries or a text file with SMILES strings

    geometry_optimize(input_fname=mol_in, output_sdf=internal_sdf, sep=sep)

    # Compute descriptors with PaDel
    # Internal file name passed should be relative to this directory I think
    _ = compute_descriptors(sdf_file=internal_sdf, excel_out=features_out)

    # Get computed descriptors
    X_features, info_df = get_descriptors(df=features_out)
    # X_features, info_df = get_descriptors(internal_df)

    # Select descriptors
    X_features = select_descriptors(df=X_features)

    # Scale descriptors
    X_features = scale_descriptors(df=X_features)

    # Get classifier
    clf = get_clf(clf_str=classification, sampling_str=sampling)

    # Get classifier
    result_df = predict_permeability(clf=clf, features_df=X_features, info_df=info_df)

    # Get classifier
    display_cols = ["ID", "SMILES", "B3clf_predicted_probability", "B3clf_predicted_label"]

    display_df = result_df[[col for col in result_df.columns.to_list() if col in display_cols]]
    # print(display_df)

    display_df.to_excel(output, index=None)
    return display_df
