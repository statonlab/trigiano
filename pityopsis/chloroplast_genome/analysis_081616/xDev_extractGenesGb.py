#!/usr/bin/env python
# tested on python 2.7.11

import getopt, sys
import Bio

from Bio import SeqIO

def main():
    # command line parsing
    try:
        options, args = getopt.getopt(sys.argv[1:], "hgo.v", ["help", "gb=","output="])
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
        elif opt in ("-g", "--gb"):
            gb = arg
        elif opt in ("-o", "--output"):
            output = arg
        else:
            assert False, "unhandled option"

    # main
    # output files
    tRNA   = open(output + ".tRNA.fasta", 'w')
    rRNA   = open(output + ".rRNA.fasta", 'w')
    CDS    = open(output + ".CDS2.fasta", 'w')
    CDSnt  = open(output + ".CDSnt.fasta", 'w')

    # open genbank file
    gbank = SeqIO.parse(gb, 'genbank')

    for genome in gbank:
        for gene in genome.features:
            if(gene.type == "tRNA"):
                start = gene.location.start.position
                end   = gene.location.end.position
                if 'db_xref' in gene.qualifiers:
                    des = str(gene.qualifiers['gene'])
                    des = des.split("'")[1]
                    gi = []
                    gi = str(gene.qualifiers['db_xref'])
                    gi = gi.split(":")[1]
                    gi = gi.split("'")[0]
                    if gene.strand == 1:
                        print >> tRNA, ">gi|%s|%s\n%s" % (gi,des,genome.seq[start:end])
                    elif gene.strand == -1:
                         print >> tRNA, ">gi|%s|%s\n%s" % (gi,des,genome.seq[start:end].reverse_complement())
            if(gene.type == "rRNA"):
                start = gene.location.start.position
                end   = gene.location.end.position
                if 'db_xref' in gene.qualifiers:
                    des = str(gene.qualifiers['gene'])
                    des = des.split("'")[1]
                    gi = []
                    gi = str(gene.qualifiers['db_xref'])
                    gi = gi.split(":")[1]
                    gi = gi.split("'")[0]
                    if gene.strand == 1:
                        print >> rRNA, ">gi|%s|%s\n%s" % (gi,des,genome.seq[start:end])
                    elif gene.strand == -1:
                         print >> rRNA, ">gi|%s|%s\n%s" % (gi,des,genome.seq[start:end].reverse_complement())
            if(gene.type == "CDS"):
                start = gene.location.start.position
                end   = gene.location.end.position
                if 'db_xref' in gene.qualifiers:
                    des = str(gene.qualifiers['gene'])
                    des = des.split("'")[1]
                    gi = []
                    gi = str(gene.qualifiers['db_xref'])
                    gi = gi.split(":")[1]
                    gi = gi.split("'")[0]
                    if gene.strand == 1:
                        print >> CDS, ">gi|%s|%s\n%s" % (gi,des,genome.seq[start:end].translate())
                        print >> CDSnt, ">gi|%s|%s\n%s" % (gi,des,genome.seq[start:end])
                    elif gene.strand == -1:
                        print >> CDS, ">gi|%s|%s\n%s" % (gi,des,genome.seq[start:end].reverse_complement().translate())
                        print >> CDS, ">gi|%s|%s\n%s" % (gi,des,genome.seq[start:end].reverse_complement())

if __name__ == "__main__":
    main()
