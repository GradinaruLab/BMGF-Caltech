# -*- coding: utf-8 -*-
"""
Created on Thu Sep 16 10:49:10 2021

@author: Carrie

Note: get_template() will break with 3.7 or higher
Use environment Caltech_BMGF_MGI which has 3.6 if you need get_template()
Not actually sure if older files will work in this environment...
Queries seem to work normally though with Caltech_BMGF on 3.8

http://www.ncbi.nlm.nih.gov/pubmed/26092688

"""
import pandas as pd
from intermine.webservice import Service



#test variables
test_csv = "mgi_test_input.csv"

gene_col = "gene symbol"

in_csv = "Top_200_OT.csv"
csv_df = pd.read_csv(in_csv, encoding = 'utf-8-sig')
out_csv = "Top_200_OT_with_MGI_ID_2021-09-16.csv"

def makeTargetStr(csv_df, col_name):
    """
    Generates a string of comma separated gene symbols from the column 
    col_name in the specified data frame from csvfile. 

    Parameters
    ----------
    csv_df : pandas.dataframe
        the name of the csv file with gene symbols
    col_name : str
        the name of the column containing the gene symbols

    Returns
    -------
    symStr : str
        The a string of comma separated gene symbols

    """
    symStr = ""
    
    for symbol in csv_df[col_name]:
        if symStr == "":
            symStr = symbol
        else:
            symStr = symStr + ", " + symbol
        
    return symStr


def makeMMHomQuery(symStr):
    """
    Given a string of comma separated human gene symbols, queries the MouseMine
    database for homologs in mouse. 

    Parameters
    ----------
    symStr : str
        a string of comma separated human gene symbols

    Returns
    -------
    query : intermine.query

    """
    service = Service("http://www.mousemine.org/mousemine/service")
    query = service.new_query("Gene")
    query.add_view(
        "primaryIdentifier", "symbol", "organism.name",
        "homologues.homologue.primaryIdentifier", "homologues.homologue.symbol",
        "homologues.homologue.organism.name", "homologues.type",
        "homologues.dataSets.name"
    )
    query.add_constraint("homologues.type", "NONE OF", 
                         ["horizontal gene transfer",
                            "least diverged horizontal gene transfer"], 
                         code = "B")
    query.add_constraint("Gene", "LOOKUP", symStr, "H. sapiens", 
                         code = "A")
    query.add_constraint("homologues.homologue.organism.name", "=", "Mus musculus",
                         code = "C")
    query.add_constraint("homologues.dataSets.name", "=", 
                         "Mouse/Human Orthologies from MGI",
                         code = "D")
    
    return query

def homologueDF(query, col_name, ID_name = "MGI_ID"):
    """
    

    Parameters
    ----------
    query : TYPE
        DESCRIPTION.

    Returns
    -------
    None.

    """
    hList = []
    symList = []
    for r in query.rows():
        symList.append(r["symbol"])
        hList.append(r["homologues.homologue.primaryIdentifier"])
    
    data = {col_name : symList, ID_name : hList}
    df = pd.DataFrame(data)
    return df

        
            
    
    
def printHomQuery(query):
    """
    Prints out useful information about a homologue query

    Parameters
    ----------
    query : intermine.query
        DESCRIPTION.

    Returns
    -------
    None.

    """
    for row in query.rows():
        print(row["primaryIdentifier"], row["symbol"], row["organism.name"], 
            row["homologues.homologue.primaryIdentifier"],
            row["homologues.homologue.symbol"],
            row["homologues.homologue.organism.name"], row["homologues.type"],
            row["homologues.dataSets.name"])

def wrapper():
    ss = makeTargetStr(csv_df, gene_col)
    hq = makeMMHomQuery(ss)
    #printHomQuery(hq)
    hdf = homologueDF(hq, gene_col)
    final_df = csv_df.merge(hdf, how="outer", on = gene_col)
    final_df.to_csv(out_csv, encoding = "utf-8-sig", index = False)
    
    return final_df
    
    
    
    
    
    
    
    

