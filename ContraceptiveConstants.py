# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 10:16:59 2021

@author: Carrie
"""
TEST_CSV = "merged_test.csv" 
CSV_NAME = "merged_OT_and_CITD_targets.csv"
#default name for the csv downloaded from opentargets
OLD_OT_CSV = "targets_associated_with_female_infertility.csv"
OT_CSV_NAME = "EFO_0008560-associated-diseases.csv" #the updated version
#CITDBase
TEST_CITD_CSV = "CITDBase_test.csv"
CITD_CSV_NAME = "CITDBase-Target-Search.csv"

TEST_ID = "ENSG00000178394" #ID for the protein HTR1A
#this protein is expressed in the ovaries, with both protein and RNA evidence
TEST_NEG_ID = "ENSG00000173714" #WFIKKN2 which has no expression data in any
#ovarian tissue
TEST_PART_ID = "ENSG00000163093" #BBS5 which has expression data in stroma
#but not in follicles
TEST_FALSE_POS_ID = "ENSG00000110888" #CAPRIN2 which has a high staining
#expression, but not detected actual expression, expert annotated staining
#as off-target binding.


#keys for the dictionaries in the list of targets
ENSID_KEY = "ensembl ID"
ASO_KEY = "association score overall"
GS_KEY = "gene symbol"
RNA_EXP_KEY = "normalized RNA expression"
NAME_KEY = "gene name"
SOURCE_KEY = "target source"

#keys for tissue types

STROMA = "Ovarian stroma cells"
FOLLICLE = "Follicle cells"
OVARY_TYPES = [STROMA, FOLLICLE]

OVARY_ONT_ID = "UBERON:0000992"

#Names for databases in the dictionaries
OT = "Open Targets"
CITD = "CITDBase"

#expression not available
EXP_NA = "na"