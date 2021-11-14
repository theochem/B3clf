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
"""

# Todo: Enable b3clf prediction without PaDeL calculation from PaDeL descriptor input
import os

from .descriptor_padel import compute_descriptors
from .geometry_opt import geometry_optimize
from .utils import (get_clf, get_descriptors, predict_permeability,
                    scale_descriptors, select_descriptors)

__all__ = [
    "b3clf",
]


def b3clf(mol_in,
          sep="\s+|\t+",
          clf="xgb",
          sampling="classic_ADASYN",
          output="B3clf_output.xlsx",
          verbose=1,
          keep_features="no",
          keep_sdf="no",
          ):
    """Use B3clf for BBB classifications with resampling strategies.

    Parameters
    ----------
    mol_in : str
        Input molecule text fie which can be SMILES strings (file extension with .smi or .csv) or
        SDF file format. No space is allowed for molecular name if input is a file with SMILES strings.
    sep : str, optional
        Separator used to parse data if a text file with SMILES strings is provided.
        Default="\s+|\t+" which will take any space and any tab as delimiter.
    clf: str, optional
        Classification algorithm, which can be "dtree" for decision trees, "knn" for kNN, "logreg"
        for logistical regression and "xgb" for XGBoost. Default="xgb".
    sampling : str, optional
        Sampling strategies that can be used which includes "common",
        "RandUndersampling", "SMOTE", "borderline_SMOTE", "kmeans_SMOTE" and "classic_ADASYN". The
        "common" denotes that no resampling strategy is employed. Default="classic_ADASYN".
    output : str, optional
        Output file name for the predicted results consisting molecule ID, predicted probability
        and labels for BBB permeability.
    verbose : int, optional
        When verbose is zero, no results are printed out. Otherwise, the program prints the
        predictions. Default=1.
    keep_features : str, optional
        To keep intermediate molecular feature file, "yes" or "no". Default="no".
    keep_sdf : str, optional
        To keep intermediate molecular geometry file with 3D coordinates, "yes" or "no".
        Default="no".

    Returns
    -------
    result_df : pandas.DataFrame
        Result of BBB predictions with molecule ID/name, predicted probability and predicted labels.

    """

    features_out = "internal_padel_descriptors.xlsx"
    internal_sdf = "internal.sdf"

    # Geometry optimization
    # Input:
    # * Either an SDF file with molecular geometries or a text file with SMILES strings

    geometry_optimize(input_fname=mol_in, output_sdf=internal_sdf, sep=sep)

    # compute descriptors with PaDel
    # internal file name passed should be relative to this directory I think
    _ = compute_descriptors(sdf_file=internal_sdf, excel_out=features_out)

    # Get computed descriptors
    X_features, info_df = get_descriptors(df=features_out)
    # X_features, info_df = get_descriptors(internal_df)

    # Select descriptors
    X_features = select_descriptors(df=X_features)

    # Scale descriptors
    X_features = scale_descriptors(df=X_features)

    # Get classifier
    clf = get_clf(clf_str=clf, sampling_str=sampling)

    # Get classifier
    result_df = predict_permeability(clf=clf, features_df=X_features, info_df=info_df)

    # Get classifier
    display_cols = ["ID", "SMILES", "B3clf_predicted_probability", "B3clf_predicted_label"]

    result_df = result_df[[col for col in result_df.columns.to_list() if col in display_cols]]
    if verbose != 0:
        print(result_df)

    result_df.to_excel(output, index=None, engine="openpyxl")

    if keep_features != "yes":
        os.remove(features_out)
    if keep_sdf != "yes":
        os.remove(internal_sdf)

    return result_df
