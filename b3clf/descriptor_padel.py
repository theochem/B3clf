import pandas as pd
from padelpy import from_sdf
from rdkit import Chem

"""Compute PaDEL descriptors."""


def compute_descriptors(sdf_file,
                        excel_out="padel_descriptors.xlsx",
                        timeout=None):
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
                    output_csv=None,
                    descriptors=True,
                    fingerprints=False,
                    timeout=timeout)
    df_desc = pd.DataFrame(desc)

    # add molecule names to dataframe
    suppl = Chem.SDMolSupplier(sdf_file,
                               sanitize=True,
                               removeHs=False,
                               strictParsing=True)
    mol_names = [mol.GetProp("_Name") for mol in suppl]
    df_desc.index = mol_names
    df_desc.index.name = "Name"

    # save results
    if excel_out is not None:
        df_desc.to_excel(excel_out, engine="openpyxl")

    return df_desc
