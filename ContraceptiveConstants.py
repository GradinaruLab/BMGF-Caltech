# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 10:16:59 2021

@author: Carrie
"""

CSV_NAME ="targets_associated_with_female_infertility.csv"
TEST_CSV = "test_targets.csv"
#default name for the csv downloaded from opentargets
TEST_ID = "ENSG00000178394" #ID for the protein HTR1A
#this protein is expressed in the ovaries, with both protein and RNA evidence
TEST_NEG_ID = "ENSG00000173714" #WFIKKN2 which has no expression data in any
#ovarian tissue
TEST_PART_ID = "ENSG00000163093" #BBS5 which has expression data in stroma
#but not in follicles

#keys for the dictionaries in the list of targets
ENSID_KEY = "ensembl ID"
ASO_KEY = "association score overall"
GN_KEY = "gene name"
RNA_EXP_KEY = "normalized RNA expression"

#keys for tissue types

STROMA = "Ovarian stroma cells"
FOLLICLE = "Follicle cells"
OVARY_TYPES = [STROMA, FOLLICLE]

OVARY_ONT_ID = "UBERON:0000992"

#expression not available
EXP_NA = "na"