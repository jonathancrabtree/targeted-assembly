

# This script is supplementary to the pipeline and allows one to view some
# stats on the reference sequences that recruited no reads during Bowtie. 
# This will print a TSV for the reference ID, the sequence GC content in
# a percentage, and the gene name. 
#
# Run the script using a command like this:
# python3 global_alignment.py -ea_map /path/to/extract_alleles.out.tsv -ref_genome /path/to/ref_genome.fsa -ref_gff3 /path/to/ref.gff3 -out /path/to/alignment_out
#
# Author: James Matsumura

import argparse,os
from collections import defaultdict
from Bio import SeqIO

def main():

    parser = argparse.ArgumentParser(description='Script to generate EMBOSS Needle alignments given output from format_for_spades.py.')
    parser.add_argument('-ea_map', type=str, required=True, help='Path to map.tsv output from extract_alleles.py.')
    parser.add_argument('-ref_map', type=str, required=True, help='Path to *_ref_map.tsv output from analyze_bam.py.')
    parser.add_argument('-ref_genome', type=str, required=True, help='Path to the reference genome file used to build Bowtie2 index.')
    parser.add_argument('-ref_gff3', type=str, required=True, help='Path to the the reference GFF3 annotation.')
    parser.add_argument('-out', type=str, required=True, help='Path to output directory for all these alignments.')
    args = parser.parse_args()

    # First, extract the sequences from the reference file and 
    # *STORE IN MEMORY* (careful how big the reference genome used is.
    # We need this to generate small FASTA files for Needle alignment. 
    seq_dict = SeqIO.to_dict(SeqIO.parse(args.ref_genome,"fasta"))

    aligned = set()

    # Rebuild the DS created in extract_alleles.py. This is a dictionary 
    # where the key is the shared locus and the value is a list of all 
    # the mapped alleles. 
    ref_dict = defaultdict(list)
    with open(args.ea_map,'r') as loc_map:

        for line in loc_map:
            line = line.rstrip()
            ele = line.split('\t')
            locus = ele[0]

            for j in range(1,len(ele)):
                allele_info = ele[j].split('|')
                allele = allele_info[4]
                ref_dict[locus].append(allele)

    # Using the file that notes which loci recruited at least one read,
    # extract all those that did not recruit a read. 
    with open(args.ref_map,'r') as aligned_set:
        for line in aligned_set:
            line = line.rstrip()
            ele = line.split('\t')
            locus = ele[0]

            aligned.add(locus)

    seen = set() # some loci have multiple paths like ABC.1/ABC.2/etc.

    # At this point we know all the names of the reference sequences for a 
    # given locus ID and we know all the locus IDs that recruited at least 
    # one read. Now subset and find those locus IDs, and their respective 
    # alleles, that failed to recruit at least one ID. Write out stats
    # for each reference that wasn't able to recruit a read.
    with open(args.out,'w') as outfile:

        # Iterate over the complete set of references
        for k,v in ref_dict.items():
            if '.' in k: # if locus is split, grab generic name
                ele = k.split('.')
                k = ele[0]
            
            if k not in aligned:
                for ref in v:
                    gc = calc_gc_content(seq_dict[ref].seq)
                    outfile.write("{0}\t{1}\n".format(ref,gc))


# Function to calculate GC percentage given a sequence.
# Argument:
# seq = nucleotide sequence to be analyzed
def calc_gc_content(seq):
    bases = {"A":0,"T":0,"C":0,"G":0}
    for base in seq:
        bases[base] += 1

    gc_cont = (100*(bases["G"]+bases["C"])/(bases["A"]+bases["T"]+bases["G"]+bases["C"]))
    return float("{0:.2f}".format(gc_cont))


if __name__ == '__main__':
    main()
