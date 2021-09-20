# -*- coding: utf-8 -*-
"""
Created on Fri Mar 12 10:16:59 2021

@author: Carrie
"""

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

MGI_EXP = 'GXDExpression.strength'

#Names for databases in the dictionaries
OT = "Open Targets"
CITD = "CITDBase"
MGI = "MGI_ID"

#expression not available
EXP_NA = "na"

#csv encoding
ENC = 'utf-8-sig'