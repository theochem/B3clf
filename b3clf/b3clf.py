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


def b3clf(descriptors_path,
          sep,
          clf_str,
          sampling_str,
          xlsx_output,
          ):
    """Use B3clf for BBB classifications."""

    features_out = "internal_padel_descriptors.xlsx"
    internal_sdf = "internal.sdf"

    # ===================
    # Pipeline
    # ===================

    # ===================
    # Geometry optimization
    # ===================
    # Input:
    # * Either an SDF file with molecular geometries or a text file with SMILES strings

    geometry_optimize(input_fname=descriptors_path, output_sdf=internal_sdf, sep=sep)

    # ===================
    # Compute descriptors with PaDel
    # ===================
    # Internal file name passed should be relative to this directory I think
    _ = compute_descriptors(sdf_file=internal_sdf, excel_out=features_out)

    # ===================
    # Get computed descriptors
    # ===================
    X_features, info_df = get_descriptors(df=features_out)
    # X_features, info_df = get_descriptors(internal_df)

    # ===================
    # Select descriptors
    # ===================
    X_features = select_descriptors(df=X_features)

    # ===================
    # Scale descriptors
    # ===================
    X_features = scale_descriptors(df=X_features)

    # ===================
    # Get classifier
    # ===================

    clf = get_clf(clf_str=clf_str, sampling_str=sampling_str)

    # ===================
    # Get classifier
    # ===================
    result_df = predict_permeability(clf=clf, features_df=X_features, info_df=info_df)

    # ===================
    # Get classifier
    # ===================
    display_cols = ["ID", "SMILES", "B3clf_predicted_probability", "B3clf_predicted_label"]

    display_df = result_df[[col for col in result_df.columns.to_list() if col in display_cols]]
    # print(display_df)

    display_df.to_excel(xlsx_output, index=None)
    return display_df
