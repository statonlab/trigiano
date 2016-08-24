#!/bin/bash
# this script is a bit hacky and juggles output between tmp1 and tmp2 (I did this purely to avoid a lot of piping and keep the comments clean for github). In the end these tmp files are erased. This script makes specific edits to the 01_p_8-16.gff based on errors in annotation, start by removing orf188
grep -v "110446	111009" 01_p_8-16.gff > tmp1
# extend atpB from 49,873 to 49,870, note this step has to account for atpE's boundary at the same site 49,873
sed 's/49873	51351/49870	51351/g' tmp1 > tmp2
# extend atpE from 49,472 to 49,469, this gene had shared a boundary with the previous annotation of atpB
sed 's/49472	49873/49469	49873/g' tmp2 > tmp1
# extend rps8 from 75,541 to 75,538.
sed 's/75541/75538/g' tmp1 > tmp2
# extend psbC from 32,999 to 33,002.
sed 's/32999/33002/g' tmp2 > tmp1
# extend rpl36 from 74,964 to 74,961.
sed 's/74964/74961/g' tmp1 > tmp2
# extend psaA from 37,195 to 37,192.
sed 's/37195/37192/g' tmp2 > tmp1
# extend psbD from 30,630 to 31,633.
sed 's/31630/31633/g' tmp1 > tmp2
# extend ycf15 from 94,130 to 94,127.
sed 's/94130/94127/g' tmp2 > tmp1
# extend atpA from 28,164 to 28,170.
sed 's/28164/28170/g' tmp1 > tmp2
# extend rbcL from 53,404 to 53,437. This adds another ~11 codons however appears to be consistent with the Aster cp genome annotation althougth with some minor variations.
sed 's/53404/53437/g' tmp2 > tmp1
# extend psbE from 60,555 to 60,552
sed 's/60555/60552/g' tmp1 > tmp2
# extend ndhC from 47,122 to 47,119
sed 's/47122/47119/g' tmp2 > tmp1
# extend psaB from 34,965 to 34,962
sed 's/34965/34962/g' tmp1 > tmp2
# extend petD from 73,154 to 73,160. This annotation has an early stop... Missing CDS? 7 bp exon?
sed 's/73154/73160/g' tmp2 > tmp1
# extend rpoC1 from 17,692 to 17,693. This annotation has an early stop...
sed 's/17692/17693/g' tmp1 > tmp2
# extend rps16 from 4,671 to 4,669. This annotation has an early stop... Missing CDS? No exon?
sed 's/4671/4669/g' tmp2 > tmp1 
# extend psbZ from 33,832 to 33,835.
sed 's/33832/33835/g' tmp1 > tmp2
# extend rpl14 from 76,132 to 76,129.
sed 's/76132/76129/g' tmp2 > tmp1
# extend rps4 from 43,091 to 43,088.
sed 's/43091/43088/g' tmp1 > tmp2
# extend rpoC2 from 21,932 to 21,938.
sed 's/21932/21938/g' tmp2 > tmp1
# rpl32...Extend rpl32 from 118,305 to 118,254.
sed 's/118305/118254/g' tmp1 > tmp2
# rpl2 (off by a couple bases here and there)
sed 's/80663	81053/80661	81053/g' tmp2 > tmp1
sed 's/79558	79989/79558	79986/g' tmp1 > tmp2
# clpP (off by a couple bases here and there)
sed 's/66680	66975/66678	66968/g' tmp2 > tmp1
sed 's/65822	66050/65822	66049/g' tmp1 > tmp2
# petD (extra AA after stop codon)
sed 's/73160/73155/g' tmp2 > tmp1
# ycf3 (exon1 needs to be altered)
sed 's/40069	40221/40069	40194/g' tmp1 > tmp2
sed 's/40914	41162/40917	41162/g' tmp2 > tmp1
# rpoC1 fixed stop codong slight adjustment
sed 's/17693/17689/g' tmp1 > tmp2
# atpF fixed stop codon slight adjustment
sed 's/26163	26571/26162	26571/g' tmp2 > tmp1
# rpl16 fixed start codon slight adjustment
sed 's/76619	77029/76619	76978/g' tmp1 > tmp2
# rename file and cleanup
cat tmp2 > 07_p_8-16.gff
#cat tmp1 > 07_p_8-16.gff
rm -f tmp1 tmp2
