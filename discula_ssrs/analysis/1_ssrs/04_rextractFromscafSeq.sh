#!/bin/bash
# create a list of those which need to be extracted
grep "^>" 03_primerIds_withSeqHandEdit.fasta | sed 's/^>//g' > 04_list.txt
./fasta_parse.py > 04_primerIds_withSeq.fasta
