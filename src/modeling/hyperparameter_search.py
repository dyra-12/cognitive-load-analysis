#!/usr/bin/env python3
"""
hyperparameter_search.py

Performs hyperparameter tuning for RandomForestClassifier using grouped CV
(LeaveOneGroupOut) so that participant groups are respected.

Saves best parameters to JSON and returns best estimator.

Usage:
    python hyperparameter_search.py --csv ../../data/processed/modeling_dataset.csv --out models/rf_tuned_params.json
"""

import argparse
import json
import os

import numpy as np
import pandas as pd
from joblib import dump
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.model_selection import GridSearchCV, LeaveOneGroupOut
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler


def run_grouped_grid_search(
    df, feature_cols, group_col="participantId", n_jobs=1, random_state=2025
):
    """Run a grouped GridSearchCV over RandomForest hyperparameters.

    Parameters
    - df: pandas.DataFrame -- dataset containing features and `High_Load` target
    - feature_cols: list[str] -- feature column names
    - group_col: str -- grouping column for LeaveOneGroupOut
    - n_jobs: int -- parallel jobs
    - random_state: int -- RNG seed

    Returns
    - fitted GridSearchCV object
    """
    X = df[feature_cols].values
    y = df["High_Load"].values
    groups = df[group_col].values

    # Pipeline: imputer -> scaler -> RF
    pipe = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            (
                "rf",
                RandomForestClassifier(
                    random_state=random_state, class_weight="balanced"
                ),
            ),
        ]
    )

    param_grid = {
        "rf__n_estimators": [100, 300, 600],
        "rf__max_depth": [None, 6, 12],
        "rf__min_samples_split": [2, 5],
        "rf__min_samples_leaf": [1, 2],
    }

    logo = LeaveOneGroupOut()
    grid = GridSearchCV(
        pipe,
        param_grid,
        cv=logo.split(X, y, groups),
        scoring="f1",
        n_jobs=n_jobs,
        verbose=1,
    )
    grid.fit(X, y)

    return grid


def main():
    """CLI entrypoint to run grouped hyperparameter search and save results."""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--csv", type=str, default="../../data/processed/modeling_dataset.csv"
    )
    parser.add_argument("--out", type=str, default="../../models/rf_grid_search.joblib")
    parser.add_argument("--n-jobs", type=int, default=1)
    args = parser.parse_args()

    df = pd.read_csv(os.path.abspath(args.csv))
    drop_cols = {"participantId", "task_id", "tlx", "High_Load"}
    feature_cols = [c for c in df.columns if c not in drop_cols]

    grid = run_grouped_grid_search(df, feature_cols, n_jobs=args.n_jobs)
    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    dump(grid, os.path.abspath(args.out))
    print("Saved GridSearchCV object to", args.out)
    # Save best params
    best = grid.best_params_
    with open(os.path.join(os.path.dirname(args.out), "rf_best_params.json"), "w") as f:
        json.dump(best, f, indent=2)
    print("Best params saved to rf_best_params.json")
    print("Best score (CV f1):", grid.best_score_)


if __name__ == "__main__":
    main()
