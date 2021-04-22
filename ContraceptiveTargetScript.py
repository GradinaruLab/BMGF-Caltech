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
    target_list = ota.data_from_csv(cc.CSV_NAME)
    counter = 0
    for target_dict in target_list:
        target_ID = target_dict[cc.ENSID_KEY]
        paResponse = paa.get_protein_xml(target_ID)
        norm_RNA_exp = paa.get_RNA_tissue_data(paResponse)
        target_dict[cc.RNA_EXP_KEY] = norm_RNA_exp
        print(counter)
        print(target_dict[cc.GN_KEY])
        counter += 1
    return target_list

def write_target_csv(target_list):
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
    target_list = compare_targets()
    write_target_csv(target_list)