# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 10:16:59 2021

@author: Carrie
"""

CSV_NAME ="targets_associated_with_female_infertility.csv"
#default name for the csv downloaded from opentargets
TEST_ID = "ENSG00000178394" #ID for the protein HTR1A
#this protein is expressed in the ovaries, with both protein and RNA evidence

#keys for the dictionaries in the list of targets
ENSID_KEY = "ensembl ID"
ASO_KEY = "association score overall"
GN_KEY = "gene name"
RNA_EXP_KEY = "normalized RNA expression"