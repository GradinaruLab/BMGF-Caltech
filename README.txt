# -*- coding: utf-8 -*-
"""
Created on Wed Sep 15 16:25:16 2021

@author: Carrie
"""

This repository contains a script for processing data about potential 
contraceptive targets from Open Targets and CITDBase and retrieving 
RNA and protein expression information from the Human Protein Atlas.

The repository also contains input and output files from various runs of the 
script, as well as other related information for the project. 

This script was written as part of the Caltech BMGF Non-Hormonal Contraceptives
research group in the Gradinaru lab. 

The files for the script are currently top level in the repository. 
Most subfolders have a "contents" file with a brief description of the files
contained. The python files should have internal documentation (assuming past
me had their act together), but I plan to add an overview here eventually. 

----

To use this code:

--- Setup and Ensembl IDs ---

Start with a csv file of putative targets. This file will need at minimum a 
column containing gene symbols. 

Set the values in ContraceptiveConstants.py to match the header names of the 
columns in the csv. If you got the data from Open Targets or CITDB, it 
probably already matches. 

Use the file targetCSVAccess.py to get ensembl IDs for your data if you don't
have them already. This file will can also merge csvs from OT and CITDB.

If you have two csvs of targets, one from CITDB and one from OT, you can just
run the function 
         csv_wrapper(OT_csv, CITD_csv, out_csv, ens_col_name = cc.ENSID_KEY, 
                symbol_col = cc.GS_KEY)
with your input files and what you want the output to be named. 

If you only have one csv of targets, or it is from another source, you will 
need to write some code to convert your csv to a dataframe. Then run
  ensIDs_for_df(df, ens_col_name = cc.ENSID_KEY, symbol_col = cc.GS_KEY)
and save that data frame as a csv. 

Note that the file "openTargetsAccess.py" was written for a previous format
data export from that website and is no longer useful. 

--- Human Protein Atlas ---

Once you have a csv of targets with ensembl IDs, use 
ContraceptiveTargetScript.py to get ovary RNA expression in the ovary and
protein expression in the follicle and stroma cells from the Human Protein
Atlas.
    compare_targets(csv_str, ens_col = cc.ENSID_KEY)

Note that there is still some debug code printing to the console in this 
script because it was useful for me to have a visual indicator of progress
since the first run of the script on ~4000 targets took several hours
to complete. 

If you want to see the inner workings of compare_targets, look at the 
functions in "proteinAtlasAccess.py". 

--- Mouse Genome Informatics ---

Again start from a csv with a column of gene symbols. 

Run the function 
    MGI_ID_wrapper(in_csv, out_csv)
to generate a csv with putative mouse homologs for all of the input genes

Once you have a column of MGI IDs for mouse genes, run
  MGI_exp_wrapper(in_csv, MGI_col, out_csv)
to collect ovary tissue expression levels. 
