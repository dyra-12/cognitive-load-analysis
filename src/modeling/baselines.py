#!/usr/bin/env python3
"""
baselines.py

Provides baseline models and LOUO evaluation utilities:
 - majority baseline (predict most frequent class per training set)
 - logistic regression baseline

Functions:
 - run_baselines_louo(df, feature_cols, group_col='participantId', target_col='High_Load')

Returns a dict with fold-level metrics and aggregated summary.
"""

import os
from typing import Any, Dict, List

import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import LeaveOneGroupOut


def evaluate_fold(y_true, y_pred, y_score=None):
    """Compute typical evaluation metrics for a single fold.

    Returns a dictionary with accuracy, precision_pos, recall_pos, f1_pos and roc_auc
    when applicable.
    """
    metrics = {}
    metrics["accuracy"] = float(accuracy_score(y_true, y_pred))
    # for positive class (1)
    try:
        metrics["precision_pos"] = float(
            precision_score(y_true, y_pred, zero_division=0)
        )
    except Exception:
        metrics["precision_pos"] = float("nan")
    try:
        metrics["recall_pos"] = float(recall_score(y_true, y_pred, zero_division=0))
    except Exception:
        metrics["recall_pos"] = float("nan")
    try:
        metrics["f1_pos"] = float(f1_score(y_true, y_pred, zero_division=0))
    except Exception:
        metrics["f1_pos"] = float("nan")
    # ROC AUC only if both classes present in y_true
    if y_score is not None and len(np.unique(y_true)) > 1:
        try:
            metrics["roc_auc"] = float(roc_auc_score(y_true, y_score))
        except Exception:
            metrics["roc_auc"] = float("nan")
    else:
        metrics["roc_auc"] = float("nan")
    return metrics


def majority_baseline_predict(train_y, test_X):
    """Return predictions and a dummy score for a majority-class baseline.

    Parameters
    - train_y: array-like -- training labels used to determine majority class
    - test_X: array-like -- test features (only used for sizing the output)

    Returns
    - y_pred: ndarray of ints (majority label)
    - y_score: ndarray of floats (dummy score equal to majority label)
    """
    # predict most frequent label in train_y
    vals, counts = np.unique(train_y, return_counts=True)
    majority_label = int(vals[np.argmax(counts)])
    return np.full(
        shape=(test_X.shape[0],), fill_value=majority_label, dtype=int
    ), np.full(shape=(test_X.shape[0],), fill_value=float(majority_label))


def run_baselines_louo(
    df: pd.DataFrame,
    feature_cols: List[str],
    group_col: str = "participantId",
    target_col: str = "High_Load",
) -> Dict[str, Any]:
    """
    Run majority baseline and logistic regression baseline under Leave-One-Group-Out (LOUO).
    Returns dict containing fold-level metrics for each baseline and aggregate summaries.
    """
    X = df[feature_cols].values
    y = df[target_col].values
    groups = df[group_col].values

    logo = LeaveOneGroupOut()
    folds = []
    fold_idx = 0

    maj_records = []
    lr_records = []

    for train_idx, test_idx in logo.split(X, y, groups):
        left_out = groups[test_idx[0]]
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        # Majority baseline
        y_pred_maj, y_score_maj = majority_baseline_predict(y_train, X_test)
        maj_m = evaluate_fold(y_test, y_pred_maj, y_score_maj)
        maj_m.update({"left_out": left_out, "fold": fold_idx})
        maj_records.append(maj_m)

        # Logistic regression baseline (simple L2 solver, class_weight balanced)
        lr = LogisticRegression(
            max_iter=2000, class_weight="balanced", solver="liblinear"
        )
        try:
            lr.fit(X_train, y_train)
            y_pred_lr = lr.predict(X_test)
            # for roc_auc, need positive probability
            if hasattr(lr, "predict_proba"):
                y_score_lr = lr.predict_proba(X_test)[:, 1]
            else:
                y_score_lr = lr.decision_function(X_test)
            lr_m = evaluate_fold(y_test, y_pred_lr, y_score_lr)
        except Exception as e:
            # In degenerate cases (e.g., single-class train), fallback to majority
            y_pred_lr = np.full_like(y_test, fill_value=int(np.round(np.mean(y_train))))
            y_score_lr = np.full_like(
                y_test, fill_value=float(np.round(np.mean(y_train)))
            )
            lr_m = evaluate_fold(y_test, y_pred_lr, y_score_lr)
        lr_m.update({"left_out": left_out, "fold": fold_idx})
        lr_records.append(lr_m)

        fold_idx += 1

    maj_df = pd.DataFrame(maj_records)
    lr_df = pd.DataFrame(lr_records)

    summary = {
        "majority_fold_metrics": maj_df,
        "logreg_fold_metrics": lr_df,
        "majority_summary": maj_df.mean(numeric_only=True).to_dict(),
        "logreg_summary": lr_df.mean(numeric_only=True).to_dict(),
    }
    return summary


# If script called directly, provide a CLI demonstration
if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--csv", type=str, default="../../data/processed/modeling_dataset.csv"
    )
    parser.add_argument("--outdir", type=str, default="../../results/modeling")
    args = parser.parse_args()

    df = pd.read_csv(args.csv)
    # infer feature columns (drop known metadata)
    drop_cols = {"participantId", "task_id", "tlx", "High_Load"}
    feature_cols = [c for c in df.columns if c not in drop_cols]
    res = run_baselines_louo(df, feature_cols)
    os.makedirs(args.outdir, exist_ok=True)
    res["majority_fold_metrics"].to_csv(
        os.path.join(args.outdir, "baseline_majority_fold_metrics.csv"), index=False
    )
    res["logreg_fold_metrics"].to_csv(
        os.path.join(args.outdir, "baseline_logreg_fold_metrics.csv"), index=False
    )
    pd.DataFrame([res["majority_summary"]]).to_csv(
        os.path.join(args.outdir, "baseline_majority_summary.csv"), index=False
    )
    pd.DataFrame([res["logreg_summary"]]).to_csv(
        os.path.join(args.outdir, "baseline_logreg_summary.csv"), index=False
    )
    print("Saved baseline metrics to", args.outdir)
