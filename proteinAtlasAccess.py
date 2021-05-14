# -*- coding: utf-8 -*-
"""
Created on Wed Feb 17 17:29:40 2021

Protein Atlas Access

@author: Carrie
"""
import requests
from bs4 import BeautifulSoup
import ContraceptiveConstants as cc
import time #for debugging
from datetime import datetime

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
    paResp = requests.get(paURL) #about 1.1 seconds
    
    #error responses
    status = paResp.status_code
    if status > 200: #equivalent to if not paResp.ok
        error_text = "status code: " + str(status)
        print(error_text)
        now = datetime.now()
        date_str = now.strftime("%Y-%m-%d_%H:%M:%S")
        with open("error_log.txt", "a") as f:
            f.write(date_str + ' ' + ensID + ' ' + error_text + '\n')
        #if it's 404, it's fine, for ex. ENSG00000166473
        if status != 404:
            #try for a bit to see if the server decides to behave
            retry = 10 #use small retry for unexpected errors
            if status in [502, 503, 504]: #server errors that will hopefully
            #resolve with enough attempts
                retry = 100
            for n in range(retry):
                print("re request attempt: " + str(n+1))
                paResp = requests.get(paURL)
                if paResp.ok:
                    print('successful request')
                    with open("error_log.txt", "a") as f:
                        f.write("resolved after " + str(n+1) + "retries"+'\n')
                    break
            
    
    #even if we break out of the loop and there's still an error, we can
    #proceed as normal, because it won't break anything later to do this, 
    #it'll just make 'na' everywhere (which is what we want from a 404)
    paXML = BeautifulSoup(paResp.content, 'lxml-xml', 
                                    from_encoding = 'utf-8')
    #about 0.4 seconds
    return paXML


def get_ovary_tags(paXML, ont_ID = cc.OVARY_ONT_ID):
    """
    gets the tissue tags for a given organ from the beautiful soup of a 
    protein atlas XML file, e.g.
    
    <tissue organ="Female tissues" ontologyTerms="UBERON:0000992">Ovary
                                                                    </tissue>
    Parameters
    ----------
    paXML : bs4.BeautifulSoup
        A beautiful soup of the xml content of the 
        response object received from proteinatlas.org.
        
    ont_ID : str
        the identifier used by the ontology terms tag for the tissue of
        interest in the paXML. Defaults to the tag for ovary

    Returns
    -------
    ovaryTissues : bs4.element.ResultSet
        
        the tags in the tree with ovary tissue tags
    """
    ovaryTissues = paXML.find_all(ontologyTerms=ont_ID)
    return ovaryTissues

def find_specific_siblings(tissueResults, sibName):
    """searches for all the siblings of the tags in tissueResults that have
    the name sibName, and returns a list of lists of each tag's siblings
    

    Parameters
    ----------
    tissueResults : bs4.element.ResultSet
        a set of tags from the XML file for a specific tissue
        
    sibName : str
        the name of the tags we're looking for in the siblings

    Returns
    -------
    allSiblings : list
        a list of lists of tags. Each inner list contains all matching 
        siblings for a tag in tissueResults

    """
    
    allSiblings = []
    for tag in tissueResults:
        prevL = tag.find_previous_siblings(sibName)
        nextL = tag.find_next_siblings(sibName)
        siblings = prevL + nextL
        if siblings != []:
            allSiblings.append(siblings) #this is a list of lists of tags
    
    return allSiblings
    
    
def get_RNA_tissue_data(paXML, tissueResults):
    """parses the protein xml file to retrieve tissue-specific 
    RNA expresssion data.    

    Parameters
    ----------
    paXML : bs4.BeautifulSoup
        A beautiful soup of the xml content of the 
        response object received from proteinatlas.org.
        
    tissueResults : bs4.element.ResultSet
        a set of tags from the XML file for a specific tissue

    Returns
    -------
    float : the normalized RNA Expression

    """
    normRNAExp = None
    allSiblings = find_specific_siblings(tissueResults, "level")
    
    for sibL in allSiblings: #for each list of tags
        if normRNAExp != None:
            break #RNA expression data should only exist once,
            #stop once we've found it
        for sib in sibL: #for each tag
            if sib['type'] == 'normalizedRNAExpression':
                normRNAExp = sib['expRNA']
                break
    if normRNAExp == None:
        print("no value was set for normRNAExp")
        return normRNAExp
    else:
        return float(normRNAExp)
     

def get_protein_exp_data(paXML, tissueResults, tissueTypes = cc.OVARY_TYPES):
    """parses the xml file for a target protein to retrieve protein 
    expression data from the provided tissue results. Defaults to ovary. 
    
    Ovarian tissue types:
        -cc.FOLLICLE : "Follicle cells"
        -cc.STROMA : "Ovarian stroma cells"

    Parameters
    ----------
    paXML : bs4.BeautifulSoup
        A beautiful soup of the xml content of the 
        response object received from proteinatlas.org.
        
    tissueResults : bs4.element.ResultSet
        a set of tags from the XML file for a specific tissue
        
    tissueTypes : list
        a list of strings used by the protein atlas to identify types of cells
        within an organ. Defaults to ovarian tissue. 

    Returns
    -------
    expDict : dict
        A dictionary containing the protein expression levels for each of 
        the selected tissue types
    """
    expDict = {}
    allSiblings = find_specific_siblings(tissueResults, "tissueCell")
    if allSiblings == []: #no protein expression data
        for tissue in tissueTypes:
            expDict[tissue] = cc.EXP_NA
    else:
        for tissue in tissueTypes:
            tissue_exp = cc.EXP_NA #if we don't find an expression value, 
            #it defaults to the value for "data not available"
            for sibList in allSiblings:
                #print(sibList)
                for s in sibList:
                    cellTag = s.find("cellType")
                    if cellTag.get_text() == tissue:
                        levelTag = cellTag.find_next_sibling("level")
                        if levelTag["type"] == "expression":
                            tissue_exp = levelTag.getText()
            expDict[tissue] = tissue_exp

    
    return expDict
    
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
    start = time.perf_counter()
    paXML = get_protein_xml(cc.TEST_FALSE_POS_ID)
    tissues = get_ovary_tags(paXML)
    
    exp_dict = get_protein_exp_data(paXML, tissues)
    stop = time.perf_counter()
    

    print(stop - start)
    
    return exp_dict
    
    
    
    
    
    
    
    
    
    