#!/usr/bin/env python3
"""
feature_importance.py

Extracts feature importances from the tuned Random Forest model and saves:
 - feature_importances.csv
 - feature_importances_barplot.png

Usage:
    python feature_importance.py \
        --model ../../models/tuned_random_forest_model.joblib \
        --csv ../../data/processed/modeling_dataset.csv \
        --outdir ../../results/interpretation
"""

import argparse
import os

import joblib
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd


def main():
    """Extract and save Random Forest feature importances and a horizontal bar plot.

    Expects a fitted `Pipeline` with a `rf` step accessible via `named_steps`.
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

    model = joblib.load(args.model)
    rf = model.named_steps["rf"]

    importances = rf.feature_importances_
    fi = pd.DataFrame({"feature": feature_cols, "importance": importances}).sort_values(
        "importance", ascending=False
    )

    # Save CSV
    fi.to_csv(os.path.join(args.outdir, "feature_importances.csv"), index=False)

    # Bar plot
    plt.figure(figsize=(10, 7))
    plt.barh(fi["feature"], fi["importance"])
    plt.gca().invert_yaxis()
    plt.xlabel("Importance")
    plt.title("Random Forest Feature Importances")
    plt.tight_layout()
    plt.savefig(os.path.join(args.outdir, "feature_importances_barplot.png"))
    plt.close()

    print("Saved feature importances CSV and plot to:", args.outdir)


if __name__ == "__main__":
    main()
