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
import time



def compare_targets(csv_str):
    """
    Given a csv from Open Targets, generates a list containing one dictionary
    for each target. The dictionary keys are provided in 
    ContraceptiveConstants.py. The information in the dictionary is:
        -the ensembl ID
        -the gene name
        -the overall association score from Open Targets
        -the RNA tissue data from the Human Protein Atlas
        -the protein tissue data from the Human Protein Atlas
        
    Parameters
    ----------
    csv_str : str
    
        a string that is the name of the csv file of targets. Currently only
        csvs from Open Targets are supported. 

    Returns
    -------
    target_list : List
    
        A list of dictionaries containing the RNA and protein tissue data 
        from the Human Protein Atlas; in addition the gene name, 
        ensembl ID, and overall association score from Open Targets

    """
    counter = 0 #so I can see that it's working
    target_list = ota.data_from_csv(csv_str)
    for target_dict in target_list:
        #Setup
        target_ID = target_dict[cc.ENSID_KEY]
        paXML = paa.get_protein_xml(target_ID)
        ovaryTissues = paa.get_ovary_tags(paXML)
        #RNA Expression
        norm_RNA_exp = paa.get_RNA_tissue_data(paXML, ovaryTissues)
        target_dict[cc.RNA_EXP_KEY] = norm_RNA_exp
        #Protein Expression
        protein_dict = paa.get_protein_exp_data(paXML, ovaryTissues)
        target_dict.update(protein_dict) #adds all entries in protein_dict
        #debug
        print(counter)
        counter += 1
        print(target_dict[cc.GS_KEY])
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
    fieldnames = list(target_list[0].keys())
    
    with open(out_csv_name, 'w', newline = '') as csv_file:
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
    start = time.perf_counter() #timing
    
    target_list = compare_targets(cc.CSV_NAME)
    write_target_csv(target_list)
    
    stop = time.perf_counter()
    print("time for full run on open targets csv:")
    print(stop - start)
    
def test_run():
    target_list = compare_targets("missing_targets_from_May-05-2021.csv")
    write_target_csv(target_list)
    return target_list
    
    
    
    
    
    