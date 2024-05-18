
# NanoMethCluster


NanoMethCluster is a Python package designed for the analysis of nanopore sequencing example that includes methylation information. The package includes tools for analyzing BAM files, extracting methylation information, processing k-mer example, general example analysis, and plotting. It provides a command-line interface (CLI) for performing various analyses and creating interactive plots.
## Installation

You can install NanoMethCluster using `pip`:

```sh
pip install NanoMethCluster
```

Or from source:

```sh
git clone https://github.com/alekseizarubin/NanoMethCluster.git
cd NanoMethCluster
pip install .
```

## Usage

NanoMethCluster provides several command-line tools:

### BAMReadAnalyzer

Preparing input BAM files

```sh
dorado basecaller sup,5mCG_5hmCG --min-qscore 10 <pod5> > <bam>

dorado demux --kit-name <KIT> --output-dir <output_dir> <bam>
```

### BAMReadAnalyzer

Analyze BAM files to extract read information and save to a TSV file with additional metaexample.

```sh
NanoMethCluster BAMReadAnalyzer <bam_file> <output_file> [options]
```

**Options:**
- `-k, --kmer_length` (int): Length of k-mers to count (2 or 3). Set to 0 to disable counting. (default: 0)
- `--include_mlbc`: Include ML_B_C_Values in the output.
- `--total_ml`: Process ML_B_C_Values to sum paired values.
- `--meth_calc` (str): Method of calculation to use (default: base). Options are base or probability.
- `--num_simulations` (int): Number of simulations for probability calculation. (default: 1000)
- `--seed` (int): Seed for random number generator. (default: 42)
- `-t, --threads` (int): Number of threads for parallel processing. (default: 1)

### KmerDataProcessor

Process k-mer example from a TSV file.

```sh
NanoMethCluster KmerDataProcessor <input_file> <output_file> [options]
```

**Options:**
- `--min_length` (int): Minimum length threshold for filtering.
- `--min_quality` (float): Minimum quality threshold for filtering.
- `--norm` (str): Normalization method: n (none), c (complementary), r (reverse), or cr (complementary and reverse). (default: n)

### DataAnalyzer

Analyze example from TSV files and perform PCA, t-SNE, UMAP analyses, and K-means clustering.

```sh
NanoMethCluster DataAnalyzer <file_path> -o <output> [options]
```

**Options:**
- `-s, --sep` (str): Column separator for input file (default is tab). (default: 	)
- `--pca` (str): Perform PCA analysis with specified number of components or "auto" for default.
- `--tsne` (int): Perform t-SNE analysis with specified number of dimensions (default: 2). (default: 2)
- `--umap` (int): Perform UMAP analysis with specified number of dimensions (default: 2). (default: 2)
- `-k, --kmeans` (int): Perform K-means clustering and determine optimal number of clusters up to specified maximum.

### PlotGenerator

Generate interactive Plotly graphs from analysis results and create matrices.

```sh
NanoMethCluster PlotGenerator <input_dir> [options]
```

**Options:**
- `--pca` (int): PCA components to visualize (specify 2 or 3 components).
- `--tsne` (int): t-SNE components to visualize (specify 2 or 3 components).
- `--umap` (int): UMAP components to visualize (specify 2 or 3 components).
- `-k, --kmeans` (int): Number of clusters to use for coloring the plots.
- `--additional_file` (str): Additional TSV or TSV.GZ file with extra example.
- `--kraken` (str): Kraken2 TSV file with tab delimiter and no header, to use for additional coloring.
- `--matrix`: Flag to create matrices for k-means clusters and additional example or kraken example.

## Examples

### Example 1: Analyze a BAM file

```sh
NanoMethCluster BAMReadAnalyzer sample.bam output.tsv.gz -k 3 --include_mlbc --total_ml --meth_calc base --num_simulations 1000 --threads 4
```

This command analyzes the `sample.bam` file, counts 3-mers, includes ML_B_C values, processes them by summing paired values, uses base calculation method for methylation, performs 1000 simulations, and uses 4 threads for parallel processing.

### Example 2: Process k-mer example

```sh
NanoMethCluster KmerDataProcessor input.tsv.gz output.tsv.gz --min_length 1000 --min_quality 30.0 --norm cr
```

This command processes the k-mer example from `input.tsv.gz`, filters reads with a minimum length of 1000 and a minimum quality of 30.0, and normalizes k-mers by their complementary and reverse sequences.

### Example 3: Perform example analysis

```sh
NanoMethCluster DataAnalyzer example.tsv.gz -o results --pca auto --tsne 2 --umap 2 --kmeans 10
```

This command analyzes the `example.tsv.gz` file, performs PCA with an automatic number of components, performs t-SNE and UMAP analyses with 2 dimensions each, and determines the optimal number of clusters up to 10 for K-means clustering.

### Example 4: Generate interactive plots

```sh
NanoMethCluster PlotGenerator results --pca 0 1 --tsne 0 1 --umap 0 1 --kmeans 3 --additional_file additional_example.tsv.gz --kraken kraken.tsv --matrix
```

This command generates interactive Plotly plots from the analysis results in the `results` directory, visualizes the first two PCA components, the first two t-SNE components, and the first two UMAP components, colors the plots by 3 clusters, uses `additional_example.tsv.gz` for extra example, uses `kraken.tsv` for additional coloring, and creates matrices for k-means clusters and additional example.

## Data Directory

The `example` directory is included for storing any sample example or input files required for running the analyses. Ensure that the necessary example files are placed in this directory before running the commands.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

If you have any questions or suggestions, please open an issue or contact [Aleksei Zarubin] at [a.a.zarubin@gmail.com].
