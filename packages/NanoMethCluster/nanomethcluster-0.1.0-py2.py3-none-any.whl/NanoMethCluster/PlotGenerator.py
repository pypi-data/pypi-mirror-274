import os
import pandas as pd
import plotly.express as px
import gzip
import argparse

def read_gzipped_tsv(file_path):
    with gzip.open(file_path, 'rt') as f:
        return pd.read_csv(f, sep='\t')

def read_kraken_file(file_path):
    """
    Reads a kraken2 file and extracts the 2nd and 3rd columns.
    """
    return pd.read_csv(file_path, sep='\t', header=None, usecols=[1, 2], names=['Read_Name', 'Kraken_Label'])

def create_interactive_plots(input_dir, pca_components, tsne_components, umap_components, kmeans_clusters, additional_file, kraken_file, create_matrix):
    output_dir = os.path.join(input_dir, "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    additional_data = None
    if additional_file:
        additional_data = read_gzipped_tsv(additional_file)
        additional_data.fillna(0, inplace=True)

    kraken_data = None
    if kraken_file:
        kraken_data = read_kraken_file(kraken_file)
        kraken_data.fillna(0, inplace=True)
        # Filter kraken_data to match Read_Name in additional_data
        kraken_data = kraken_data[kraken_data['Read_Name'].isin(additional_data['Read_Name'])]
        # Sort kraken_data to match the order in additional_data
        kraken_data.set_index('Read_Name', inplace=True)
        kraken_data = kraken_data.reindex(additional_data['Read_Name']).reset_index()

    # Reading K-means clustering results
    kmeans_file = None
    kmeans_labels = None
    if kmeans_clusters:
        kmeans_file = [f for f in os.listdir(input_dir) if f'kmeans_optimal_clusters_{kmeans_clusters}' in f]
        if kmeans_file:
            kmeans_file = kmeans_file[0]
            kmeans_results = read_gzipped_tsv(os.path.join(input_dir, kmeans_file))
            kmeans_results.fillna(0, inplace=True)
            kmeans_labels = kmeans_results['Optimal_Cluster'].astype(str)  # Convert to string to treat as categorical
            additional_data['Cluster'] = kmeans_labels.values
        else:
            print(f"No K-means clustering results found for {kmeans_clusters} clusters.")

    # Reading PCA results
    pca_file = [f for f in os.listdir(input_dir) if 'pca_results' in f]
    pca_results = None
    if pca_file:
        pca_file = pca_file[0]
        pca_results = read_gzipped_tsv(os.path.join(input_dir, pca_file))
        pca_results.fillna(0, inplace=True)
        
        if kmeans_clusters:
            pca_results['Cluster'] = kmeans_labels

        if pca_components and len(pca_components) == 2:
            fig_pca = px.scatter(pca_results, x=pca_results.columns[pca_components[0]], y=pca_results.columns[pca_components[1]], color='Cluster' if kmeans_clusters else None, title="PCA Results")
        elif pca_components and len(pca_components) == 3:
            fig_pca = px.scatter_3d(pca_results, x=pca_results.columns[pca_components[0]], y=pca_results.columns[pca_components[1]], z=pca_results.columns[pca_components[2]], color='Cluster' if kmeans_clusters else None, title="PCA Results")
        else:
            print("Invalid number of PCA components specified. Please specify 2 or 3 components.")
        
        pca_plot_path = os.path.join(output_dir, 'pca_plot.html')
        fig_pca.write_html(pca_plot_path)
    else:
        print("No PCA results found.")

    # Reading t-SNE results
    tsne_file = [f for f in os.listdir(input_dir) if 'tsne_results' in f]
    tsne_results = None
    if tsne_file:
        tsne_file = tsne_file[0]
        tsne_results = read_gzipped_tsv(os.path.join(input_dir, tsne_file))
        tsne_results.fillna(0, inplace=True)
        
        if kmeans_clusters:
            tsne_results['Cluster'] = kmeans_labels

        if tsne_components and len(tsne_components) == 2:
            fig_tsne = px.scatter(tsne_results, x=tsne_results.columns[tsne_components[0]], y=tsne_results.columns[tsne_components[1]], color='Cluster' if kmeans_clusters else None, title="t-SNE Results")
        elif len(tsne_components) >= 3:
            fig_tsne = px.scatter_3d(tsne_results, x=tsne_results.columns[tsne_components[0]], y=tsne_results.columns[tsne_components[1]], z=tsne_results.columns[tsne_components[2]], color='Cluster' if kmeans_clusters else None, title="t-SNE Results")
        
        tsne_plot_path = os.path.join(output_dir, 'tsne_plot.html')
        fig_tsne.write_html(tsne_plot_path)
    else:
        print("No t-SNE results found.")

    # Reading UMAP results
    umap_file = [f for f in os.listdir(input_dir) if 'umap_results' in f]
    umap_results = None
    if umap_file:
        umap_file = umap_file[0]
        umap_results = read_gzipped_tsv(os.path.join(input_dir, umap_file))
        umap_results.fillna(0, inplace=True)
        
        if kmeans_clusters:
            umap_results['Cluster'] = kmeans_labels

        if umap_components and len(umap_components) == 2:
            fig_umap = px.scatter(umap_results, x=umap_results.columns[umap_components[0]], y=umap_results.columns[umap_components[1]], color='Cluster' if kmeans_clusters else None, title="UMAP Results")
        elif len(umap_components) >= 3:
            fig_umap = px.scatter_3d(umap_results, x=umap_results.columns[umap_components[0]], y=umap_results.columns[umap_components[1]], z=umap_results.columns[umap_components[2]], color='Cluster' if kmeans_clusters else None, title="UMAP Results")
        
        umap_plot_path = os.path.join(output_dir, 'umap_plot.html')
        fig_umap.write_html(umap_plot_path)
    else:
        print("No UMAP results found.")

    # Apply coloring based on Count_Max_Ch, Count_Max_Cm, Count_Max_Ch_m
    if additional_data is not None:
        color_columns = ['Count_Max_Ch', 'Count_Max_Cm', 'Count_Max_Ch_m']
        available_columns = [col for col in color_columns if col in additional_data.columns]
        for col in available_columns:
            color_label = additional_data[col]
            if pca_results is not None:
                pca_results['Color'] = color_label
            if tsne_results is not None:
                tsne_results['Color'] = color_label
            if umap_results is not None:
                umap_results['Color'] = color_label

            # PCA plots with different colorings
            if pca_file:
                if len(pca_components) == 2:
                    fig_pca_colored = px.scatter(pca_results, x=pca_results.columns[pca_components[0]], y=pca_results.columns[pca_components[1]], color='Color', title=f"PCA Results colored by {col}")
                elif len(pca_components) == 3:
                    fig_pca_colored = px.scatter_3d(pca_results, x=pca_results.columns[pca_components[0]], y=pca_results.columns[pca_components[1]], z=pca_results.columns[pca_components[2]], color='Color', title=f"PCA Results colored by {col}")
                pca_colored_plot_path = os.path.join(output_dir, f'pca_plot_colored_by_{col}.html')
                fig_pca_colored.write_html(pca_colored_plot_path)

            # t-SNE plots with different colorings
            if tsne_file:
                if len(tsne_components) == 2:
                    fig_tsne_colored = px.scatter(tsne_results, x=tsne_results.columns[tsne_components[0]], y=tsne_results.columns[tsne_components[1]], color='Color', title=f"t-SNE Results colored by {col}")
                elif len(tsne_components) >= 3:
                    fig_tsne_colored = px.scatter_3d(tsne_results, x=tsne_results.columns[tsne_components[0]], y=tsne_results.columns[tsne_components[1]], z=tsne_results.columns[tsne_components[2]], color='Color', title=f"t-SNE Results colored by {col}")
                tsne_colored_plot_path = os.path.join(output_dir, f'tsne_plot_colored_by_{col}.html')
                fig_tsne_colored.write_html(tsne_colored_plot_path)

            # UMAP plots with different colorings
            if umap_file:
                if len(umap_components) == 2:
                    fig_umap_colored = px.scatter(umap_results, x=umap_results.columns[umap_components[0]], y=umap_results.columns[umap_components[1]], color='Color', title=f"UMAP Results colored by {col}")
                elif len(umap_components) >= 3:
                    fig_umap_colored = px.scatter_3d(umap_results, x=umap_results.columns[umap_components[0]], y=umap_results.columns[umap_components[1]], z=umap_results.columns[umap_components[2]], color='Color', title=f"UMAP Results colored by {col}")
                umap_colored_plot_path = os.path.join(output_dir, f'umap_plot_colored_by_{col}.html')
                fig_umap_colored.write_html(umap_colored_plot_path)

    # Plot PCA, t-SNE, UMAP again with kraken labels
    if kraken_data is not None:
        kraken_label = kraken_data['Kraken_Label'].astype(str)
        if pca_results is not None:
            pca_results['Kraken_Label'] = kraken_label
        if tsne_results is not None:
            tsne_results['Kraken_Label'] = kraken_label
        if umap_results is not None:
            umap_results['Kraken_Label'] = kraken_label

        # PCA plots with kraken labels
        if pca_file:
            if len(pca_components) == 2:
                fig_pca_kraken = px.scatter(pca_results, x=pca_results.columns[pca_components[0]], y=pca_results.columns[pca_components[1]], color='Kraken_Label', title="PCA Results with Kraken Labels")
            elif len(pca_components) == 3:
                fig_pca_kraken = px.scatter_3d(pca_results, x=pca_results.columns[pca_components[0]], y=pca_results.columns[pca_components[1]], z=pca_results.columns[pca_components[2]], color='Kraken_Label', title="PCA Results with Kraken Labels")
            pca_kraken_plot_path = os.path.join(output_dir, 'pca_plot_with_kraken.html')
            fig_pca_kraken.write_html(pca_kraken_plot_path)

        # t-SNE plots with kraken labels
        if tsne_file:
            if len(tsne_components) == 2:
                fig_tsne_kraken = px.scatter(tsne_results, x=tsne_results.columns[tsne_components[0]], y=tsne_results.columns[tsne_components[1]], color='Kraken_Label', title="t-SNE Results with Kraken Labels")
            elif len(tsne_components) >= 3:
                fig_tsne_kraken = px.scatter_3d(tsne_results, x=tsne_results.columns[tsne_components[0]], y=tsne_results.columns[tsne_components[1]], z=tsne_results.columns[tsne_components[2]], color='Kraken_Label', title="t-SNE Results with Kraken Labels")
            tsne_kraken_plot_path = os.path.join(output_dir, 'tsne_plot_with_kraken.html')
            fig_tsne_kraken.write_html(tsne_kraken_plot_path)

        # UMAP plots with kraken labels
        if umap_file:
            if len(umap_components) == 2:
                fig_umap_kraken = px.scatter(umap_results, x=umap_results.columns[umap_components[0]], y=umap_results.columns[umap_components[1]], color='Kraken_Label', title="UMAP Results with Kraken Labels")
            elif len(umap_components) >= 3:
                fig_umap_kraken = px.scatter_3d(umap_results, x=umap_results.columns[umap_components[0]], y=umap_results.columns[umap_components[1]], z=umap_results.columns[umap_components[2]], color='Kraken_Label', title="UMAP Results with Kraken Labels")
            umap_kraken_plot_path = os.path.join(output_dir, 'umap_plot_with_kraken.html')
            fig_umap_kraken.write_html(umap_kraken_plot_path)

    # Create matrix files if requested
    if create_matrix:
        if additional_data is not None and kmeans_clusters:
            # Create matrix for additional data
            available_columns = [col for col in ['Count_Max_Ch', 'Count_Max_Cm', 'Count_Max_Ch_m'] if col in additional_data.columns]
            if available_columns:
                cluster_means = additional_data.groupby(kmeans_labels)[available_columns].mean()
                cluster_means_file = os.path.join(output_dir, 'cluster_means.tsv')
                cluster_means.to_csv(cluster_means_file, sep='\t')
        
        if kraken_data is not None and kmeans_clusters:
            # Create matrix for kraken data
            kraken_counts = pd.crosstab(kmeans_labels, kraken_label)
            kraken_counts_file = os.path.join(output_dir, 'kraken_cluster_counts.tsv')
            kraken_counts.to_csv(kraken_counts_file, sep='\t')

        # Create combined matrix file
        if additional_data is not None and kmeans_clusters:
            combined_columns = ['Read_Name', 'Count_Max_Ch', 'Count_Max_Cm', 'Count_Max_Ch_m']
            available_combined_columns = [col for col in combined_columns if col in additional_data.columns]
            combined_data = additional_data[available_combined_columns].copy()
            if 'Read_Name' in available_combined_columns:
                combined_data.set_index('Read_Name', inplace=True)
            if kraken_data is not None:
                combined_data['Kraken_Label'] = kraken_data['Kraken_Label'].values
            combined_data['Cluster'] = kmeans_labels.values
            combined_matrix_file = os.path.join(output_dir, 'combined_matrix.tsv')
            combined_data.to_csv(combined_matrix_file, sep='\t')
            
    print(f"Interactive plots and matrices saved in {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Script to generate interactive Plotly graphs from analysis results and create matrices.")
    parser.add_argument('input_dir', type=str, help='Directory containing analysis result files')
    parser.add_argument('--pca', type=int, nargs='+', help='PCA components to visualize (specify 2 or 3 components)')
    parser.add_argument('--tsne', type=int, nargs='+', help='t-SNE components to visualize (specify 2 or 3 components)')
    parser.add_argument('--umap', type=int, nargs='+', help='UMAP components to visualize (specify 2 or 3 components)')
    parser.add_argument('-k', '--kmeans', type=int, help='Number of clusters to use for coloring the plots')
    parser.add_argument('--additional_file', type=str, help='Additional TSV or TSV.GZ file with extra data')
    parser.add_argument('--kraken', type=str, help='Kraken2 TSV file with tab delimiter and no header, to use for additional coloring')
    parser.add_argument('--matrix', action='store_true', help='Flag to create matrices for k-means clusters and additional data or kraken data')
    args = parser.parse_args()

    create_interactive_plots(args.input_dir, args.pca, args.tsne, args.umap, args.kmeans, args.additional_file, args.kraken, args.matrix)
