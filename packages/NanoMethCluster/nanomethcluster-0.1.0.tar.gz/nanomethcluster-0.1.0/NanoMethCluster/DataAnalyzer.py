import os
import pandas as pd
import argparse
import gzip
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from sklearn.decomposition import PCA
from sklearn.manifold import TSNE
import umap
import numpy as np
from sklearn.cluster import KMeans

def read_tsv(file_path, output_dir, sep='\t'):
    """
    Reads a TSV or TSV.GZ file in chunks, calculates basic statistics, and saves them.

    Args:
        file_path (str): Path to the input file.
        output_dir (str): Directory to save the results.
        sep (str, optional): Column separator (default is tab).
    """
    try:
        compression = 'gzip' if file_path.endswith('.gz') else None
        chunk_size = 10000  # Adjust chunk size for memory management
        chunks = pd.read_csv(file_path, sep=sep, compression=compression, chunksize=chunk_size)

        total_rows = 0
        total_cols = 0

        for chunk in chunks:
            total_rows += chunk.shape[0]
            total_cols = chunk.shape[1]

        print(f'Number of rows: {total_rows}')
        print(f'Number of columns: {total_cols}')

        output_file = os.path.join(output_dir, f'{os.path.basename(file_path).split(".")[0]}_counts.tsv.gz')
        with gzip.open(output_file, 'wt') as f:
            f.write(f'Number of rows:\t{total_rows}\n')
            f.write(f'Number of columns:\t{total_cols}\n')

    except Exception as e:
        print(f"Error reading the file: {e}")

def pca_analysis(file_path, output_dir, n_components):
    try:
        compression = 'gzip' if file_path.endswith('.gz') else None
        data = pd.read_csv(file_path, sep='\t', compression=compression)
        data.fillna(0, inplace=True)
        features = data.iloc[:, 1:]

        if n_components == 'auto':
            n_components = max(1, (features.shape[1] - 1) // 3)
        else:
            n_components = int(n_components)

        pca = PCA(n_components=n_components)
        principal_components = pca.fit_transform(features.values)

        print('PCA Analysis completed.')
        print('Explained variance ratio:', pca.explained_variance_ratio_)

        output_pca_file = os.path.join(output_dir, f'{os.path.basename(file_path).split(".")[0]}_pca_results.tsv.gz')
        output_variance_file = os.path.join(output_dir, f'{os.path.basename(file_path).split(".")[0]}_explained_variance.tsv.gz')
        
        pd.DataFrame(principal_components).to_csv(output_pca_file, sep='\t', index=False, compression='gzip')
        with gzip.open(output_variance_file, 'wt') as f:
            f.write('Component\tExplained Variance Ratio\n')
            for i, ratio in enumerate(pca.explained_variance_ratio_):
                f.write(f'{i+1}\t{ratio}\n')

        return principal_components

    except Exception as e:
        print(f"Error performing PCA: {e}")

def tsne_analysis(pca_result, output_dir, n_components):
    try:
        tsne = TSNE(n_components=n_components)
        tsne_result = tsne.fit_transform(pca_result)

        output_tsne_file = os.path.join(output_dir, f'{os.path.basename(output_dir)}_tsne_results.tsv.gz')
        pd.DataFrame(tsne_result).to_csv(output_tsne_file, sep='\t', index=False, compression='gzip')

        print('t-SNE Analysis completed.')

    except Exception as e:
        print(f"Error performing t-SNE: {e}")

def umap_analysis(pca_result, output_dir, n_components):
    try:
        umap_model = umap.UMAP(n_components=n_components)
        umap_result = umap_model.fit_transform(pca_result)

        output_umap_file = os.path.join(output_dir, f'{os.path.basename(output_dir)}_umap_results.tsv.gz')
        pd.DataFrame(umap_result).to_csv(output_umap_file, sep='\t', index=False, compression='gzip')

        print('UMAP Analysis completed.')

    except Exception as e:
        print(f"Error performing UMAP: {e}")

def kmeans_clustering(features, output_dir, max_clusters):
    """
    Performs K-means clustering on the input features and determines the optimal number of clusters using the elbow method.

    Args:
        features (pandas.DataFrame): The input features for clustering.
        output_dir (str): Directory to save the results.
        max_clusters (int): Maximum number of clusters to evaluate.
    """
    try:
        distortions = []
        all_cluster_labels = pd.DataFrame()
        K = range(1, max_clusters + 1)
        print(f"Calculating distortions for k values in range 1 to {max_clusters}")
        for k in K:
            kmeanModel = KMeans(n_clusters=k, random_state=0, n_init=10)
            kmeanModel.fit(features)
            distortions.append(kmeanModel.inertia_)

            # Save cluster labels for this k
            all_cluster_labels[f'Cluster_{k}'] = kmeanModel.labels_

        plt.figure(figsize=(10, 6))
        plt.plot(K, distortions, 'bx-')
        plt.xlabel('Number of clusters')
        plt.ylabel('Distortion')
        plt.title('The Elbow Method showing the optimal number of clusters')
        elbow_plot_file = os.path.join(output_dir, f'{os.path.basename(output_dir)}_kmeans_elbow_plot.png')
        plt.savefig(elbow_plot_file)
        plt.close()

        print(f"Distortions: {distortions}")

        output_clusters_file = os.path.join(output_dir, f'{os.path.basename(output_dir)}_kmeans_all_clusters.tsv.gz')
        all_cluster_labels.to_csv(output_clusters_file, sep='\t', index=False, compression='gzip')

        print(f"All K-means clustering results saved to {output_clusters_file}")

        # Using knee point detection method
        second_derivative = np.diff(distortions, 2)
        optimal_clusters = np.argmin(second_derivative) + 2
        print(f'Optimal number of clusters: {optimal_clusters}')

        kmeans = KMeans(n_clusters=optimal_clusters, random_state=0, n_init=10)
        kmeans.fit(features)
        
        clusters_df = pd.DataFrame({'Optimal_Cluster': kmeans.labels_}) 
        # Save optimal cluster labels
        output_optimal_clusters_file = os.path.join(output_dir, f'{os.path.basename(output_dir)}_kmeans_optimal_clusters_{optimal_clusters}.tsv.gz')
        clusters_df.to_csv(output_optimal_clusters_file, sep='\t', index=False, compression='gzip')
        
        print(f"K-means clustering with optimal number of clusters completed and results saved to {output_optimal_clusters_file}")
    
    except Exception as e:
        print(f"Error performing K-means clustering: {e}")

def main(file_path, output, sep, pca, tsne, umap, kmeans):
    """Main function to handle the overall analysis."""
    if not os.path.exists(output):
        os.makedirs(output)
    
    print(f"Output directory {output} created or already exists.")

    for f in os.listdir(output):
        os.remove(os.path.join(output, f))
    
    print("Output directory cleared.")

    if pca is not None:
        print("Starting PCA analysis...")
        pca_result = pca_analysis(file_path, output, pca)
        if tsne is not None:
            print("Starting t-SNE analysis...")
            tsne_analysis(pca_result, output, tsne)
        if umap is not None:
            print("Starting UMAP analysis...")
            umap_analysis(pca_result, output, umap)
        if kmeans is not None:
            print("Starting K-means clustering...")
            kmeans_clustering(pca_result, output, kmeans)
    elif kmeans is not None:
        print("Starting K-means clustering...")
        compression = 'gzip' if file_path.endswith('.gz') else None
        data = pd.read_csv(file_path, sep=sep, compression=compression)
        data.fillna(0, inplace=True)
        features = data.iloc[:, 1:]
        kmeans_clustering(features, output, kmeans)
    else:
        print("Reading TSV file...")
        read_tsv(file_path, output, sep=sep)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to read a TSV or TSV.GZ file and perform various analyses.")
    parser.add_argument('file_path', type=str, help='Path to the TSV or TSV.GZ file')
    parser.add_argument('-o', '--output', type=str, required=True, help='Output directory for saving results')
    parser.add_argument('-s', '--sep', type=str, default='\t', help='Column separator for input file (default is tab)')
    parser.add_argument('--pca', type=str, nargs='?', const='auto', default=None, help='Perform PCA analysis with specified number of components or "auto" for default')
    parser.add_argument('--tsne', type=int, nargs='?', const=2, default=None, help='Perform t-SNE analysis with specified number of dimensions (default 2)')
    parser.add_argument('--umap', type=int, nargs='?', const=2, default=None, help='Perform UMAP analysis with specified number of dimensions (default 2)')
    parser.add_argument('-k', '--kmeans', type=int, nargs='?', const=10, default=None, help='Perform K-means clustering and determine optimal number of clusters up to specified maximum')

    args = parser.parse_args()

    print("Arguments parsed successfully.")
    print(f"file_path: {args.file_path}")
    print(f"output: {args.output}")
    print(f"sep: {args.sep}")
    print(f"pca: {args.pca}")
    print(f"tsne: {args.tsne}")
    print(f"umap: {args.umap}")
    print(f"kmeans: {args.kmeans}")

    main(args.file_path, args.output, args.sep, args.pca, args.tsne, args.umap, args.kmeans)
