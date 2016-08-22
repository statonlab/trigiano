#!/usr/bin/env python
# tested on python 2.7.11

import getopt, sys, re
import Bio

import pprint
from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq

import operator

def main():
    # command line parsing
    try:
        options, args = getopt.getopt(sys.argv[1:], "hfgo.v", ["help", "fasta=","gff=","output="])
    except getopt.GetoptError as err:
        # print help information and exit:
        print str(err)
        xDev_SNV_modules.usage()
        sys.exit(2)
    output = None
    verbose = False
    for opt, arg in options:
        if opt == "-v":
            verbose = True
        elif opt in ("-h", "--help"):
            xDev_SNV_modules.usage()
            sys.exit()
        elif opt in ("-f", "--fasta"):
            fasta = arg
        elif opt in ("-g", "--gff"):
            gff = arg
        elif opt in ("-o", "--output"):
            output = arg
        else:
            assert False, "unhandled option"

    # main
    # output files
    AA     = open(output + ".aa.fasta", 'w')
    NTD    = open(output + ".ntd.fasta", 'w')
    NONCAN = open(output + ".non_can.txt", 'w')
    ESTOP  = open(output + ".early_stop.txt", 'w')
    NOSTOP = open(output + ".no_stop.txt", 'w')
    TBL    = open(output + ".tbl", 'w')
    
    # global variables
    locusTag = 'AYK71'
    translationTable = 11
    dbName = 'WadlUT'
    idNum = 1
    tabs = '\t\t\t'

    # process fasta file
    in_seq_file = fasta
    in_seq_handle = open(in_seq_file)
    seq_dict = SeqIO.to_dict(SeqIO.parse(in_seq_handle, "fasta"))
    in_seq_handle.close()
    # this is how we will access our single fasta entry
    entry = ""
    for f in seq_dict:
        entry = f

    # open up a gff file
    in_file = gff
    in_handle = open(in_file)

    # process gff file
    name = ""
    spliced_dict = {}
    exons_dict   = {}
    orienta_dict = {}
    for line in in_handle:
        # ignore comment lines
        if line.startswith("##"):
            x = None
        # process records
        # each record starts with gene
        else:
            rec = line.rstrip().split()
            # if we see a gene line start a new entry
            if rec[2] == "gene":
                start = int(rec[3]) - 1
                stop  = int(rec[4])
                parseN = rec[9].split(";")
                parseM = parseN[0].split("=")
                name = parseM[1] + "_" + rec[3] + "_" + rec[4]
                spliced_dict[name] = Seq("")
                orienta_dict[name] = rec[6]
                exons_dict[name] = []
            # add exon to the entry
            elif rec[2] == "exon":
                # this is our spliced nucletoide sequence for our exons
                spliced_dict[name] = spliced_dict[name] + seq_dict[entry].seq[start:stop]
                # we need to keep track of exon boundaries for the output table, these get sorted
                exons_dict[name].append(rec[3] + "\t" + rec[4])
    in_handle.close()

    # handle printing first line of TBL
    outtbl = "Features\n"
    print >> TBL, outtbl

    for rec in spliced_dict:
        # protein coding gene?
        if rec.startswith(("trn"), 0):
            # output tRNA to ntd fasta file of non-coding genes
            header = ">" + rec + ", nucleotide len=" + str(len(spliced_dict[rec]))
            seq    = spliced_dict[rec]
            print >> NTD, header
            print >> NTD, seq
            # output rRNA to tbl for upload to ncbi
            ss = rec.split("_")
            # gene entry
            outtbl = str(ss[1]) + "\t" + str(ss[2]) + "\tgene"
            print >> TBL, outtbl
            outtbl = tabs + "gene\t" + ss[0]
            print >> TBL, outtbl
            outtbl = tabs + "locus_tag\t" + locusTag
            print >> TBL, outtbl
            # tRNA entry
            outtbl = str(ss[1]) + "\t" + str(ss[2]) + "\ttRNA"
            print >> TBL, outtbl
            outtbl = tabs + "gene\t" + ss[0]
            print >> TBL, outtbl
            outtbl = tabs + "locus_tag\t" + locusTag
            print >> TBL, outtbl
            outtbl = tabs + "product tRNA"
            print >> TBL, outtbl
        elif rec.startswith(("rrn"), 0):
            # output rRNA to ntd fasta file of non-coding genes
            header = ">" + rec + ", nucleotide len=" + str(len(spliced_dict[rec]))
            seq    = spliced_dict[rec]
            print >> NTD, header
            print >> NTD, seq
            # output rRNA to tbl for upload to ncbi
            ss = rec.split("_")
            # gene entry
            outtbl = str(ss[1]) + "\t" + str(ss[2]) + "\tgene"
            print >> TBL, outtbl
            outtbl = tabs + "gene\t" + ss[0]
            print >> TBL, outtbl
            outtbl = tabs + "locus_tag\t" + locusTag
            print >> TBL, outtbl
            # rRNA entry
            outtbl = str(ss[1]) + "\t" + str(ss[2]) + "\trRNA"
            print >> TBL, outtbl
            outtbl = tabs + "gene\t" + ss[0]
            print >> TBL, outtbl
            outtbl = tabs + "locus_tag\t" + locusTag
            print >> TBL, outtbl
            outtbl = tabs + "product 16S ribosomal RNA"
            print >> TBL, outtbl
        else:
            # print aa if negative, requires reverse_complement
            if orienta_dict[rec] == "-":
                rev = spliced_dict[rec].reverse_complement()
                aaseq = rev.translate()
                aaheader = ">" + rec + ", amino acid(-) len=" + str(len(aaseq))
                print >> AA, aaheader
                print >> AA, aaseq
                # output CDS to tbl for upload to ncbi
                ss = rec.split("_")
                # gene entry
                outtbl = str(ss[1]) + "\t" + str(ss[2]) + "\tgene"
                print >> TBL, outtbl
                outtbl = tabs + "gene\t" + ss[0]
                print >> TBL, outtbl
                outtbl = tabs + "locus_tag\t" + locusTag
                print >> TBL, outtbl
                # CDS entry
                # flag is so we know we are on the first itteration of this loop
                flag = 0
                for i in sorted(exons_dict[rec]):
                     if flag == 0:
                         print >> TBL, i + "\tCDS"
                         flag = 1
                     else:
                         print >> TBL, i
                outtbl = tabs + "gene\t" + ss[0]
                print >> TBL, outtbl
                outtbl = tabs + "locus_tag\t" + locusTag
                print >> TBL, outtbl
                outtbl = tabs + "codon_start\t1"
                print >> TBL, outtbl
                outtbl = tabs + "trasnl_table\t" + str(translationTable)
                print >> TBL, outtbl
                outtbl = tabs + "product\thypothetical protein"
                print >> TBL, outtbl
                outtbl = tabs + "protein_id\tgnl|" + dbName + "|" + locusTag + "_" + str(idNum)
                print >> TBL, outtbl
                outtbl = tabs + "transcript_id\tgnl|" + dbName + "|mrna." + locusTag + "_" + str(idNum)
                print >> TBL, outtbl
                idNum += 1
                outtbl = tabs + "translation\t" + aaseq
                print >> TBL, outtbl
                # check for early stop codon
                matches = re.search(r'[A-Z]\*[A-Z]', str(aaseq))
                if matches:
                    print >> ESTOP, rec
                else:
                    x = None
                # check for noncanoncial start site
                ntdseq = spliced_dict[rec].reverse_complement()
                if not ntdseq.startswith(("ATG", "GTG", "TTG"), 0):
                    print >> NONCAN, rec
                # check for missing stop codon
                if not ntdseq.endswith(("TAA", "TAG", "TGA"), 0):
                    print >> NOSTOP, rec
            # print aa if positive
            elif orienta_dict[rec] == "+":
                aaseq = spliced_dict[rec].translate()
                aaheader = ">" + rec + ", amino acid(+) len=" + str(len(aaseq))
                print >> AA, aaheader
                print >> AA, aaseq
                # output CDS to tbl for upload to ncbi
                ss = rec.split("_")
                # gene entry
                outtbl = str(ss[1]) + "\t" + str(ss[2]) + "\tgene"
                print >> TBL, outtbl
                outtbl = tabs + "gene\t" + ss[0]
                print >> TBL, outtbl
                outtbl = tabs + "locus_tag\t" + locusTag
                print >> TBL, outtbl
                # CDS entry
                # flag is so we know we are on the first itteration of this loop
                flag = 0
                for i in sorted(exons_dict[rec]):
                     if flag == 0:
                         print >> TBL, i + "\tCDS"
                         flag = 1
                     else:
                         print >> TBL, i
                outtbl = tabs + "gene\t" + ss[0]
                print >> TBL, outtbl
                outtbl = tabs + "locus_tag\t" + locusTag
                print >> TBL, outtbl
                outtbl = tabs + "codon_start\t1"
                print >> TBL, outtbl
                outtbl = tabs + "trasnl_table\t" + str(translationTable)
                print >> TBL, outtbl
                outtbl = tabs + "product\thypothetical protein"
                print >> TBL, outtbl
                outtbl = tabs + "protein_id\tgnl|" + dbName + "|" + locusTag + "_" + str(idNum)
                print >> TBL, outtbl
                outtbl = tabs + "transcript_id\tgnl|" + dbName + "|mrna." + locusTag + "_" + str(idNum)
                print >> TBL, outtbl
                idNum += 1
                outtbl = tabs + "translation\t" + aaseq
                print >> TBL, outtbl
                # check for early stop codon
                matches = re.search(r'[A-Z]\*[A-Z]', str(aaseq))
                if matches:
                    print >> ESTOP, rec
                else:
                    x = None
                # check for noncanoncial start site
                ntdseq = spliced_dict[rec]
                if not ntdseq.startswith(("ATG", "GTG", "TTG"), 0):
                    print >> NONCAN, rec
                # check for missing stop codon
                if not ntdseq.endswith(("TAA", "TAG", "TGA"), 0):
                    print >> NOSTOP, rec
            else:
                # we should never see this message
                print "fail", rec
                exit

if __name__ == "__main__":
    main()
