# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 17:29:40 2021

Protein Atlas Access

@author: Carrie
"""
import requests
from bs4 import BeautifulSoup
import ContraceptiveConstants as cc

test_ID = "ENSG00000178394" #ID for the protein HTR1A
#this protein is expressed in the ovaries, with both protein and RNA evidence

def get_protein_xml(ensID):
    """ Retrieves the XML file for a protein from the Protein Atlas
    
    Parameters
    ----------
    ensID : str
        an ensembl gene ID

    Returns
    -------
    paXML : bs4.BeautifulSoup
        the XML file from the Protein Atlas for the gene of interest in the
        for of a Response object. 
    """
    #step 1, use ensID to generate the protein atlas URL
    #https://www.proteinatlas.org/ENSG00000178394.xml
    paURL = "https://www.proteinatlas.org/" + ensID + ".xml"
    #print(paURL)
    paResp = requests.get(paURL)
    paXML = BeautifulSoup(paResp.content, 'lxml-xml', 
                                    from_encoding = 'utf-8')
    #print(paResp.content)
    #paSoup = BeautifulSoup(paResp.content, 'lxml-xml', from_encoding = 'utf-8')
    #pretty = paSoup.prettify()
    #print(pretty[:1000])
    return paXML


def get_RNA_tissue_data(paXML):
    """parses the protein xml file to retrieve ovary-specific 
    RNA expresssion data.
    
    Currently this function is written to only work for ovarian tissue.
    Once I have a better idea what I need, I might expand it to work for
    generic tissue types (and therefor take another argument)

    Parameters
    ----------
    paResponse : bs4.BeautifulSoup
        A beautiful soup of the xml content of the 
        response object received from proteinatlas.org.

    Returns
    -------
    float : the normalized RNA Expression

    """
    #<tissue organ="Female tissues" ontologyTerms="UBERON:0000992">
    #Ovary</tissue>
    normRNAExp = None
    
    ovaryTissues = paXML.find_all(ontologyTerms="UBERON:0000992")
    #finds all the tissue tags with the ontologyTerms attribute for ovary
    allSiblings = []
    for tag in ovaryTissues:
        prevL = tag.find_previous_siblings("level")
        nextL = tag.find_next_siblings("level")
        #siblings with a <level> tag will have expression level data
        siblings = prevL + nextL
        allSiblings.append(siblings) #this is a list of lists of tags
        #print(siblings)
        
    for sibL in allSiblings: #for each list of tags
        for sib in sibL: #for each tag
            if sib['type'] == 'normalizedRNAExpression':
                normRNAExp = sib['expRNA']
    if normRNAExp == None:
        print("no value was set for normRNAExp")
        return normRNAExp
    else:
        return float(normRNAExp)
    #In [147]: allSiblings[3][0]['type']
    #Out[147]: 'normalizedRNAExpression'    

# I think I need to find the tissue tag for ovary, then look at its siblings
# bs has sibling search functionality. Can find all "ontologyTerms" tags
# that have ontologyTerms="UBERON:0000992" then check through siblings
# to find <level type="normalizedRNAExpression" unitRNA="NX" expRNA="10.4">
# for example

def get_protein_exp_data(paXML):
    """
    parses the xml file for a target protein to retrieve protein expression
    data from ovarian tissues. 
    
    Ovarian tissue types:
        -Follicle cells
        -Ovarian stroma cells
        -#TODO

    Parameters
    ----------
    paXML : bs4.BeautifulSoup
        
        A beautiful soup of the xml content of the 
        response object received from proteinatlas.org.

    Returns
    -------
    expDict : dict
    
        A dictionary containing the protein expression levels for each of 
        the selected tissue types
        
    """
    #### PLAN ####
    
    # dictionary for levels
    # what are dictionary keys? names of specific ovarian tissue
    #    put in constants
    # search tags as in RNA expression
    # how to do this efficiently? want to look for all tissue types in one 
    #    search through the tree if possible
    # some trees won't have various tissue types
    #    give those a value of "na" - maybe make this a constant?
    #    "na" is different from "not detected" which is a provided value

def test_run():
    paR = get_protein_xml(test_ID)
    paS = get_RNA_tissue_data(paR)
    #tissueList = paS.find_all(has_tissue_and_ont)
    #tissueList = paS.find_all(ontologyTerms="UBERON:0000992")
    #print(tissueList[0])
    #return tissueList

    #for t in tissueList:
        #print(t)
        #if t["ontologyTerms"] == "UBERON:0000992":
            #print(t)
    #print(tag)
    #print(tag["ontologyTerms"])
    #found = paS.find_all(organ="Female tissues")
    #if len(found) == 0:
    #    print("nothing found")
    #else:
    #    for i in range(min(10, len(found))):
    #        print(found[i].prettify())

    return paS
    
    
    
    
    
    
    
    
    