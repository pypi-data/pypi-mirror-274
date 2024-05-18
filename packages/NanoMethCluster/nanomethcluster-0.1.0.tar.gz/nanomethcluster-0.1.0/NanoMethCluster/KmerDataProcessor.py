import pandas as pd
import argparse

def reverse_complement(seq):
    """Return the reverse complement of a DNA sequence."""
    complement = {'A': 'T', 'T': 'A', 'G': 'C', 'C': 'G'}
    return ''.join(complement[base] for base in reversed(seq))

def reverse(seq):
    """Return the reverse of a DNA sequence."""
    return seq[::-1]

def normalize_kmers(data, kmer_start_col, norm):
    """Normalize k-mer columns in the dataframe based on the specified normalization method."""
    if norm not in ('c', 'r', 'cr') or kmer_start_col is None:
        return data

    kmer_columns = data.columns[kmer_start_col:].tolist()
    processed_kmers = set()

    for kmer in kmer_columns:
        if kmer in processed_kmers:
            continue

        alt_kmers = []
        if norm == 'c':
            alt_kmers = [reverse_complement(kmer)]
        elif norm == 'r':
            alt_kmers = [reverse(kmer)]
        elif norm == 'cr':
            alt_kmers = [reverse_complement(kmer), reverse(kmer), reverse(reverse_complement(kmer))]

        for alt_kmer in alt_kmers:
            if alt_kmer in data.columns and alt_kmer != kmer:
                data[kmer] += data[alt_kmer]
                data.drop(columns=[alt_kmer], inplace=True)
                processed_kmers.add(alt_kmer)

        processed_kmers.add(kmer)

    return data

def process_file(input_file, output_file, min_length, min_quality, norm):
    """Process the input file,
    removing the ML_B_C_Values column if it exists, performing necessary calculations,
    filtering based on Length and Mean_Quality, and normalizing k-mer columns if specified."""

    # Read the data from the 9th line onwards
    data = pd.read_csv(input_file, sep='\t')

    # Drop the ML_B_C_Values column if it exists
    if 'ML_B_C_Values' in data.columns:
        data.drop(columns=['ML_B_C_Values'], inplace=True)

    # Apply length and quality filters if specified
    if min_length is not None:
        data = data[data['Length'] >= min_length]
    if min_quality is not None:
        data = data[data['Mean_Quality'] >= min_quality]

    # Divide nucleotide columns by Length
    nucleotide_columns = ['A', 'T', 'G', 'C']
    for col in nucleotide_columns:
        if col in data.columns:
            data[col] = data[col] / data['Length']

    # Divide count columns by Num_Pairs
    count_columns = ['Count_Max_Ch', 'Count_Max_Cm', 'Count_Max_Ch_m']
    for col in count_columns:
        if col in data.columns:
            data[col] = data[col] / data['Num_Pairs']

    # Identify k-mer columns and divide them by Length
    kmer_start_col = None
    if 'Count_Max_Ch_m' in data.columns:
        kmer_start_col = data.columns.get_loc('Count_Max_Ch_m') + 1
    elif 'Count_Max_Cm' in data.columns:
        kmer_start_col = data.columns.get_loc('Count_Max_Cm') + 1

    if kmer_start_col is not None:
        kmer_columns = data.columns[kmer_start_col:]
        for kmer in kmer_columns:
            data[kmer] = data[kmer] / data['Length']

    # Normalize k-mer columns if specified
    data = normalize_kmers(data, kmer_start_col, norm)

    # Drop Length, Mean_Quality, and Num_Pairs columns
    data.drop(columns=['Length', 'Mean_Quality', 'Num_Pairs'], inplace=True)

    # Write the processed data to the output file
    data.to_csv(output_file, sep='\t', index=False)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Process the input file by skipping the first 8 lines, removing the ML_B_C_Values column if it exists, performing necessary calculations, filtering based on Length and Mean_Quality, and normalizing k-mer columns if specified.')
    parser.add_argument('input_file', type=str, help='Path to the input TSV file.')
    parser.add_argument('output_file', type=str, help='Path to the output TSV file.')
    parser.add_argument('--min_length', type=int, default=None, help='Minimum length threshold for filtering.')
    parser.add_argument('--min_quality', type=float, default=None, help='Minimum quality threshold for filtering.')
    parser.add_argument('--norm', type=str, default='n', choices=['n', 'c', 'r', 'cr'], help='Normalization method: n (none), c (complementary), r (reverse), or cr (complementary and reverse).')
    args = parser.parse_args()

    process_file(args.input_file, args.output_file, args.min_length, args.min_quality, args.norm)
