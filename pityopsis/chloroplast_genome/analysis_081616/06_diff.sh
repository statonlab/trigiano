#!/bin/bash
# find differences between blast outputs
cut -f 1,2 05_BLAST.tsv | sed 's/_.*,//g' | sed 's/gi|.*|//g' | grep -v "Aster" > data
diff <(awk '{print $1}' data) <(awk '{print $2}' data) > 06_differences.txt
rm -f data
