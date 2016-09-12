01_primerPairGrep.txt was copied from an excel spread sheet where a reverse complement of the Reverse primer was concatenated to

the Forward primer with a ".*" separating them. This list of search terms was used for 02_findPrimerIDs.sh

need to extract scaffolds from discula70_53.scafSeq based on the ids we already have
####script to search for primerIDs in p3out.txt file
```
for f in `cat 01_primerPairGrep.txt`
do 
	grep -B1 "$f" discula70_53.scafSeq.p3out.txt | head -n1 | cut -f 2 -d '='; 
        echo $f
done > 02_primerIds.txt
```
---
####script to search for primerIDs in p3out.txt file
```
for f in `cat 01_primerPairGrep.txt`
do 
	grep -B1 -m1 "$f" discula70_53.scafSeq.p3out.txt | head -n1 | cut -f 2 -d '=' | sed 's/^scaff/>scaff/'; 
        grep -m1 "$f" discula70_53.scafSeq.p3out.txt | cut -f 2 -d '='
done > 03_primerIds_withSeq.fasta
```
---
####create a list of those which need to be extracted
```
grep "^>" 03_primerIds_withSeqHandEdit.fasta | sed 's/^>//g' > 04_list.txt
./fasta_parse.py > 04_primerIds_withSeq.fasta
```
---
####script to findSSRs
```
ln -s ../../archive/discula70_53.scafSeq 
/lustre/projects/staton/software/makerP/exe/blast/bin/dustmasker \
-in discula70_53.scafSeq \
-out discula70_53.scafSeq.masked \
-outfmt fasta \
-level 1
perl findSSRs_post_assembly.pl \
-f discula70_53.scafSeq \
-m discula70_53.scafSeq.masked
```
---
