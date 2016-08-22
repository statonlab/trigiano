Aster_NC_027434.gb and Aster_NC_027434.CDS.fasta were acquired from http://www.ncbi.nlm.nih.gov/ on 19 August 2016.
####this script is intended to cleanup the gff file.
```
```
####first step removes ^M carriage returns
```
```
####second step removes the fasta entry from the end of the file
```
```
####third step removes non-standard ###			0 lines
```
```
####fourth step fixes a line missing the chromosome and info lines (first 2 columns)
```
sed 's/$//g' Pityopsis_annotation_8-16.gff |\
head -n584 |\
grep -v "^###.*0	$" |\
sed 's/^		/NC_007977.1	.	/g' > 01_p_8-16.gff
#sed 's/$//g' Pityopsis_annotation_8-16.gff |\
#head -n584 |\
#grep -v "^###.*0	$" |\
#sed 's/^		/NC_007977.1	.	/g' |\
#grep -v "Name=trn" |\
#grep -v "Name=orf" > 01_p_8-16_noTrn.gff
#sed 's/^M$//g' Pityopsis_annotation_8-16.gff |\
#grep -v "^###.*0	$" |\
#sed 's/^		/NC_007977.1	.	/g' > 01_p_8-16_keepFasta.gff
```
---
####load necessary modules
```
module unload python/2.7.3
module load biopython
```
####run python script to extract pertinent information from gff file
```
./xDev_extractAA.py --g 01_p_8-16.gff --f Pityopsis.fasta --o 02_p_8-16
```
---
####load necessary modules
```
module unload python/2.7.3
module load biopython
```
####run python script to extract fasta sequence for genes/proteins from genbank file in aster
```
./xDev_extractGenesGb.py --g Aster_NC_027434.gb --o Aster_NC_027434
```
---
####create blast DBs
```
```
####one for rRNAs and tRNAs
```
module load blast
makeblastdb \
-in Aster_NC_027434.r_t_RNA.fasta \
-dbtype nucl \
-title Aster_NC_027434.r_t_RNA \
-out Aster_NC_027434.r_t_RNA
```
####one for proteins
```
makeblastdb \
-in Aster_NC_027434.CDS2.fasta \
-dbtype 'prot' \
-title Aster_NC_027434.CDS \
-out Aster_NC_027434.CDS
```
---
####run BLAST nucleotides tRNAs + rRNAs
```
module load blast
echo "Pitiyopsis	Aster	% identity	alignment length	mismatches	gap opens	q. start	q. end	s. start	s. end  evalue	bit score"
blastn \
-query 02_p_8-16.ntd.fasta \
-db Aster_NC_027434.r_t_RNA \
-outfmt 6 \
-show_gis \
-max_target_seqs 1 \
-num_threads 30
```
####run BLAST proteins
```
echo "Pitiyopsis	Aster	% identity	alignment length	mismatches	gap opens	q. start	q. end	s. start	s. end  evalue	bit score"
blastp \
-query 02_p_8-16.aa.fasta \
-db Aster_NC_027434.CDS \
-outfmt 6 \
-show_gis \
-max_target_seqs 1 \
-num_threads 30
```
---
