#!/usr/bin/env python3
"""
shap_clustering.py

Loads saved SHAP values and feature names, performs clustering on SHAP vectors:
 - k-means (k=2)
Saves:
 - shap_cluster_labels.csv
 - shap_clusters_pca.png

Usage:
    python shap_clustering.py \
        --shap-values ../../results/interpretation/shap_values.npy \
        --features ../../results/interpretation/shap_feature_names.json \
        --csv ../../data/processed/modeling_dataset.csv \
        --outdir ../../results/interpretation
"""

import argparse
import json
import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA


def main():
    """Load SHAP arrays and cluster SHAP vectors (KMeans), saving labels and a PCA plot.

    This helps identify groups of examples with similar model explanations.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--shap-values", type=str, required=True)
    parser.add_argument("--features", type=str, required=True)
    parser.add_argument("--csv", type=str, required=True)
    parser.add_argument("--outdir", type=str, required=True)
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    shap_values = np.load(args.shap_values)
    df = pd.read_csv(args.csv)

    # K-means clustering on SHAP vectors (simple 2-cluster separation)
    kmeans = KMeans(n_clusters=2, random_state=2025)
    labels = kmeans.fit_predict(shap_values)

    # Save cluster labels
    out = df[["participantId", "task_id", "tlx", "High_Load"]].copy()
    out["shap_cluster"] = labels
    out.to_csv(os.path.join(args.outdir, "shap_cluster_labels.csv"), index=False)

    # PCA visualization
    pca = PCA(n_components=2)
    comps = pca.fit_transform(shap_values)

    plt.figure(figsize=(8, 7))
    plt.scatter(comps[:, 0], comps[:, 1], c=labels, cmap="coolwarm", s=80, alpha=0.8)
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("SHAP Clusters (PCA)")
    plt.savefig(os.path.join(args.outdir, "shap_clusters_pca.png"))
    plt.close()

    print("Saved cluster labels and PCA plot in:", args.outdir)


if __name__ == "__main__":
    main()
