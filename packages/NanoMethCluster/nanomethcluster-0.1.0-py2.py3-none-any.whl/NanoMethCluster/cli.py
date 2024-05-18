import argparse
from NanoMethCluster import BAMReadAnalyzer_main, KmerDataProcessor_main, DataAnalyzer_main, PlotGenerator_main

def bamreadanalyzer(args):
    BAMReadAnalyzer_main(
        args.bam_file,
        args.output_file,
        args.kmer_length,
        args.include_mlbc,
        args.total_ml,
        args.meth_calc,
        args.num_simulations,
        args.seed,
        args.threads
    )

def kmerdataprocessor(args):
    KmerDataProcessor_main(
        args.input_file,
        args.output_file,
        args.min_length,
        args.min_quality,
        args.norm
    )

def dataanalyzer(args):
    DataAnalyzer_main(
        args.file_path,
        args.output,
        args.sep,
        args.pca,
        args.tsne,
        args.umap,
        args.kmeans
    )

def plotgenerator(args):
    PlotGenerator_main(
        args.input_dir,
        args.pca,
        args.tsne,
        args.umap,
        args.kmeans,
        args.additional_file,
        args.kraken,
        args.matrix
    )

def main():
    parser = argparse.ArgumentParser(description='NanoMethCluster Command Line Interface')
    subparsers = parser.add_subparsers(dest="command")

    # Subcommand для BAMReadAnalyzer
    parser_bam = subparsers.add_parser("BAMReadAnalyzer", help="Analyze BAM files")
    parser_bam.add_argument('bam_file', type=str, help='Path to the BAM file to process.')
    parser_bam.add_argument('output_file', type=str, help='Path to the output TSV file.')
    parser_bam.add_argument('-k', '--kmer_length', type=int, default=0, help='Length of k-mers to count (2 or 3). Set to 0 to disable counting.')
    parser_bam.add_argument('--include_mlbc', action='store_true', help='Include ML_B_C_Values in the output.')
    parser_bam.add_argument('--total_ml', action='store_true', help='Process ML_B_C_Values to sum paired values.')
    parser_bam.add_argument('--meth_calc', type=str, default='base', help='Method of calculation to use (default: base). Options are base or probability.')
    parser_bam.add_argument('--num_simulations', type=int, default=1000, help='Number of simulations for probability calculation.')
    parser_bam.add_argument('--seed', type=int, default=42, help='Seed for random number generator.')
    parser_bam.add_argument('-t', '--threads', type=int, default=1, help='Number of threads for parallel processing.')
    parser_bam.set_defaults(func=bamreadanalyzer)

    # Subcommand для KmerDataProcessor
    parser_kmer = subparsers.add_parser("KmerDataProcessor", help="Process k-mer data")
    parser_kmer.add_argument('input_file', type=str, help='Path to the input TSV file.')
    parser_kmer.add_argument('output_file', type=str, help='Path to the output TSV file.')
    parser_kmer.add_argument('--min_length', type=int, default=None, help='Minimum length threshold for filtering.')
    parser_kmer.add_argument('--min_quality', type=float, default=None, help='Minimum quality threshold for filtering.')
    parser_kmer.add_argument('--norm', type=str, default='n', choices=['n', 'c', 'r', 'cr'], help='Normalization method: n (none), c (complementary), r (reverse), or cr (complementary and reverse).')
    parser_kmer.set_defaults(func=kmerdataprocessor)

    # Subcommand для DataAnalyzer
    parser_data = subparsers.add_parser("DataAnalyzer", help="Analyze data from TSV files")
    parser_data.add_argument('file_path', type=str, help='Path to the TSV or TSV.GZ file')
    parser_data.add_argument('-o', '--output', type=str, required=True, help='Output directory for saving results')
    parser_data.add_argument('-s', '--sep', type=str, default='\t', help='Column separator for input file (default is tab)')
    parser_data.add_argument('--pca', type=str, nargs='?', const='auto', default=None, help='Perform PCA analysis with specified number of components or "auto" for default')
    parser_data.add_argument('--tsne', type=int, nargs='?', const=2, default=None, help='Perform t-SNE analysis with specified number of dimensions (default 2)')
    parser_data.add_argument('--umap', type=int, nargs='?', const=2, default=None, help='Perform UMAP analysis with specified number of dimensions (default 2)')
    parser_data.add_argument('-k', '--kmeans', type=int, nargs='?', const=10, default=None, help='Perform K-means clustering and determine optimal number of clusters up to specified maximum')
    parser_data.set_defaults(func=dataanalyzer)

    # Subcommand для PlotGenerator
    parser_plot = subparsers.add_parser("PlotGenerator", help="Generate interactive Plotly graphs from analysis results")
    parser_plot.add_argument('input_dir', type=str, help='Directory containing analysis result files')
    parser_plot.add_argument('--pca', type=int, nargs='+', help='PCA components to visualize (specify 2 or 3 components)')
    parser_plot.add_argument('--tsne', type=int, nargs='+', help='t-SNE components to visualize (specify 2 or 3 components)')
    parser_plot.add_argument('--umap', type=int, nargs='+', help='UMAP components to visualize (specify 2 or 3 components)')
    parser_plot.add_argument('-k', '--kmeans', type=int, help='Number of clusters to use for coloring the plots')
    parser_plot.add_argument('--additional_file', type=str, help='Additional TSV or TSV.GZ file with extra data')
    parser_plot.add_argument('--kraken', type=str, help='Kraken2 TSV file with tab delimiter and no header, to use for additional coloring')
    parser_plot.add_argument('--matrix', action='store_true', help='Flag to create matrices for k-means clusters and additional data or kraken data')
    parser_plot.set_defaults(func=plotgenerator)

    args = parser.parse_args()
    if hasattr(args, 'func'):
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
