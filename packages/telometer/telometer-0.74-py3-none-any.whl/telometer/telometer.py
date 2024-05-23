#!/usr/bin/env python3
# Telometer v0.74
# Created by: Santiago E Sanchez
# Artandi Lab, Stanford University, 2023
# Measures telomeres from ONT or PacBio long reads aligned to a T2T genome assembly
# Simple Usage: telometer -b sorted_t2t.bam -o output.tsv

import pysam
import re
import regex
import csv
import argparse
import pandas as pd

def reverse_complement(seq):
    """Returns the reverse complement of a DNA sequence."""
    complement = {'A': 'T', 'C': 'G', 'G': 'C', 'T': 'A', 'N': 'N'}
    return "".join(complement[base] for base in reversed(seq))

def get_adapters(chemistry):
    """Returns the adapter sequences based on the sequencing chemistry."""
    if chemistry == 'r10':
        adapters = ['TTTTTTTTCCTGTACTTCGTTCAGTTACGTATTGCT', 'GCAATACGTAACTGAACGAAGTACAGG']
    else:
        adapters = ['TTTTTTTTTTTAATGTACTTCGTTCAGTTACGTATTGCT', 'GCAATACGTAACTGAACGAAGT']

    adapters_rc = [reverse_complement(adapter) for adapter in adapters]
    return adapters + adapters_rc

def get_telomere_repeats():
    """Returns the telomere repeat sequences."""
    telomere_repeats = ['GGCCA', 'CCCTAA', 'TTAGGG', 'CCCTGG', 'CTTCTT', 'TTAAAA', 'CCTGG']
    telomere_repeats_rc = [reverse_complement(repeat) for repeat in telomere_repeats]
    return telomere_repeats + telomere_repeats_rc

def find_initial_boundary_region(sequence, patterns, max_mismatches):
    """Finds the initial boundary region with allowed mismatches."""
    boundary_length = 0
    combined_pattern = '|'.join(f'({pattern})' for pattern in patterns)
    regex_pattern = f'({combined_pattern}){{2,}}'

    for match in regex.finditer(f'({regex_pattern}){{e<={max_mismatches}}}', sequence, regex.BESTMATCH):
        boundary_length = max(boundary_length, len(match.group(0)))
    return boundary_length

def extend_boundary_region(sequence, start, end, patterns, window_size, mismatch_threshold):
    """Extends the boundary region around the initial match, allowing some mismatches."""
    extended_start = max(0, start - window_size)
    extended_end = min(len(sequence), end + window_size)
    extended_seq = sequence[extended_start:extended_end]

    combined_pattern = ''.join(patterns)
    mismatches = sum(1 for base in extended_seq if base not in combined_pattern)

    if mismatches / len(extended_seq) <= mismatch_threshold:
        return len(extended_seq) - (end - start)  # Additional length
    return 0

def calculate_telomere_length():
    # required inputs: bam_file_path, output_file_path, chemistry
    parser = argparse.ArgumentParser(description='Calculate telomere length from a BAM file.')
    parser.add_argument('-b', '--bam', help='The path to the sorted BAM file.', required=True)
    parser.add_argument('-o', '--output', help='The path to the output file.', required=True)
    parser.add_argument('-c', '--chemistry', default="r10", help="Sequencing chemistry (r9 or r10, default=r10). Optional", required=False)
    parser.add_argument('-m', '--minreadlen', default=1000, type=int, help='Minimum read length to consider (Default: 1000 for telomere capture, use 4000 for WGS). Optional', required=False)
    args = parser.parse_args()
    bam_file = pysam.AlignmentFile(args.bam, "rb")

    adapters = get_adapters(args.chemistry)
    telomere_repeats = get_telomere_repeats()
    telomere_repeats_re = "|".join(f'({repeat}){{2,}}' for repeat in telomere_repeats)

    highest_mapping_quality = {}
    results = []
    p_count = 0
    q_count = 0
    rev_count = 0
    fwd_count = 0
    p_tel = 0
    q_tel = 0

    for read in bam_file:
        if read.is_unmapped or read.query_sequence is None or len(read.query_sequence) < args.minreadlen:
            continue

        alignment_start = read.reference_start
        alignment_end = read.reference_end
        seq = read.query_sequence

        if read.is_reverse:
            rev_count += 1
            direction = "rev"
            seq = reverse_complement(seq)
        else:
            fwd_count += 1
            direction = "fwd"

        reference_genome_length = bam_file.get_reference_length(read.reference_name)

        if alignment_start < 15000 or alignment_start > reference_genome_length - 30000:
            if alignment_start < 15000 and "q" not in read.reference_name:
                arm = "p"
                p_count += 1
            else:
                arm = "q"
                q_count += 1

            telomere_start = [m.start() for m in re.finditer(telomere_repeats_re, seq)]
            if telomere_start:
                telomere_start = telomere_start[0]
                if telomere_start > 100 and (len(seq) - telomere_start > 200):
                    continue

                telomere_end = min((seq.find(adapter) for adapter in adapters), default=-1)
                if telomere_end == -1:
                    telomere_end = len(seq)

                telomere_region = seq[telomere_start:telomere_end]
                telomere_repeat = [m.group() for m in re.finditer('|'.join(telomere_repeats), telomere_region)]
                telomere_length = len(''.join(telomere_repeat))

                boundary_mm1_length = find_initial_boundary_region(telomere_region, telomere_repeats, max_mismatches=1)

                if telomere_length < boundary_mm1_length:
                    telomere_length = boundary_mm1_length
                if telomere_length < boundary_mm2_length:
                    telomere_length = boundary_mm2_length

                if read.query_name not in highest_mapping_quality or read.mapping_quality > highest_mapping_quality[read.query_name]:
                    if arm == "p":
                        p_tel += 1
                    else:
                        q_tel += 1
                    highest_mapping_quality[read.query_name] = read.mapping_quality
                    results.append({
                        'chromosome': read.reference_name,
                        'reference_start': alignment_start,
                        'reference_end': alignment_end,
                        'telomere_length': telomere_length,
                        'subtel_boundary_length': boundary_mm1_length,
                        'read_id': read.query_name,
                        'mapping_quality': read.mapping_quality,
                        'read_length': len(seq),
                        'arm': arm,
                        'direction': direction
                    })

    bam_file.close()

    with open(args.output, 'w', newline='') as output_file:
        writer = csv.DictWriter(output_file, fieldnames=results[0].keys(), delimiter='\t')
        writer.writeheader()
        writer.writerows(results)

    # Print the total number of telomeres measured
    print(f"Telometer completed successfully. Total telomeres measured: {len(results)}")

if __name__ == "__main__":
    calculate_telomere_length()
