#!/bin/bash
# load necessary modules
module unload python/2.7.3
module load biopython
# run python script to extract pertinent information from gff file
./xDev_extractAA.py --g 07_p_8-16.gff --f Pityopsis.fasta --o 08_p_8-16
