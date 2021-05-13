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
        returns None if no ensID available

    """
    server = "https://rest.ensembl.org"
    ext = "/xrefs/symbol/homo_sapiens/" + symbol + "?"
    r = requests.get(server+ext, headers={"Content-Type":"application/json"})
 
    if not r.ok:
      r.raise_for_status()
      sys.exit()
      
    j = r.json() #looks like [{'id': 'ENSG00000183770', 'type': 'gene'}]
    if j == []:
        return None
    else:
        ensID = j[0]['id']
        return ensID

def ensIDs_for_df(df, ens_col_name = cc.ENSID_KEY, symbol_col = cc.GS_KEY):
    """
    Adds a column of ensembl IDs to a dataframe of protein targets

    Parameters
    ----------
    df : dataframe
        A dataframe of protein targets
    ens_col_name : str
        the name of the column of ensembl IDs
    symbol_col : str
        the name of the column with gene symbols

    Returns
    -------
    out_df : dataframe
        A dataframe with ensIDs inserted

    """
    ensIDs = [None] * len(df) #should this be pandas' NaN?
    for i in range(len(df)):
        symbol = df[symbol_col][i]
        ensID = get_ensID(symbol)
        ensIDs[i] = ensID
        if ensID != None:
            print(symbol + ": " + ensID)
        else:
            print('no ensID found for ' + symbol)
    df.insert(1, ens_col_name, ensIDs)
    return df
        
        
    

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
    data_set : str
        the name of the data_set the csv is from
        
    Returns
    -------
    df : dataFrame
        a data frame made from the csv, with updated column names
    """
    df = pd.read_csv(csv, encoding = 'utf-8-sig')
    #rename the first column to the constant name for gene symbol
    old_name = df.columns[0]
    df.rename(columns = {old_name : cc.GS_KEY}, inplace=True)
    
    #add a column indicating the data set for each entry
    vals = [True] * len(df)
    df[data_set] = vals
                             
    return df

def merge_OT_and_CITD(OT_csv, CITD_csv):
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
    Returns
    -------
    out_df : dataframe
        the merged dataframe 

    """
    OT_df = prepare_df(OT_csv, cc.OT)
    CITD_df = prepare_df(CITD_csv, cc.CITD)
    out_df = pd.merge(OT_df, CITD_df, on = cc.GS_KEY, how = 'outer')
    return out_df
    
def csv_wrapper(OT_csv, CITD_csv, out_csv, ens_col_name = cc.ENSID_KEY, 
                symbol_col = cc.GS_KEY):
    """
    Parameters
    ----------
    OT_csv : str
        the file name of the csv from Open Targets
    CITD_csv : str
        the file name of the csv from CITD
    out_csv : str
        the name of the file to write to (will be overwritten)
    ens_col_name : str
        the name of the column of ensembl IDs
    symbol_col : str
        the name of the column with gene symbols

    Returns
    -------
    None.

    """
    df = merge_OT_and_CITD(OT_csv, CITD_csv)
    df = ensIDs_for_df(df, ens_col_name, symbol_col)
    df.to_csv(out_csv, encoding = "utf-8-sig")
    

def test_run():
    csv_wrapper(cc.TEST_CSV, cc.TEST_CITD_CSV, "test_merge_with_ensID.csv")
    #df = merge_OT_and_CITD(cc.TEST_CSV, cc.TEST_CITD_CSV)
    #df2 = ensIDs_for_df(df, 'ensID')
    #return df2






    