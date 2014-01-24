#! /usr/bin/env python
from modeller import *
from modeller.automodel import *
import sys
import subprocess, shlex

USAGE = """
Created on Wed Jan 22 11:24:53 2014
@author: phillippe

Usage: phython homology_modeling.py file.fasta

Files pdball.pir or pdb_95.pir are needed for database search.
"""
DATABASE_TYPE = 'pdball.pir'

#def get_sequences():
#    #read from an input fasta file a protein sequence.
#    try:
#        Ifile = Seq.parse(sys.argv[1],'fasta', ProteinAlphabet())
#    except:
#        print usage

if len(sys.argv) < 2:
    print USAGE

def get_homologs():
    """
    search for homologs in the non-redundant (with 95% identity cutoff) PDB or
    the complete PDB on the DATABASE_TYPE variable.
    """
    
    log.verbose()
    env = environ()

    # Read in the database of PDB chains clustered at 95% sequence identity
    sdb = sequence_db(env)
    try:
        sdb.read(seq_database_file=DATABASE_TYPE, seq_database_format='PIR',
                 chains_list='ALL', minmax_db_seq_len=(30, 4000),
                 clean_sequences=True)
    except IOError:
        errmsg = str(sys.exc_info()[1]) + """
       Could not open the PDB 95 database or PDBALL. This database is *not* 
       included in the Modeller release, since it is frequently updated. 
       To run this, you first need to download pdb_95.pir.gz from the "Data 
       file downloads" page on the Modeller website.
    """
        print(errmsg)
        sys.exit(0)

    # Read in the target sequence in PIR alignment format
    aln = alignment(env)
    aln.append(file=sys.argv[1], alignment_format='PIR', align_codes='ALL')

    # Convert the target sequence from alignment to profile format
    prf = aln.to_profile()

    # Scan sequence database to pick up homologous sequences
    prf.build(sdb, matrix_offset=-450, rr_file='${LIB}/blosum62.sim.mat',
              gap_penalties_1d=(-500, -50), n_prof_iterations=1,
              check_profile=False, max_aln_evalue=0.01, gaps_in_target=True)

    # Write out the profile in text format
    prf.write(file='search_' + sys.argv[1].strip('.pir') + '_pdBall.prf',
              profile_format = 'TEXT')
    
    aln2 = prf.to_alignment()
    aln2.write(file = 'search_' + sys.argv[1].strip('.pir') + '_pdBall.pir', 
              alignment_format='PIR')
    aln2.write(file = 'search_' + sys.argv[1].strip('.pir') + '_pdBall.fasta', 
              alignment_format='FASTA')

def get_motifs():
    """
    search in the Pfam database for known motifs.
    The output isn't parsed though.
    """
#    data = os.system("curl -L -H 'Expect:' -H 'Accept:text/xml' -F hmmdb=pfam -F seq='<" + sys.argv[1] + "' http://hmmer.janelia.org/search/hmmscan")
#    print """This is the return from the program:
#        %s        
#        """ % (data)
#    type(data)

    args = shlex.split("curl -L -H 'Expect:' -H 'Accept:text/xml' -F hmmdb=pfam -F seq='<" + sys.argv[1] + "' http://hmmer.janelia.org/search/hmmscan")
    output = subprocess.check_output(args)
    o_file = open("Pfam_result_" + sys.argv[1].strip('.pir'), 'wb')   
    o_file.write(output)
    o_file.close()
#    subprocess.call(args, stdout=output)
    #print output
    

def do_model():

    pass

def do_assessment():
    pass

#get_homologs() this is my changed file
get_motifs()