#!/bin/bash
# this script is intended to cleanup the gff file. first step removes ^M carriage returns second step removes the fasta entry from the end of the file third step removes non-standard ###			0 lines fourth step fixes a line missing the chromosome and info lines (first 2 columns)
sed 's/$//g' Pityopsis_annotation_8-16.gff |\
head -n584 |\
grep -v "^###.*0	$" |\
sed 's/^		/NC_007977.1	.	/g' > 01_p_8-16.gff
