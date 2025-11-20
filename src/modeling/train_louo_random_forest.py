#!/usr/bin/env python3
"""
train_louo_random_forest.py

1) Optionally run hyperparameter search (calls hyperparameter_search.py)
2) Trains a RandomForest on the full dataset using best params (or defaults)
3) Evaluates with LOUO using evaluate_model.evaluate_louo()
4) Saves model and results to models/ and results/

Usage:
    python train_louo_random_forest.py --csv ../../data/processed/modeling_dataset.csv --model-out ../../models/tuned_random_forest_model.joblib
"""

import argparse
import json
import os

import joblib
import numpy as np
import pandas as pd
from evaluate_model import evaluate_louo, save_feature_importances
from hyperparameter_search import run_grouped_grid_search
from sklearn.ensemble import RandomForestClassifier
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

DEFAULT_PARAMS = {
    "rf__n_estimators": 300,
    "rf__max_depth": 12,
    "rf__min_samples_split": 2,
    "rf__min_samples_leaf": 1,
}


def build_pipeline_from_params(params, random_state=2025):
    """Construct a preprocessing + RandomForest pipeline from parameter dict.

    Parameters
    - params: dict -- keys use scikit-learn pipeline parameter names, e.g. 'rf__n_estimators'
    - random_state: int

    Returns
    - sklearn.Pipeline instance
    """
    pipe = Pipeline(
        [
            ("imputer", SimpleImputer(strategy="median")),
            ("scaler", StandardScaler()),
            (
                "rf",
                RandomForestClassifier(
                    random_state=random_state,
                    class_weight="balanced",
                    n_estimators=params.get("rf__n_estimators", 300),
                    max_depth=params.get("rf__max_depth", None),
                    min_samples_split=params.get("rf__min_samples_split", 2),
                    min_samples_leaf=params.get("rf__min_samples_leaf", 1),
                ),
            ),
        ]
    )
    return pipe


def main():
    """Train a RandomForest pipeline (optionally tune) and evaluate with LOUO.

    CLI wrapper around hyperparameter search, pipeline construction, training,
    LOUO evaluation, and saving of model + results.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--csv", type=str, default="../../data/processed/modeling_dataset.csv"
    )
    parser.add_argument(
        "--model-out", type=str, default="../../models/tuned_random_forest_model.joblib"
    )
    parser.add_argument("--results-outdir", type=str, default="../../results/modeling")
    parser.add_argument(
        "--do-search",
        action="store_true",
        help="Run grouped hyperparameter search before training",
    )
    parser.add_argument(
        "--grid-out", type=str, default="../../models/rf_grid_search.joblib"
    )
    parser.add_argument("--n-jobs", type=int, default=1)
    args = parser.parse_args()

    df = pd.read_csv(os.path.abspath(args.csv))
    drop_cols = {"participantId", "task_id", "tlx", "High_Load"}
    feature_cols = [c for c in df.columns if c not in drop_cols]

    os.makedirs(os.path.dirname(os.path.abspath(args.model_out)), exist_ok=True)
    os.makedirs(os.path.abspath(args.results_outdir), exist_ok=True)

    best_params = DEFAULT_PARAMS.copy()
    if args.do_search:
        print("Running grouped hyperparameter search (this may take time)...")
        grid = run_grouped_grid_search(df, feature_cols, n_jobs=args.n_jobs)
        # extract best params (GridSearchCV returns keys like 'rf__n_estimators')
        best_params = {k: v for k, v in grid.best_params_.items()}
        # save grid object
        joblib.dump(grid, os.path.abspath(args.grid_out))
        print("Saved grid search object to", args.grid_out)
        with open(
            os.path.join(os.path.dirname(args.grid_out), "rf_best_params.json"), "w"
        ) as f:
            json.dump(best_params, f, indent=2)
        print("Saved best params:", best_params)
    else:
        print("Using default RF params:", best_params)

    # build pipeline and fit on full data
    pipeline = build_pipeline_from_params(best_params)
    X = df[feature_cols].values
    y = df["High_Load"].values
    pipeline.fit(X, y)
    # save model
    joblib.dump(pipeline, os.path.abspath(args.model_out))
    print("Saved fitted model to", args.model_out)

    # Evaluate under LOUO
    folds_df, summary, mis = evaluate_louo(pipeline, df, feature_cols)
    folds_df.to_csv(
        os.path.join(args.results_outdir, "rf_fold_metrics_ultrarealistic.csv"),
        index=False,
    )
    pd.DataFrame([summary]).to_csv(
        os.path.join(args.results_outdir, "rf_summary_ultrarealistic.csv"), index=False
    )
    print("Saved LOUO evaluation results to", args.results_outdir)

    # Save feature importances
    save_feature_importances(
        pipeline.named_steps["rf"],
        feature_cols,
        os.path.join(
            args.results_outdir, "feature_importances_ultrarealistic_summary.csv"
        ),
    )

    # Save misclassifications for analysis
    mis_df = pd.DataFrame(mis)
    mis_df.to_csv(
        os.path.join(args.results_outdir, "rf_misclassifications.csv"), index=False
    )
    print("Saved misclassifications")


if __name__ == "__main__":
    main()
