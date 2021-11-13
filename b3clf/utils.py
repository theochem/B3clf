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
B3clf utility functions

"""
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
    selected_list = ['nAcid',
                     'ALogP',
                     'ALogp2',
                     'AMR',
                     'naAromAtom',
                     'nH',
                     'nN',
                     'nO',
                     'nS',
                     'nP',
                     'nF',
                     'nCl',
                     'nBr',
                     'nI',
                     'nX',
                     'ATS0m',
                     'ATS4m',
                     'ATS2s',
                     'AATS0m',
                     'AATS1m',
                     'AATS4m',
                     'AATS5m',
                     'AATS6m',
                     'AATS7m',
                     'AATS8m',
                     'AATS0v',
                     'AATS3v',
                     'AATS5v',
                     'AATS7v',
                     'AATS0e',
                     'AATS4e',
                     'AATS5e',
                     'AATS6e',
                     'AATS7e',
                     'AATS4p',
                     'AATS0i',
                     'AATS1i',
                     'AATS4i',
                     'AATS5i',
                     'AATS8i',
                     'AATS4s',
                     'AATS5s',
                     'AATS6s',
                     'AATS7s',
                     'AATS8s',
                     'ATSC2c',
                     'ATSC3c',
                     'ATSC4c',
                     'ATSC5c',
                     'ATSC6c',
                     'ATSC7c',
                     'ATSC8c',
                     'ATSC1m',
                     'ATSC2m',
                     'ATSC3m',
                     'ATSC4m',
                     'ATSC5m',
                     'ATSC6m',
                     'ATSC7m',
                     'ATSC8m',
                     'ATSC1v',
                     'ATSC2v',
                     'ATSC3v',
                     'ATSC4v',
                     'ATSC5v',
                     'ATSC6v',
                     'ATSC7v',
                     'ATSC8v',
                     'ATSC1e',
                     'ATSC2e',
                     'ATSC3e',
                     'ATSC4e',
                     'ATSC5e',
                     'ATSC6e',
                     'ATSC7e',
                     'ATSC8e',
                     'ATSC1i',
                     'ATSC2i',
                     'ATSC3i',
                     'ATSC4i',
                     'ATSC5i',
                     'ATSC6i',
                     'ATSC7i',
                     'ATSC8i',
                     'ATSC1s',
                     'ATSC3s',
                     'AATSC1c',
                     'AATSC4c',
                     'AATSC5c',
                     'AATSC6c',
                     'AATSC7c',
                     'AATSC8c',
                     'AATSC2m',
                     'AATSC3m',
                     'AATSC4m',
                     'AATSC5m',
                     'AATSC6m',
                     'AATSC7m',
                     'AATSC8m',
                     'AATSC0v',
                     'AATSC4v',
                     'AATSC5v',
                     'AATSC6v',
                     'AATSC7v',
                     'AATSC8v',
                     'AATSC3e',
                     'AATSC4e',
                     'AATSC5e',
                     'AATSC6e',
                     'AATSC7e',
                     'AATSC8e',
                     'AATSC1p',
                     'AATSC2p',
                     'AATSC3p',
                     'AATSC4p',
                     'AATSC3i',
                     'AATSC4i',
                     'AATSC5i',
                     'AATSC6i',
                     'AATSC7i',
                     'AATSC8i',
                     'AATSC1s',
                     'AATSC2s',
                     'AATSC3s',
                     'AATSC4s',
                     'AATSC6s',
                     'AATSC8s',
                     'MATS1c',
                     'MATS3c',
                     'MATS3m',
                     'MATS4m',
                     'MATS5m',
                     'MATS6m',
                     'MATS1e',
                     'MATS3e',
                     'MATS1s',
                     'MATS2s',
                     'MATS3s',
                     'MATS4s',
                     'MATS5s',
                     'MATS7s',
                     'GATS1c',
                     'GATS2c',
                     'GATS3c',
                     'GATS4c',
                     'GATS5c',
                     'GATS6c',
                     'GATS7c',
                     'GATS8c',
                     'GATS1m',
                     'GATS2m',
                     'GATS4m',
                     'GATS5m',
                     'GATS6m',
                     'GATS7m',
                     'GATS8m',
                     'GATS2v',
                     'GATS6v',
                     'GATS7v',
                     'GATS8v',
                     'GATS1e',
                     'GATS3e',
                     'GATS4e',
                     'GATS1p',
                     'GATS3p',
                     'GATS4p',
                     'GATS5p',
                     'GATS1i',
                     'GATS2i',
                     'GATS3i',
                     'GATS4i',
                     'GATS2s',
                     'GATS3s',
                     'GATS5s',
                     'GATS6s',
                     'GATS7s',
                     'GATS8s',
                     'SM1_DzZ',
                     'VE1_DzZ',
                     'VE3_DzZ',
                     'VR1_DzZ',
                     'VE1_Dzv',
                     'VR2_Dzv',
                     'VE2_Dze',
                     'SpMAD_Dzp',
                     'VE2_Dzp',
                     'SpMAD_Dzs',
                     'SM1_Dzs',
                     'VE1_Dzs',
                     'VR2_Dzs',
                     'nBase',
                     'BCUTw-1l',
                     'BCUTw-1h',
                     'BCUTc-1l',
                     'BCUTc-1h',
                     'BCUTp-1l',
                     'BCUTp-1h',
                     'nBondsD',
                     'nBondsD2',
                     'nBondsT',
                     'SpMax3_Bhm',
                     'SpMin1_Bhm',
                     'SpMin2_Bhm',
                     'SpMin4_Bhm',
                     'SpMin7_Bhm',
                     'SpMax1_Bhv',
                     'SpMax2_Bhe',
                     'SpMin8_Bhe',
                     'SpMax1_Bhs',
                     'SpMax3_Bhs',
                     'C2SP1',
                     'C1SP2',
                     'C2SP2',
                     'C3SP2',
                     'C1SP3',
                     'C2SP3',
                     'C3SP3',
                     'C4SP3',
                     'SCH-3',
                     'SCH-4',
                     'SCH-5',
                     'SCH-7',
                     'SC-4',
                     'SC-5',
                     'VC-3',
                     'SP-7',
                     'ASP-0',
                     'ASP-1',
                     'ASP-4',
                     'ASP-5',
                     'ASP-6',
                     'ASP-7',
                     'AVP-0',
                     'AVP-3',
                     'AVP-4',
                     'AVP-6',
                     'AVP-7',
                     'CrippenLogP',
                     'VE1_Dt',
                     'VE3_Dt',
                     'VR1_Dt',
                     'ECCEN',
                     'nwHBd',
                     'nHBint2',
                     'nHBint3',
                     'nHBint4',
                     'nHBint5',
                     'nHBint6',
                     'nHBint7',
                     'nHBint8',
                     'nHBint9',
                     'nHdNH',
                     'nHsSH',
                     'nHsNH2',
                     'nHssNH',
                     'nHaaNH',
                     'nHtCH',
                     'nHdCH2',
                     'nHdsCH',
                     'nHCsatu',
                     'nHAvin',
                     'nsCH3',
                     'nssCH2',
                     'nsssCH',
                     'naaaC',
                     'ndsN',
                     'naaN',
                     'nsssN',
                     'naasN',
                     'nssssNp',
                     'ndO',
                     'nssO',
                     'naaO',
                     'nsOm',
                     'ndS',
                     'naaS',
                     'ndssS',
                     'nddssS',
                     'SwHBa',
                     'SHBint10',
                     'SHsOH',
                     'SsssCH',
                     'SdssC',
                     'SaasC',
                     'SssssC',
                     'SssS',
                     'SsBr',
                     'SsI',
                     'minHBd',
                     'minHBa',
                     'minwHBa',
                     'minHBint2',
                     'minHBint3',
                     'minHBint4',
                     'minHBint5',
                     'minHBint6',
                     'minHBint7',
                     'minHBint8',
                     'minHBint9',
                     'minHBint10',
                     'minHsOH',
                     'minHsNH2',
                     'minHssNH',
                     'minHdsCH',
                     'minHaaCH',
                     'minHCsats',
                     'minHCsatu',
                     'minHother',
                     'minsCH3',
                     'minssCH2',
                     'minsssCH',
                     'minaasC',
                     'mintN',
                     'minsssN',
                     'minsOH',
                     'mindO',
                     'minssO',
                     'minsF',
                     'maxHBa',
                     'maxwHBa',
                     'maxHBint2',
                     'maxHBint3',
                     'maxHBint4',
                     'maxHBint5',
                     'maxHBint6',
                     'maxHBint7',
                     'maxHBint9',
                     'maxHBint10',
                     'maxHCsats',
                     'maxssCH2',
                     'maxsssCH',
                     'maxdssC',
                     'maxssssC',
                     'maxsI',
                     'hmax',
                     'hmin',
                     'ETA_AlphaP',
                     'ETA_dAlpha_A',
                     'ETA_dEpsilon_B',
                     'ETA_dEpsilon_D',
                     'ETA_dPsi_B',
                     'ETA_Shape_Y',
                     'ETA_BetaP_s',
                     'ETA_Beta_ns_d',
                     'ETA_EtaP_B',
                     'IC0',
                     'IC1',
                     'IC2',
                     'SIC1',
                     'SIC3',
                     'SIC5',
                     'BIC0',
                     'MIC5',
                     'ZMIC2',
                     'ZMIC5',
                     'Kier3',
                     'nAtomLC',
                     'nAtomP',
                     'nAtomLAC',
                     'MDEC-14',
                     'MDEC-22',
                     'MDEC-23',
                     'MDEC-33',
                     'MDEO-11',
                     'MDEO-12',
                     'MDEN-11',
                     'MDEN-12',
                     'MDEN-13',
                     'MDEN-22',
                     'MDEN-23',
                     'MDEN-33',
                     'MLFER_A',
                     'MLFER_BH',
                     'MLFER_S',
                     'piPC10',
                     'R_TpiPCTPC',
                     'PetitjeanNumber',
                     'n5Ring',
                     'n6Ring',
                     'n7Ring',
                     'n8Ring',
                     'n12Ring',
                     'nG12Ring',
                     'nFRing',
                     'nF4Ring',
                     'nF6Ring',
                     'nF7Ring',
                     'nF8Ring',
                     'nF9Ring',
                     'nF10Ring',
                     'nF11Ring',
                     'nF12Ring',
                     'nT7Ring',
                     'nHeteroRing',
                     'n3HeteroRing',
                     'n6HeteroRing',
                     'n8HeteroRing',
                     'nF6HeteroRing',
                     'nF10HeteroRing',
                     'RotBFrac',
                     'nRotBt',
                     'LipinskiFailures',
                     'topoRadius',
                     'JGI2',
                     'JGI3',
                     'JGI4',
                     'JGI5',
                     'JGI6',
                     'JGI7',
                     'JGI8',
                     'JGI9',
                     'JGI10',
                     'VE1_D',
                     'VE3_D',
                     'VR1_D',
                     'SRW9',
                     'TDB1u',
                     'TDB4u',
                     'TDB5u',
                     'TDB9u',
                     'TDB10u',
                     'TDB9m',
                     'TDB10m',
                     'TDB9v',
                     'TDB2i',
                     'TDB9s',
                     'TDB10s',
                     'PPSA-3',
                     'DPSA-1',
                     'FPSA-3',
                     'FNSA-3',
                     'RPCG',
                     'RNCG',
                     'RPCS',
                     'RNCS',
                     'THSA',
                     'LOBMAX',
                     'MOMI-Y',
                     'MOMI-XY',
                     'geomShape',
                     'RDF20u',
                     'RDF100u',
                     'RDF155u',
                     'RDF10m',
                     'RDF20m',
                     'RDF35m',
                     'RDF40m',
                     'RDF55m',
                     'RDF60m',
                     'RDF65m',
                     'RDF110m',
                     'RDF125m',
                     'RDF130m',
                     'RDF135m',
                     'RDF140m',
                     'RDF30p',
                     'RDF40s',
                     'RDF80s',
                     'RDF115s',
                     'RDF145s',
                     'L2u',
                     'L3u',
                     'P1u',
                     'E1u',
                     'E2u',
                     'E3u',
                     'Du',
                     'E1m',
                     'E2m',
                     'E3m',
                     'Dm',
                     'E1v',
                     'E2v',
                     'E3v',
                     'Dv']

    df = df[[col for col in df.columns.to_list() if col in selected_list]]

    return df


def scale_descriptors(df):
    """Scale input features using B3DB Standard Scaler.

    The b3db_scaler was fitted using the full B3DB dataset.
    """

    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, "./files/b3db_scaler.joblib")
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
        dirname, "./files/b3clf_{}_{}.joblib".format(clf_str, sampling_str))

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
