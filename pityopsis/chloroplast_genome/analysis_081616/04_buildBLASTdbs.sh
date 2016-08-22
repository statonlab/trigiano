#!/bin/bash
# create blast DBs
# one for rRNAs and tRNAs
module load blast
makeblastdb \
-in Aster_NC_027434.r_t_RNA.fasta \
-dbtype nucl \
-title Aster_NC_027434.r_t_RNA \
-out Aster_NC_027434.r_t_RNA
# one for proteins
makeblastdb \
-in Aster_NC_027434.CDS2.fasta \
-dbtype 'prot' \
-title Aster_NC_027434.CDS \
-out Aster_NC_027434.CDS
