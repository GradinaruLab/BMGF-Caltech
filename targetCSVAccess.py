# -*- coding: utf-8 -*-
"""
Created on Tue May 11 11:11:35 2021

@author: Carrie
"""

import requests, sys
import ContraceptiveConstants as cc
import pandas as pd

def get_ensID(symbol):
    """
    Requests the ensembl ID for a gene symbol and returns it. Uses the human
    gene data set

    Parameters
    ----------
    symbol : str
        a gene symbol

    Returns
    -------
    ensID : str
        the ensembl ID for the input symbol, in human format

    """
    server = "https://rest.ensembl.org"
    ext = "/xrefs/symbol/homo_sapiens/" + symbol + "?"
    r = requests.get(server+ext, headers={"Content-Type":"application/json"})
 
    if not r.ok:
      r.raise_for_status()
      sys.exit()
      
    j = r.json() #looks like [{'id': 'ENSG00000183770', 'type': 'gene'}]
    ensID = j[0]['id']
    return ensID

def prepare_df(csv, data_set):
    """
    makes a data frame from the a csv from open targets or CITDB,
    and renames the columns to be consistent between data sets, 
    where applicable. Also adds a column to indicate which data set 
    the data are from
    
    Parameters
    ----------
    csv : str
        the file name of the csv
        
    Returns
    -------
    df : dataFrame
        a data frame made from the csv, with updated column names
    """
    df = pd.read_csv(csv)
    #rename the first column to the constant name for gene symbol
    old_name = df.columns[0]
    df.rename(columns = {old_name : cc.GS_KEY}, inplace=True)
    
    #add a column indicating the data set for each entry
    vals = [True] * len(df)
    df[data_set] = vals
                             
    return df

def merge_OT_and_CITD(OT_csv, CITD_csv, out_csv):
    """
    merges the csv files from Open Targets and the Contraceptive Infertility
    Target Database. Adds columns to indicate which database a target 
    came from.

    Parameters
    ----------
    OT_csv : str
        the file name of the csv from Open Targets
    CITD_csv : str
        the file name of the csv from CITD
    out_csv : str
        the name of the file to write to (will be overwritten)

    Returns
    -------
    None.

    """
    OT_df = prepare_df(OT_csv, cc.OT)
    CITD_df = prepare_df(CITD_csv, cc.CITD)
    out_df = pd.merge(OT_df, CITD_df, on = cc.GS_KEY, how = 'outer')
    return out_df
    

def test_run():
    df = merge_OT_and_CITD(cc.TEST_CSV, cc.TEST_CITD_CSV, '')
    return df






    