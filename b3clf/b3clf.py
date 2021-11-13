"""
Main B3clf Script.

Usage: b3clf molecules.sdf -clf xgb -sampling borderline_SMOTE
----------
ToDo: Store and delete temporal files (sdf & PaDel features)    
ToDo: Enable b3clf prediction without PaDeL calculation from PaDeL descriptor input
"""

import argparse

from utils import get_descriptors, select_descriptors, scale_descriptors, get_clf, predict_BBB, display_df
from geometry_opt import geometry_optimize
from descriptor_padel import compute_descriptors

# Temporary modules
# from rdkit.Chem import PandasTools
import pandas as pd

__author__ = "Ayers-Lab"
__version__ = "0.1.0"



if __name__ == "__main__":
    """B3clf command-line interface.
    """
    # This might be needed later, for this point just build a simple interface
    # description = """B3clf Command-Line Interface"""
    # parser = argparse.ArgumentParser(prog="b3clf", description=description)

    parser = argparse.ArgumentParser()
    parser.add_argument("-mol",
                        type=str,
                        default=None,
                        help="Input file with descriptors.")
    parser.add_argument("-output",
                        type=str,
                        default="B3clf_output.xlsx",
                        help="Name of XLSX output file.")
    parser.add_argument("-clf",
                        type=str,
                        default="xgb",
                        help="Machine Learning classifier type.")
    parser.add_argument("-sampling",
                        type=str,
                        default="classic_ADASYN",  # Change it for best sampling of XGBoost
                        help="Machine Learning classifier type.")
    parser.add_argument("-sep",
                        type=str,
                        default="\s+|\t+",
                        help="Separator for input file.")
    
    args = parser.parse_args()

    # Input variables
    descriptors_path = args.mol
    clf_str = args.clf
    sampling_str = args.sampling
    xlsx_output = args.output

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

    geometry_optimize(input_fname=descriptors_path, output_sdf=internal_sdf, sep=args.sep)

    # ===================
    # Compute descriptors with PaDel
    # ===================
    # Internal file name passed should be relative to this directory I think
    internal_df = compute_descriptors(sdf_file=internal_sdf, excel_out=features_out)

    print("This is the internal DF")
    print(internal_df.shape)
    print(internal_df.index)
    print(internal_df.columns)
    print(internal_df)

    print("Try to reset index")
    internal_df.reset_index(inplace=True)
    print("Here is after main reset")
    # ===================
    # Get computed descriptors
    # ===================
    #X_features, info_df = get_descriptors(features_out)
    X_features, info_df = get_descriptors(internal_df)

    # ===================
    # Select descriptors
    # ===================
    X_features = select_descriptors(X_features)

    # ===================
    # Scale descriptors
    # ===================
    X_features = scale_descriptors(X_features)

    # ===================
    # Get classifier
    # ===================
    clf = get_clf(clf_str, sampling_str)

    # ===================
    # Get classifier
    # ===================
    result_df = predict_BBB(clf, X_features, info_df)

    # ===================
    # Get classifier
    # ===================
    display_df = display_df(result_df)
    
    print(display_df)

    display_df.to_excel(xlsx_output, index=None)

    

    