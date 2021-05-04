# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 10:58:55 2021

@author: Carrie
"""
import proteinAtlasAccess as paa
import openTargetsAccess as ota
import ContraceptiveConstants as cc
from datetime import date
import csv



def compare_targets():
    """
    Given a csv from Open Targets, generates a list containing one dictionary
    for each target. The dictionary keys are provided in 
    ContraceptiveConstants.py. The information in the dictionary is:
        -the ensembl ID
        -the gene name
        -the overall association score from Open Targets
        -the RNA tissue data from the Human Protein Atlas

    Returns
    -------
    target_list : List
    
        A list of dictionaries containing the RNA tissue data from 
        the Human Protein Atlas; in addition the gene name, 
        ensembl ID, and overall association score from Open Targets

    """
    target_list = ota.data_from_csv(cc.CSV_NAME)
    #counter = 0 #debugging
    for target_dict in target_list:
        target_ID = target_dict[cc.ENSID_KEY]
        paResponse = paa.get_protein_xml(target_ID)
        norm_RNA_exp = paa.get_RNA_tissue_data(paResponse)
        target_dict[cc.RNA_EXP_KEY] = norm_RNA_exp
        #print(counter) #so I can see that it's actually running
        #print(target_dict[cc.GN_KEY])
        #counter += 1 #debugging
    return target_list

def write_target_csv(target_list):
    """
    Writes the list of target dictionaries to a csv file.
    
    Currently, the file is named "target_list_[today's date]"
    #TODO make this a parameter in constants

    Parameters
    ----------
    target_list : List
        The list of dictionaries provided by compare_targets

    Returns
    -------
    None.

    """
    today = date.today()
    today_str = today.strftime("%b-%d-%Y")
    out_csv_name = "target_list_" + today_str + ".csv"
    
    with open(out_csv_name, 'w', newline = '') as csv_file:
        fieldnames = [cc.GN_KEY, cc.ENSID_KEY, cc.ASO_KEY, cc.RNA_EXP_KEY]
        writer = csv.DictWriter(csv_file, fieldnames = fieldnames, \
                                dialect = 'excel')
        writer.writeheader()
        for target_dict in target_list:
            writer.writerow(target_dict)
            
    
def script_wrapper():
    """
    Wrapper function that runs the script. Generates the target list and
    writes it to a csv file. 

    Returns
    -------
    None.

    """
    target_list = compare_targets()
    write_target_csv(target_list)