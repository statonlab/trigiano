# script to findSSRs
ln -s ../../archive/discula70_53.scafSeq 

/lustre/projects/staton/software/makerP/exe/blast/bin/dustmasker \
-in discula70_53.scafSeq \
-out discula70_53.scafSeq.masked \
-outfmt fasta \
-level 1

perl findSSRs_post_assembly.pl \
-f discula70_53.scafSeq \
-m discula70_53.scafSeq.masked
