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

# Temporary modules
from rdkit.Chem import PandasTools
import pandas as pd

__author__ = "Juansa Collins & Fanwang Meng"
__version__ = "0.1.0"



if __name__ == "__main__":
    # This might be needed later, for this point just build a simple interface
    # """Parse command-line input for B3clf executable."""
    # description = """B3clf Command-Line Interface"""
    # parser = argparse.ArgumentParser(prog="b3clf", description=description)

    parser = argparse.ArgumentParser()
    parser.add_argument("-descriptors",  # Test with /Users/JuansaCollins/Documents/Academico/MITACS/Ayers-Group/B3DB/repo_imbalanced_learning/command-line_tool/input_test.xlsx
                        type=str,
                        default=None,
                        help="Input file with descriptors.")
    parser.add_argument("-clf",
                        type=str,
                        default="xgb",
                        help="Machine Learning classifier type.")
    parser.add_argument("-sampling",
                        type=str,
                        default="common",  # Change it for best sampling of XGBoost
                        help="Machine Learning classifier type.")
    args = parser.parse_args()

    descriptors_path = args.descriptors
    clf_str = args.clf
    sampling_str = args.sampling

    descriptors_path = "/Users/JuansaCollins/Documents/Academico/MITACS/Ayers-Group/B3DB/B3clf_command-line/b3clf/files/input_test.xlsx"

    # ===================
    # Pipeline
    # ===================

    # Geometry Optimization
    # Input: 
    #   - SDF file with molecular geometries
    #   - Text file with SMILES strings or Names

    csv_path = "/Users/JuansaCollins/Documents/Academico/MITACS/Ayers-Group/B3DB/B3clf_command-line/b3clf/files/test_SMILES.csv"
    test_sdf = "SMI_to_SDF.sdf"
    
    df_mol = pd.read_csv(csv_path, sep="\s+", header=None)
    print(df_mol)
    
    geometry_optimize(input_fname=csv_path, output_sdf=test_sdf, sep="\s+")

    test_df = PandasTools.LoadSDF(test_sdf).drop("ROMol", axis=1)

    print(test_df)

    raise RuntimeError

    # ===================
    # Get descriptors
    # ===================
    X_features, info_df = get_descriptors(descriptors_path)

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

    