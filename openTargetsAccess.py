# -*- coding: utf-8 -*-
"""
Created on Thu Mar 11 11:08:32 2021

@author: Carrie
"""
from pprint import pprint
import requests
from bs4 import BeautifulSoup
import csv
import ContraceptiveConstants as cc


full_csv = "targets_associated_with_female_infertility.csv"
test_csv = "test_targets.csv"

def data_from_csv(csv_str):
    """
    reads a csv from Open Targets and collects the gene name, ensembl ID, and
    overall association score for each target. 
    
    Deprecated - only works on the CSV file from the older version of Open 
                 Targets

    Parameters
    ----------
    csv_str : str
        The name of the csv file from open targets

    Returns
    -------
    A list of dictionaries where each dictionary contains the gene symbol, 
    gene name, ensembl ID, and overall association score from Open Targets. 

    """
    outList = []
    
    with open(csv_str, newline = "", encoding = "utf-8") as csvfile:
        reader = csv.DictReader(csvfile)
        for target in reader:
            target_dict = {}
            target_dict[cc.GS_KEY] = target['\ufefftarget.gene_info.symbol']
            target_dict[cc.ENSID_KEY] = target['target.id']
            target_dict[cc.ASO_KEY] = target['association_score.overall']
            target_dict[cc.NAME_KEY] = target['target.gene_info.name']
            target_dict[cc.SOURCE_KEY] = cc.OT
            outList.append(target_dict)
    
    return outList


def test_run():
    return data_from_csv(test_csv)

#### having trouble with the open targets API

OT_search = "https://www.targetvalidation.org/disease/EFO_0008560/" + \
    "associations?fcts=zscore_expression_tissue:UBERON_0000992," + \
    "zscore_expression_level:1"

def get_OT_html(OT_url):
    OT_resp = requests.get(OT_url)
    OT_soup = BeautifulSoup(OT_resp.content, "lxml")
    return OT_resp


