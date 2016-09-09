#!/bin/bash
# script to search for primerIDs in p3out.txt file
for f in `cat 01_primerPairGrep.txt`
do 
	grep -B1 -m1 "$f" discula70_53.scafSeq.p3out.txt | head -n1 | cut -f 2 -d '=' | sed 's/^scaff/>scaff/'; 
        grep -m1 "$f" discula70_53.scafSeq.p3out.txt | cut -f 2 -d '='
done > 03_primerIds_withSeq.fasta
