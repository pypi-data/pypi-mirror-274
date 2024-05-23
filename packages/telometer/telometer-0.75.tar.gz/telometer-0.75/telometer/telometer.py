#!/usr/bin/env python3
# Telometer v0.75
# Created by: Santiago E Sanchez
# Artandi Lab, Stanford University, 2023
# Measures telomeres from ONT or PacBio long reads aligned to a T2T genome assembly
# Simple Usage: telometer -b sorted_t2t.bam -o output.tsv

import pysam
import re
import regex
import csv
import argparse
from multiprocessing import Pool, cpu_count

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

def process_read(args):
    read_data, telomere_repeats_re, adapters, minreadlen = args

    if read_data['is_unmapped'] or read_data['query_sequence'] is None or len(read_data['query_sequence']) < minreadlen:
        return None

    alignment_start = read_data['reference_start']
    alignment_end = read_data['reference_end']
    seq = read_data['query_sequence']

    if read_data['is_reverse']:
        direction = "rev"
        seq = reverse_complement(seq)
    else:
        direction = "fwd"

    reference_genome_length = read_data['reference_length']

    if alignment_start >= 15000 and alignment_start <= reference_genome_length - 30000:
        return None

    if alignment_start < 15000 and "q" not in read_data['reference_name']:
        arm = "p"
    else:
        arm = "q"

    telomere_start = [m.start() for m in re.finditer(telomere_repeats_re, seq)]
    if telomere_start:
        telomere_start = telomere_start[0]
        if telomere_start > 100 and (len(seq) - telomere_start > 200):
            return None

        telomere_end = min((seq.find(adapter) for adapter in adapters), default=-1)
        if telomere_end == -1:
            telomere_end = len(seq)

        telomere_region = seq[telomere_start:telomere_end]
        telomere_repeat = [m.group() for m in re.finditer('|'.join(telomere_repeats_re.split('|')), telomere_region)]
        telomere_length = len(''.join(telomere_repeat))

        boundary_mm1_length = find_initial_boundary_region(telomere_region, telomere_repeats_re.split('|'), max_mismatches=1)

        return {
            'chromosome': read_data['reference_name'],
            'reference_start': alignment_start,
            'reference_end': alignment_end,
            'telomere_length': telomere_length,
            'subtel_boundary_length': boundary_mm1_length,
            'read_id': read_data['query_name'],
            'mapping_quality': read_data['mapping_quality'],
            'read_length': len(seq),
            'arm': arm,
            'direction': direction
        }
    return None

def calculate_telomere_length():
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

    read_data_list = [{
        'query_name': read.query_name,
        'is_unmapped': read.is_unmapped,
        'is_reverse': read.is_reverse,
        'reference_start': read.reference_start,
        'reference_end': read.reference_end,
        'reference_name': read.reference_name,
        'mapping_quality': read.mapping_quality,
        'query_sequence': read.query_sequence,
        'reference_length': bam_file.get_reference_length(read.reference_name)
    } for read in bam_file]

    with Pool(processes=cpu_count()) as pool:
        results = pool.map(
            process_read,
            [(read_data, telomere_repeats_re, adapters, args.minreadlen) for read_data in read_data_list]
        )

    results = [result for result in results if result]

    # Ensure only the best result per read_id is saved
    best_results = {}
    for result in results:
        read_id = result['read_id']
        if read_id not in best_results:
            best_results[read_id] = result
        else:
            existing_result = best_results[read_id]
            if result['mapping_quality'] > existing_result['mapping_quality']:
                best_results[read_id] = result
            elif result['mapping_quality'] == existing_result['mapping_quality']:
                if result['telomere_length'] > existing_result['telomere_length']:
                    best_results[read_id] = result
                elif result['telomere_length'] == existing_result['telomere_length']:
                    # Arbitrarily keep the existing one if both telomere_length and mapping_quality are the same
                    pass

    final_results = list(best_results.values())

    if final_results:
        with open(args.output, 'w', newline='') as output_file:
            writer = csv.DictWriter(output_file, fieldnames=final_results[0].keys(), delimiter='\t')
            writer.writeheader()
            writer.writerows(final_results)

    print(f"Telometer completed successfully. Total telomeres measured: {len(final_results)}")

if __name__ == "__main__":
    calculate_telomere_length()
