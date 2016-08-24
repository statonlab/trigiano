#!/bin/bash
# run BLAST nucleotides tRNAs + rRNAs
module load blast
echo "Pitiyopsis	Aster	% identity	alignment length	mismatches	gap opens	q. start	q. end	s. start	s. end	evalue	bit score"
blastn \
-query 02_p_8-16.ntd.fasta \
-db Aster_NC_027434.r_t_RNA \
-outfmt 6 \
-show_gis \
-max_target_seqs 1 \
-num_threads 30
# run BLAST proteins
echo "Pitiyopsis	Aster	% identity	alignment length	mismatches	gap opens	q. start	q. end	s. start	s. end	evalue	bit score"
blastp \
-query 02_p_8-16.aa.fasta \
-db Aster_NC_027434.CDS \
-outfmt 6 \
-show_gis \
-max_target_seqs 1 \
-num_threads 30
