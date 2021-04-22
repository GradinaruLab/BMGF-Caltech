# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 17:29:40 2021

Protein Atlas Access

@author: Carrie
"""
import requests
from bs4 import BeautifulSoup

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
    paResp : requests.models.Response
        the XML file from the Protein Atlas for the gene of interest in the
        for of a Response object. 
    """
    #step 1, use ensID to generate the protein atlas URL
    #https://www.proteinatlas.org/ENSG00000178394.xml
    paURL = "https://www.proteinatlas.org/" + ensID + ".xml"
    print(paURL)
    paResp = requests.get(paURL)
    #print(paResp.content)
    #paSoup = BeautifulSoup(paResp.content, 'lxml-xml', from_encoding = 'utf-8')
    #pretty = paSoup.prettify()
    #print(pretty[:1000])
    return paResp


def get_RNA_tissue_data(paResponse):
    """parses the protein xml file to retrieve ovary-specific 
    RNA expresssion data.
    
    Currently this function is written to only work for ovarian tissue.
    Once I have a better idea what I need, I might expand it to work for
    generic tissue types (and therefor take another argument)

    Parameters
    ----------
    paResponse : requests.models.Response
        The response object received from proteinatlas.org.
        Contains the atlas' xml file for a target protein. 

    Returns
    -------
    float : the normalized RNA Expression

    """
    #<tissue organ="Female tissues" ontologyTerms="UBERON:0000992">
    #Ovary</tissue>
    normRNAExp = None
    paSoup = BeautifulSoup(paResponse.content, 'lxml-xml', 
                                    from_encoding = 'utf-8')
    ovaryTissues = paSoup.find_all(ontologyTerms="UBERON:0000992")
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
    return float(normRNAExp)
    #In [147]: allSiblings[3][0]['type']
    #Out[147]: 'normalizedRNAExpression'    

# I think I need to find the tissue tag for ovary, then look at its siblings
# bs has sibling search functionality. Can find all "ontologyTerms" tags
# that have ontologyTerms="UBERON:0000992" then check through siblings
# to find <level type="normalizedRNAExpression" unitRNA="NX" expRNA="10.4">
# for example

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
    
    
    
    
    
    
    
    
    