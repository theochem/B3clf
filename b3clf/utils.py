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

"""B3clf utility functions."""

import os

import numpy as np
import pandas as pd
from joblib import load

__all__ = [
    "get_descriptors",
    "select_descriptors",
    "scale_descriptors",
    "get_clf",
    "predict_permeability",
]


def get_descriptors(df):
    """Create features dataframe and information dataframe from provided path."""
    if type(df) == str:
        if df.lower().endswith(".sdf"):
            df = pd.read_sdf(df)
        elif df.lower().endswith(".xlsx"):
            df = pd.read_excel(df, engine="openpyxl")
        elif df.lower().endswith(".csv"):
            df = pd.read_csv(df)
        else:
            raise ValueError(
                "Command-line tool only supports feature files in .XLSX format"
            )

    info_list = ["compoud_name", "SMILES", "cid", "category", "inchi", "Energy"]

    # drop infinity and NaN values
    df.replace([np.inf, -np.inf], np.nan, inplace=True)
    df.dropna(axis=0, inplace=True)

    features_cols = [col for col in df.columns.to_list() if col not in info_list]
    X = df[features_cols]
    info_cols = [col for col in df.columns.to_list() if col in info_list]
    if len(info_cols) != 0:
        info = df[info_cols]
    else:
        info = pd.DataFrame(index=df.index)

    return X, info


def select_descriptors(df):
    """Select certain Padel descriptors, which are those taken by B3clf models."""
    dirname = os.path.dirname(__file__)
    with open(os.path.join(dirname, "feature_list.txt")) as f:
        selected_list = f.read().splitlines()

    df_selected = df[[col for col in df.columns.to_list() if col in selected_list]]

    return df_selected


def scale_descriptors(df):
    """Scale input features using B3DB Standard Scaler.

    The b3db_scaler was fitted using the full B3DB dataset.
    """

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "pre_trained", "b3clf_scaler.joblib")
    b3db_scaler = load(filename)
    df_new = b3db_scaler.transform(df)

    return df_new


def get_clf(clf_str, sampling_str):
    """Get b3clf fitted classifier"""
    clf_list = ["dtree", "knn", "logreg", "xgb"]
    sampling_list = [
        "borderline_SMOTE",
        "classic_ADASYN",
        "classic_RandUndersampling",
        "classic_SMOTE",
        "kmeans_SMOTE",
        "common",
    ]

    # This could be moved to an initial check method for input parameters
    if clf_str not in clf_list:
        raise ValueError("Input classifier is not supported; got {}".format(clf_str))
    elif sampling_str not in sampling_list:
        raise ValueError(
            "Input sampling method is not supported; got {}".format(sampling_str)
        )

    dirname = os.path.dirname(__file__)
    # Move data to new storage place for packaging
    clf_path = os.path.join(
        dirname, "pre_trained", "b3clf_{}_{}.joblib".format(clf_str, sampling_str)
    )

    clf = load(clf_path)

    return clf


def predict_permeability(
    clf_str, sampling_str, mol_features, info_df, threshold="none"
):
    """Compute and store BBB predicted label and predicted probability to results dataframe."""

    # load the threshold data
    dirname = os.path.dirname(__file__)
    fpath_thres = os.path.join(dirname, "data", "B3clf_thresholds.xlsx")
    df_thres = pd.read_excel(fpath_thres, index_col=0, engine="openpyxl")
    # default threshold is 0.5
    label_pool = np.zeros(mol_features.shape[0], dtype=int)

    # get the classifier
    clf = get_clf(clf_str=clf_str, sampling_str=sampling_str)

    if type(mol_features) == pd.DataFrame:
        if mol_features.index.tolist() != info_df.index.tolist():
            raise ValueError(
                "Features_df and Info_df do not have the same index. Internal processing error"
            )

    # get predicted probabilities
    info_df.loc[:, "B3clf_predicted_probability"] = clf.predict_proba(mol_features)[
        :, 1
    ]
    # get predicted label from probability using the threshold
    mask = np.greater_equal(
        info_df["B3clf_predicted_probability"].to_numpy(),
        # df_thres.loc[clf_str + "-" + sampling_str, threshold])
        df_thres.loc["xgb-classic_ADASYN", threshold],
    )
    label_pool[mask] = 1
    # save the predicted labels
    info_df["B3clf_predicted_label"] = label_pool

    # info_df["B3clf_predicted_label"] = info_df["B3clf_predicted_label"].astype("int64")
    info_df.reset_index(inplace=True)

    return info_df
