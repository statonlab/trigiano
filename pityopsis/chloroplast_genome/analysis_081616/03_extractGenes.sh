#!/bin/bash
# load necessary modules
module unload python/2.7.3
module load biopython
# run python script to extract fasta sequence for genes/proteins from genbank file in aster
./xDev_extractGenesGb.py --g Aster_NC_027434.gb --o Aster_NC_027434
