# -*- coding: utf-8 -*-
"""
Created on Sun Sep 23 20:13:08 2012

@author: orient
"""

import urllib.request, urllib.parse, urllib.error
import re
import string
import os
from rdkit import Chem

Version=1.0

def ReadMolFromFile(self,filename=""):
    """
    #################################################################
    Read a molecule by SDF or MOL file format.
        
    Usage:
            
        res=ReadMolFromFile(filename)
            
        Input: filename is a file name.
            
        Output: res is a molecule object.
    #################################################################
    """
    mol=Chem.MolFromMolFile(filename)
    return mol
    
    
def ReadMolFromSmile(smi=""):
    """
    #################################################################
    Read a molecule by SMILES string.
        
    Usage:
            
        res=ReadMolFromSmile(smi)
            
        Input: smi is a SMILES string.
            
        Output: res is a molecule object.
    #################################################################
    """
    mol = Chem.MolFromSmiles(string.strip(smi))
        
    return mol
        
        
def ReadMolFromInchi(inchi=""):
    """
    #################################################################
    Read a molecule by Inchi string.
        
    Usage:
            
        res=ReadMolFromInchi(inchi)
            
        Input: inchi is a InChi string.
            
        Output: res is a molecule object.
    #################################################################
    """
    import pybel
    temp=pybel.readstring("inchi",inchi)
    smi=temp.write("smi")
    mol = Chem.MolFromSmiles(string.strip(smi))
        
    return mol
 
       
def ReadMolFromMol(filename=""):
    """
    #################################################################
    Read a molecule with mol file format.
        
    Usage:
            
        res=ReadMolFromMol(filename)
            
        Input: filename is a file name.
            
        Output: res is a molecule object.
    #################################################################
    """
    mol=Chem.MolFromMolFile(filename)
    return mol
    
    
def ReadMol(molstructure,molformat='smi'):
    """
    Read a molcule with the given format.

    Usage:
            
        res=ReadMol(filename)
            
        Input: molstructure is a molecular structure.
              
               molformat is a molecular format such as smile, inchi etc.
            
        Output: res is a molecule object.
    """
    import pybel
    mol=pybel.readstring(molformat,molstructure)
    
    return mol

#############################################################################

def GetMolFromCAS(casid=""):
    """
    Downloading the molecules from http://www.chemnet.com/cas/ by CAS ID (casid).
    if you want to use this function, you must be install pybel.
    """
    import pybel
    casid=string.strip(casid)
    localfile=urllib.request.urlopen('http://www.chemnet.com/cas/supplier.cgi?terms='+casid+'&l=&exact=dict')
    temp=localfile.readlines()
    for i in temp:
        if re.findall('InChI=',i)==['InChI=']:
            k=i.split('    <td align="left">')
            kk=k[1].split('</td>\r\n')
            if kk[0][0:5]=="InChI":
                res=kk[0]    
            else:
                res="None"
    localfile.close()
    mol=pybel.readstring('inchi',string.strip(res))
    smile=mol.write('smi')
    return string.strip(smile)


def GetMolFromEBI():
    """
    """
    pass


def GetMolFromNCBI(cid=""):
    """
    Downloading the molecules from http://pubchem.ncbi.nlm.nih.gov/ by cid (cid).
    """
    cid=string.strip(cid)
    localfile=urllib.request.urlopen('http://pubchem.ncbi.nlm.nih.gov/summary/summary.cgi?cid='+cid+'&disopt=SaveSDF')
    temp=localfile.readlines()   
    f=file("temp.sdf",'w')
    f.writelines(temp)
    f.close()
    localfile.close()
    m=Chem.MolFromMolFile("temp.sdf")
    os.remove("temp.sdf")
    temp=Chem.MolToSmiles(m,isomericSmiles=True)
    return temp


def GetMolFromDrugbank(dbid=""):
    """
    Downloading the molecules from http://www.drugbank.ca/ by dbid (dbid).
    """
    dbid=string.strip(dbid)
    
    localfile=urllib.request.urlopen('http://www.drugbank.ca/drugs/'+dbid+'.sdf')
    temp=localfile.readlines()   
    f=file("temp.sdf",'w')
    f.writelines(temp)
    f.close()
    localfile.close()
    m=Chem.MolFromMolFile("temp.sdf")
    os.remove("temp.sdf")
    temp=Chem.MolToSmiles(m,isomericSmiles=True)
    return temp



def GetMolFromKegg(kid=""):
    """
    Downloading the molecules from http://www.genome.jp/ by kegg id (kid).
    """
    ID=str(kid)
    localfile=urllib.request.urlopen('http://www.genome.jp/dbget-bin/www_bget?-f+m+drug+'+ID)
    temp=localfile.readlines() 
    f=file("temp.mol",'w')
    f.writelines(temp)
    f.close()
    localfile.close()
    m=Chem.MolFromMolFile("temp.mol")
    os.remove("temp.mol")
    temp=Chem.MolToSmiles(m,isomericSmiles=True)
    return temp
#############################################################################

if __name__=="__main__":
    
    print("Downloading......")
    temp=GetMolFromCAS(casid="50-12-4")
    print(temp)
    temp=GetMolFromNCBI(cid="2244")
    print(temp) 
    temp=GetMolFromDrugbank(dbid="DB00133")
    print(temp)
    temp=GetMolFromKegg(kid="D02176")
    print(temp)

