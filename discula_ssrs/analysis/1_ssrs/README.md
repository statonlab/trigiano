####script to search for primerIDs in p3out.txt file
```
for f in `cat 01_primerPairGrep.txt`
do 
	grep -B1 "$f" discula70_53.scafSeq.p3out.txt | head -n1 | cut -f 2 -d '='; 
        echo $f
done > 02_primerIds.txt
```
---
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
