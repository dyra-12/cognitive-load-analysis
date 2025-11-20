#!/usr/bin/env python3
"""
shap_analysis.py

Compute SHAP values for the tuned Random Forest model and save:
 - shap_summary_bar.png
 - shap_summary_beeswarm.png
 - shap_values.npy
 - shap_feature_names.json

Usage:
    python shap_analysis.py \
        --model ../../models/tuned_random_forest_model.joblib \
        --csv ../../data/processed/modeling_dataset.csv \
        --outdir ../../results/interpretation
"""

import argparse
import json
import os

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import shap


def main():
    """Compute and save SHAP values and summary plots for a trained RF pipeline.

    Expects a scikit-learn `Pipeline` with steps `imputer`, `scaler`, and `rf`.
    Saves raw SHAP arrays and common summary visualizations into `--outdir`.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--model", type=str, required=True)
    parser.add_argument("--csv", type=str, required=True)
    parser.add_argument("--outdir", type=str, required=True)
    args = parser.parse_args()

    os.makedirs(args.outdir, exist_ok=True)

    df = pd.read_csv(args.csv)
    drop_cols = {"participantId", "task_id", "tlx", "High_Load"}
    feature_cols = [c for c in df.columns if c not in drop_cols]
    X = df[feature_cols]

    model = joblib.load(args.model)

    print("Computing SHAP values (TreeExplainer)...")
    # TreeExplainer accepts the underlying fitted tree model (RandomForest estimator).
    # We compute SHAP values on the transformed feature matrix (imputer -> scaler)
    # because the RF was trained on the pipeline's output.
    explainer = shap.TreeExplainer(model.named_steps["rf"])
    transformed_X = model.named_steps["scaler"].transform(
        model.named_steps["imputer"].transform(X)
    )
    # shap_values for binary classifiers are returned as an array for each class;
    # index [1] corresponds to the positive class explanations.
    shap_values = explainer.shap_values(transformed_X)[1]

    # Save SHAP data
    np.save(os.path.join(args.outdir, "shap_values.npy"), shap_values)
    with open(os.path.join(args.outdir, "shap_feature_names.json"), "w") as f:
        json.dump(feature_cols, f, indent=2)

    # SHAP summary bar
    plt.figure(figsize=(10, 7))
    shap.summary_plot(shap_values, X, plot_type="bar", show=False)
    plt.tight_layout()
    plt.savefig(os.path.join(args.outdir, "shap_summary_bar.png"))
    plt.close()

    # SHAP beeswarm
    plt.figure(figsize=(10, 7))
    shap.summary_plot(shap_values, X, show=False)
    plt.tight_layout()
    plt.savefig(os.path.join(args.outdir, "shap_summary_beeswarm.png"))
    plt.close()

    print("Saved SHAP plots + raw arrays to:", args.outdir)


if __name__ == "__main__":
    main()
