import pysam
import pandas as pd
import argparse
from collections import Counter
import random
from concurrent.futures import ThreadPoolExecutor
from itertools import product
import gzip

read_counter = 0

def calculate_mean_quality(qualities):
    """Calculate the mean quality score of a sequence."""
    global read_counter
    read_counter += 1
    if read_counter % 1000 == 0:
        print(f"Processed {read_counter} reads")
    return sum(qualities) / len(qualities) if qualities else 0

def count_nucleotides(sequence):
    """Count the number of each nucleotide in a sequence."""
    counts = {'A': 0, 'T': 0, 'G': 0, 'C': 0}
    for nucleotide in sequence:
        if nucleotide in counts:
            counts[nucleotide] += 1
    return counts['A'], counts['T'], counts['G'], counts['C']

def get_mlbc_values(read):
    """Extract ML_B_C values from a read if present."""
    if read.has_tag('ML'):
        return read.get_tag('ML')
    return []

def process_mlbc_values(ml_values):
    """Process ML_B_C values by summing paired values."""
    half = len(ml_values) // 2
    first_half = ml_values[:half]
    second_half = ml_values[half:]
    return [first_half[i] + second_half[i] for i in range(half)]

def count_kmers(sequence, k):
    """Count the occurrences of each k-mer in a sequence."""
    kmers = [sequence[i:i+k] for i in range(len(sequence) - k + 1)]
    return Counter(kmers)

def generate_all_possible_kmers(k):
    """Generate all possible k-mers of a given length."""
    bases = 'ATGC'
    return [''.join(p) for p in product(bases, repeat=k)]

def meth_calc_base(ml_values, total_ml):
    """Calculate base methylation metrics."""
    if not ml_values:
        return 0, 0, 0
    
    num_values = len(ml_values)
    num_pairs = num_values // 2
    
    if total_ml:
        processed_values = process_mlbc_values(ml_values)
        C_h_m = processed_values
        C_n = [255 - value for value in C_h_m]
        count_greater_chm = sum(1 for chm, cn in zip(C_h_m, C_n) if chm > cn)
        return num_pairs, count_greater_chm, 0
    else:
        half = num_pairs
        C_h = ml_values[:half]
        C_m = ml_values[half:]
        C_n = [255 - ch - cm for ch, cm in zip(C_h, C_m)]
        count_max_ch = sum(1 for ch, cm, cn in zip(C_h, C_m, C_n) if ch > cm and ch > cn)
        count_max_cm = sum(1 for cm, ch, cn in zip(C_m, C_h, C_n) if cm > ch and cm > cn)
        return num_pairs, count_max_ch, count_max_cm

def simulate_event_occurrences(sequence, num_simulations):
    """Simulate event occurrences based on sequence probabilities."""
    if not sequence:
        return 0
    probabilities = [x / 256 for x in sequence]
    total_occurrences = 0
    for _ in range(num_simulations):
        occurrences = 0
        for p in probabilities:
            if random.random() < p:
                occurrences += 1
        total_occurrences += occurrences
    return total_occurrences / num_simulations

def meth_calc_probability(ml_values, total_ml, num_simulations):
    """Calculate methylation probabilities using simulations."""
    if not ml_values:
        return 0, 0

    if total_ml:
        processed_values = process_mlbc_values(ml_values)
        average_occurrences = simulate_event_occurrences(processed_values, num_simulations)
        return average_occurrences, 0
    else:
        half = len(ml_values) // 2
        C_h = ml_values[:half]
        C_m = ml_values[half:]
        average_occurrences_h = simulate_event_occurrences(C_h, num_simulations)
        average_occurrences_m = simulate_event_occurrences(C_m, num_simulations)
        return average_occurrences_h, average_occurrences_m

def process_read(read, k, include_mlbc, total_ml, meth_calc, num_simulations):
    """Process a single read and extract relevant information."""
    read_name = read.query_name
    read_length = read.query_length
    mean_quality = calculate_mean_quality(read.query_qualities)
    a_count, t_count, g_count, c_count = count_nucleotides(read.query_sequence)
    ml_values = get_mlbc_values(read)
    
    if include_mlbc:
        if total_ml:
            mlbc_values = ','.join(map(str, process_mlbc_values(ml_values)))
        else:
            mlbc_values = ','.join(map(str, ml_values))
    else:
        mlbc_values = '0'

    if meth_calc == 'base':
        num_pairs, count_max_ch, count_max_cm = meth_calc_base(ml_values, total_ml)
    elif meth_calc == 'probability':
        num_pairs = len(ml_values) // 2
        count_max_ch, count_max_cm = meth_calc_probability(ml_values, total_ml, num_simulations)

    kmer_count = count_kmers(read.query_sequence, k) if k > 0 else Counter()
    kmer_row = [kmer_count.get(kmer, 0) for kmer in all_kmers]

    row = [read_name, read_length, mean_quality, a_count, t_count, g_count, c_count, num_pairs]
    if include_mlbc:
        row.append(mlbc_values)
    if meth_calc == 'base' and total_ml:
        row.append(count_max_ch)  # Count_Max_Ch_m
    elif meth_calc == 'base':
        row.extend([count_max_ch, count_max_cm])
    elif meth_calc == 'probability' and total_ml:
        row.append(count_max_ch)  # Most likely methylation count for total_ml
    elif meth_calc == 'probability':
        row.extend([count_max_ch, count_max_cm])  # Most likely methylation counts for C_h and C_m

    row.extend(kmer_row)
    return row

def main(bam_file_path, output_file, k, include_mlbc, total_ml, meth_calc, num_simulations, seed, num_threads):
    """Main function to process BAM file and extract information."""
    random.seed(seed)
    bamfile = pysam.AlignmentFile(bam_file_path, "rb", check_sq=False)
    data = []
    global all_kmers
    all_kmers = generate_all_possible_kmers(k) if k > 0 else []

    with ThreadPoolExecutor(max_workers=num_threads) as executor:
        results = executor.map(lambda read: process_read(read, k, include_mlbc, total_ml, meth_calc, num_simulations), bamfile)
        data.extend(results)

    columns = ['Read_Name', 'Length', 'Mean_Quality', 'A', 'T', 'G', 'C', 'Num_Pairs']
    if include_mlbc:
        columns.append('ML_B_C_Values')
    if (meth_calc == 'base' or meth_calc == 'probability') and total_ml:
        columns.append('Count_Max_Ch_m')
    else:
        columns.extend(['Count_Max_Ch', 'Count_Max_Cm'])
    columns.extend(all_kmers)

    df = pd.DataFrame(data, columns=columns)

    if output_file.endswith('.gz'):
        with gzip.open(output_file, 'wt') as f:
            df.to_csv(f, sep='\t', index=False)
    else:
        with open(output_file, 'w') as f:
            df.to_csv(f, sep='\t', index=False)

    bamfile.close()

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process a BAM file to extract read information and save to a TSV file with additional metadata.')
    parser.add_argument('bam_file', type=str, help='Path to the BAM file to process.')
    parser.add_argument('output_file', type=str, help='Path to the output TSV file.')
    parser.add_argument('-k', '--kmer_length', type=int, default=0, help='Length of k-mers to count (2 or 3). Set to 0 to disable counting.')
    parser.add_argument('--include_mlbc', action='store_true', help='Include ML_B_C_Values in the output.')
    parser.add_argument('--total_ml', action='store_true', help='Process ML_B_C_Values to sum paired values.')
    parser.add_argument('--meth_calc', type=str, default='base', help='Method of calculation to use (default: base). Options are base or probability.')
    parser.add_argument('--num_simulations', type=int, default=1000, help='Number of simulations for probability calculation.')
    parser.add_argument('--seed', type=int, default=random.randint(0, 10000), help='Seed for random number generator.')
    parser.add_argument('-t', '--threads', type=int, default=1, help='Number of threads for parallel processing.')
    args = parser.parse_args()

    main(args.bam_file, args.output_file, args.kmer_length, args.include_mlbc, args.total_ml, args.meth_calc, args.num_simulations, args.seed, args.threads)
