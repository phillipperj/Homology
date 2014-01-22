#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 22 11:24:53 2014
@author: phillippe
All other scripts need to be in the same folder.

Usage: phython homology_modeling.py file.fasta 
"""
import sys
from Bio import SeqIO as Seq
from modeller import *
from modeller.automodel import *

def get_sequences():
    #read from an input fasta file a protein sequence.
    try:
        Ifile = Seq.parse(sys.argv[1],'fasta', alphabet)
    except:
        """ Usage: phython homology_modeling.py file.fasta 
        """
def get_motifs():
    #search in the Pfam database for known motifs.
    #The output isn't parsed though.
    pass

def get_homologs():
    #search for homologs in the non-redundant (with 95% identity cutoff) PDB.
    pass

def do_model():
    pass

def do_assessment():
    pass
