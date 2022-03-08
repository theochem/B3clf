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

import numpy as np
import pandas as pd
from .descriptor_padel import compute_descriptors
from .geometry_opt import geometry_optimize
from .utils import (get_descriptors, predict_permeability,
                    scale_descriptors, select_descriptors)

__all__ = [
    "b3clf",
]


def b3clf(input_fname,
          input_type="feature",
          sep="\s+|\t+",
          engine="openpyxl",
          clf="xgb",
          sampling="classic_ADASYN",
          output="B3clf_output.xlsx",
          verbose=1,
          random_seed=42,
          keep_features="no",
          keep_sdf="no",
          threshold="none",
          **kwargs,
          ):
    """Use B3clf for BBB classifications with resampling strategies.

    Parameters
    ----------
    input_fname : str
        Input molecule text"job_padel.sh" fie which can be SMILES strings (file extension with .smi or .csv) or
        SDF file format. No space is allowed for molecular name if input is a file with SMILES
        strings.
    input_type : str, optional
        Input file type. Options are "feature" or "mol". Default="feature".
    sep : str, optional
        Separator used to parse data if a text file with SMILES strings is provided.
        Default="\s+|\t+" which will take any space and any tab as delimiter.
    engine : str, optional
        Engine used to load input feature files. Options are "openpyxl", "xlrd", "odf", "pyxlsb"
        for EXCEL file related formats.
        For more information, see
        https://pandas.pyda"job_padel.sh"ta.org/pandas-docs/stable/io.html#excel-formats.
        For CSV related text files, use "c", "python" or "pyarrow"
        (https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html)
        Default="openpyxl".
    clf: str, optional
        Classification algorithm, which can be "dtree" for decision trees, "knn" for kNN, "logreg"
        for logistical regression and "xgb" for XGBoost. Default="xgb".
    sampling : str, optional
        Sampling strategies that can be used which includes "common",
        "RandUndersampling""job_padel.sh", "SMOTE", "borderline_SMOTE", "kmeans_SMOTE" and "classic_ADASYN". The
        "common" denotes that no resampling strategy is employed. Default="classic_ADASYN".
    output : str, optional
        Output file name for the predicted results consisting molecule ID, predicted probability
        and labels for BBB permeability.
    verbose : int, optional
        When verbose is zero, no results are printed out. Otherwise, the program prints the
        predictions. Default=1.
    random_seed : int, optional
        Random seed for reproducibility. Default=42.
    keep_features : str, optional
        To keep intermediate molecular feature file, "yes" or "no". Default="no".
    keep_sdf : str, optional
        To keep intermediate molecular geometry file with 3D coordinates, "yes" or "no".
        Default="no".
    threshold : str, optional
        To set the threshold for the predicted probability which can be "none". "J_threshold" and
        "F_threshold". "J_threshold" will use threshold optimized from Youden’s J statistic.
        "F_threshold" will use threshold optimized from F score. Default="none".
    **kwargs : dict, optional
        Additional keyword arguments for the loading of input feature files.

    Returns
    -------
    result_df : pandas.DataFrame
        Result of BBB predictions with molecule ID/name, predicted probability and predicted labels.

    """

    # set random seed
    if random_seed is not None:
        rng = np.random.default_rng(random_seed)

    if input_type == "feature":
        # read in molecular feature file
        # https://openpyxl.readthedocs.io/en/stable/
        if os.path.splitext(input_fname)[1] in \
                {".xls", ".xlsx", ".xlsm", ".xltx", ".xltm", ".xlsb", ".odf", ".ods", ".odt"}:
            df_desc = pd.read_excel(input_fname, engine=engine)
        elif os.path.splitext(input_fname)[1] in {".csv", ".tsv", ".txt"}:
            df_desc = pd.read_csv(input_fname, sep=sep, engine=engine)
        else:
            raise ValueError(f"Unsupported file type for {input_fname}.")
        print(df_desc)

    elif input_type == "mol":
        mol_tag = os.path.basename(input_fname).split(".")[0]

        features_out = f"{mol_tag}_padel_descriptors.xlsx"
        internal_sdf = f"{mol_tag}_optimized_3d.sdf"
        # Geometry optimization
        # Input:000
        # * Either an SDF file with molecular geometries or a text file with SMILES strings
        geometry_optimize(input_fname=input_fname, output_sdf=internal_sdf, sep=sep)

        # compute descriptors with PaDel
        # internal file name passed should be relative to this directory I think
        df_desc = compute_descriptors(sdf_file=internal_sdf, excel_out=features_out)

        # clean up intermediate files
        if keep_features != "yes":
            os.remove(features_out)
        if keep_sdf != "yes":
            os.remove(internal_sdf)

    else:
        raise ValueError("""Input type must be either "feature" or "mol".""")

    # Get computed descriptors
    X_features, info_df = get_descriptors(df=df_desc)
    # X_features, info_df = get_descriptors(internal_df)

    # Select descriptors
    X_features = select_descriptors(df=X_features)

    # Scale descriptors
    X_features = scale_descriptors(df=X_features)

    # Get classifier
    # clf = get_clf(clf_str=clf, sampling_str=sampling)

    # Get classifier
    result_df = predict_permeability(clf_str=clf,
                                     sampling_str=sampling,
                                     features_df=X_features,
                                     info_df=info_df,
                                     threshold=threshold)

    # Get classifier
    display_cols = ["ID", "SMILES", "predicted_probability", "predicted_label"]

    result_df = result_df[[col for col in result_df.columns.to_list() if col in display_cols]]
    if verbose != 0:
        print(result_df)

    result_df.to_excel(output, index=None, engine="openpyxl")

    return result_df
