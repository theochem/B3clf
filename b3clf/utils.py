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
    """Create features dataframe and information dataframe from provided path.

    """
    if isinstance(df, pd.DataFrame):
        pass
    elif df.lower().endswith(".xlsx"):
        df = pd.read_excel(df)
    else:
        raise ValueError(
            "Command-line tool only supports feature files in .XLSX format")

    info_list = ["compoud_name", "SMILES", "cid", "category", "inchi", "Energy"]

    df = df.set_index("ID")  # This could change
    X = df.drop([col for col in df.columns.to_list()
                 if col in info_list], axis=1)
    info = df[[col for col in df.columns.to_list() if col in info_list]]

    return X, info


def select_descriptors(df):
    """Select certain Padel descriptors, which are those taken by B3clf models.

    """
    dirname = os.path.dirname(__file__)
    with open(os.path.join(dirname, "feature_list.txt")) as f:
        selected_list = f.read().splitlines()

    df = df[[col for col in df.columns.to_list() if col in selected_list]]

    return df


def scale_descriptors(df):
    """Scale input features using B3DB Standard Scaler.

    The b3db_scaler was fitted using the full B3DB dataset.
    """

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "pre_trained", "b3db_scaler.joblib")
    b3db_scaler = load(filename)
    df.iloc[:, :] = b3db_scaler.transform(df)

    return df


def get_clf(clf_str, sampling_str):
    """Get b3clf fitted classifier
    """
    clf_list = ["dtree", "knn", "logreg", "xgb"]
    sampling_list = ["borderline_SMOTE", "classic_ADASYN",
                     "classic_RandUndersampling", "classic_SMOTE", "kmeans_SMOTE", "common"]

    # This could be moved to an initial check method for input parameters
    if clf_str not in clf_list:
        raise ValueError(
            "Input classifier is not supported; got {}".format(clf_str))
    elif sampling_str not in sampling_list:
        raise ValueError(
            "Input sampling method is not supported; got {}".format(sampling_str))

    dirname = os.path.dirname(__file__)
    # Move data to new storage place for packaging
    clf_path = os.path.join(
        dirname, "pre_trained", "b3clf_{}_{}.joblib".format(clf_str, sampling_str))

    clf = load(clf_path)

    return clf


def predict_permeability(clf, features_df, info_df):
    """Compute and store BBB predicted label and predicted probability to results dataframe
    """
    if features_df.index.tolist() != info_df.index.tolist():
        raise ValueError(
            "Features_df and Info_df do not have the same index. Internal processing error")
    for index, row in features_df.iterrows():
        # try:
        info_df.loc[index, "B3clf_predicted_probability"] = clf.predict_proba(
            row.to_numpy().reshape(1, -1))[:, 1]
        info_df.loc[index, "B3clf_predicted_label"] = clf.predict(row.to_numpy().reshape(1, -1))
        # except:
        #     info_df.loc[index, "B3clf_predicted_probability"] = "Invalid descriptors"
        #     info_df.loc[index, "B3clf_predicted_label"] = "Invalid descriptors"

    # info_df["B3clf_predicted_label"] = info_df["B3clf_predicted_label"].astype("int64")
    info_df.reset_index(inplace=True)

    return info_df
