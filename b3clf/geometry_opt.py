# import os
# import subprocess

import pandas as pd
from rdkit import Chem
from rdkit.Chem import AllChem

"""Convert SMILES to 3D and/or minimize the geometry from SDF with force field."""


def geometry_optimize(input_fname,
                      output_sdf,
                      steps_opt=10000,
                      # convergence=1.e-7,
                      tool="rdkit",
                      # optimization="cg",
                      force_field="MMFF94s",
                      smi_col=None,
                      sep="\s+"):
    """Generate 3D coordinates and run geometry optimization with force field."""

    # optimize the 3d coordinates
    # use RDKit to minimize the geometry
    if tool.lower() == "rdkit":
        minimize_with_rdkit(input_molfname=input_fname,
                            sdf_out=output_sdf,
                            maxIters=steps_opt,
                            force_field=force_field,
                            smi_col=smi_col,
                            sep=sep)
    # use openbabel to minimize the geometry
    elif tool == "openbabel":
        # minimize_with_openbabel(input_molfname=input_fname,
        #                         sdf_out=output_sdf,
        #                         steps=steps_opt,
        #                         optimization=optimization,
        #                         convergence=convergence,
        #                         force_field=force_field,
        #                         smi_col=smi_col)
        raise ValueError("OpenBabel is not supported yet.")
    else:
        raise ValueError("{} not implemented yet.".format(tool))


def minimize_with_rdkit(input_molfname,
                        sdf_out,
                        smi_col=None,
                        mol_name_col=None,
                        maxIters=400,
                        force_field="MMFF94s",
                        sep="\s+"):
    """Add hydrogen for 3D coordinates and minimize the geometry with RdKit."""
    # load molecules
    if input_molfname.lower().endswith(".smi") or input_molfname.lower().endswith(".csv"):
        # todo: support .txt files
        # todo: add support of more flexible separators
        # todo: fix problem when mol_name is empty
        df_mol = pd.read_csv(input_molfname, sep=sep, engine="python", header=None)
        if df_mol.shape[1] == 1:
            # Case for only SMILES column
            smile_list = df_mol.iloc[:, -1].to_list()
            mol_name_list = df_mol.iloc[:, -1].to_list()
        else:
            # Case for SMILES and MOL name columns
            if smi_col is None:
                smile_list = df_mol.iloc[:, 0].to_list()
            else:
                smile_list = df_mol[smi_col].to_list()

            if mol_name_col is None:
            # todo: use name if column name is valid
                mol_name_list = df_mol.iloc[:, -1].to_list()
            else:
                mol_name_list = df_mol[mol_name_col].to_list()

        mols = []
        for idx, smi in enumerate(smile_list):
            mol = Chem.MolFromSmiles(smi)
            # This will overwrite 
            if mol is not None:
                mol.SetProp("_Name", mol_name_list[idx])
                mols.append(mol)

    elif input_molfname.lower().endswith(".sdf"):
        suppl = Chem.SDMolSupplier(input_molfname,
                                   sanitize=True,
                                   removeHs=False,
                                   strictParsing=True)
        mols = [mol for mol in suppl]
        for idx, mol in enumerate(mols):
            if (mol.GetProp("_Name") == "") or (mol.GetProp("_Name") is None):
                smi = Chem.MolToSmiles(mol)
                mol.SetProp("_Name", smi)
                mols[idx] = mol

    writer = Chem.SDWriter(sdf_out)
    for idx, mol in enumerate(mols):
        mol = Chem.AddHs(mol)
        if force_field == "MMFF94s":
            # use MMFF~ force field if possible

            # taken from
            # https://open-babel.readthedocs.io/en/latest/Forcefields/mmff94.html
            # Some experiments and most theoretical calculations show significant pyramidal
            # “puckering” at nitrogens in isolated structures. The MMFF94s (static) variant has
            # slightly different  out-of-plane bending and dihedral torsion parameters to planarize
            # certain types of delocalized trigonal N atoms, such as aromatic aniline. This provides
            # a better match to the time-average molecular geometry in solution or crystal
            # structures.
            #
            # If you are comparing force-field optimized molecules to crystal structure geometries,
            # we recommend using the MMFF94s variant for this reason. All other parameters are
            # identical. However, if you are performing “docking” simulations, consideration of
            # active solution conformations, or other types of computational studies, we recommend
            # using the MMFF94 variant, since one form or another of the N geometry will
            # predominate.

            AllChem.EmbedMolecule(mol, randomSeed=999)
            # the following code will raise some errors
            mini_tag = AllChem.MMFFOptimizeMolecule(mol, force_field, maxIters=maxIters)
            # 0 optimize converged
            # -1 can not set up force field
            # 1 more iterations required
            if mini_tag == 0:
                writer.write(mol)
            else:
                if mini_tag == 1:
                    AllChem.MMFFOptimizeMolecule(mol, force_field, maxIters=maxIters * 2)
                elif mini_tag == -1:
                    AllChem.UFFOptimizeMolecule(mol, maxIters=400)
                writer.write(mol)

        elif force_field == "uff":
            # use uff force field if possible
            AllChem.EmbedMolecule(mol, randomSeed=999)
            # the following code will raise some errors
            mini_tag = AllChem.UFFOptimizeMolecule(mol, maxIters=maxIters)
            # 0 optimize converged
            # -1 can not set up force field
            # 1 more iterations required
            if mini_tag == 0:
                writer.write(mol)
            else:
                if mini_tag == 1:
                    AllChem.UFFOptimizeMolecule(mol, maxIters=maxIters * 2)
                elif mini_tag == -1:
                    AllChem.MMFFOptimizeMolecule(mol, "MMFF94s", maxIters=maxIters)
                writer.write(mol)

        else:
            raise NotImplementedError("This method is not implemented yet.")

    writer.close()
    print("Geometry optimization with RDKit is done.")

# todo: now the implementation is not supporting adding molecule name (such as SMILES strings)
# def minimize_with_openbabel(input_molfname,
#                             sdf_out,
#                             steps=10000,
#                             convergence=1.e-7,
#                             optimization="cg",
#                             force_field="GAFF",
#                             smi_col=None):
#     """Minimize the geometries with openbabel.
#
#     Parameters
#     ----------
#     input_molfname : str
#         Input molecule fie name.
#     sdf_out : str
#         Output molecule file name.
#     steps : int, optional
#         Specify the maximum number of steps. default=2500.
#     optimization : str, optional
#         Use conjugate gradients ("cg") or steepest descent ("sd") algorithm for optimization.
#         Default="cg".
#     convergence : float, optional
#         convergence threshold. Default=1.e-7.
#     force_field : str, optional
#         ForceField name including Generalized Amber Force Field (gaff), Ghemical Force Field
#         (ghemical), MMFF94 Force Field (mmff94) and Universal Force Field (uff). Default="gaff".
#     """
#
#     # https://open-babel.readthedocs.io/en/latest/Command-line_tools/babel.html#forcefield-energy-and-minimization
#     subprocess.Popen(["obabel", input_molfname, "-h", "-O", sdf_out,
#                       "--gen3d", "--minimize",
#                       "--n", str(steps), "--sd", optimization, "--crit",
#                       str(convergence), "--ff", force_field])
#     print("Geometry optimization with OpenBabel is done.")
