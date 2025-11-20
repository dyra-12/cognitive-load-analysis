#!/usr/bin/env python3
"""
evaluate_model.py

Utilities for evaluating a classifier under Leave-One-User-Out (LOUO).
Saves fold-level metrics and an aggregate summary, and can save feature importances.

Functions:
 - evaluate_louo(model, df, feature_cols, group_col='participantId', target_col='High_Load')
 - save_fold_metrics_csv(metrics_df, out_path)
"""

import os
from typing import Any, Dict, List

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)
from sklearn.model_selection import LeaveOneGroupOut


def fold_metrics(y_true, y_pred, y_score=None):
    """Compute a small dictionary of common classification metrics for a fold.

    Parameters
    - y_true: array-like -- true labels
    - y_pred: array-like -- predicted labels
    - y_score: array-like or None -- scores for ROC AUC if available

    Returns
    - dict: contains accuracy, precision_pos, recall_pos, f1_pos, and roc_auc
    """
    m = {}
    m["accuracy"] = float(accuracy_score(y_true, y_pred))
    m["precision_pos"] = float(precision_score(y_true, y_pred, zero_division=0))
    m["recall_pos"] = float(recall_score(y_true, y_pred, zero_division=0))
    m["f1_pos"] = float(f1_score(y_true, y_pred, zero_division=0))
    if y_score is not None and len(np.unique(y_true)) > 1:
        try:
            m["roc_auc"] = float(roc_auc_score(y_true, y_score))
        except Exception:
            m["roc_auc"] = float("nan")
    else:
        m["roc_auc"] = float("nan")
    return m


def evaluate_louo(
    model,
    df: pd.DataFrame,
    feature_cols: List[str],
    group_col: str = "participantId",
    target_col: str = "High_Load",
):
    """
    Evaluate a fitted sklearn-like model under LOUO.
    model: fitted estimator with predict and predict_proba or decision_function
    returns (folds_df, summary_dict, misclassifications_list)
    """
    X = df[feature_cols].values
    y = df[target_col].values
    groups = df[group_col].values

    logo = LeaveOneGroupOut()
    records = []
    mis_list = []

    fold = 0
    for train_idx, test_idx in logo.split(X, y, groups):
        left_out = groups[test_idx[0]]
        X_train, X_test = X[train_idx], X[test_idx]
        y_train, y_test = y[train_idx], y[test_idx]

        # If model isn't fitted yet, fit (but normally model should be pre-fit on full train set)
        try:
            y_pred = model.predict(X_test)
            if hasattr(model, "predict_proba"):
                y_score = model.predict_proba(X_test)[:, 1]
            elif hasattr(model, "decision_function"):
                y_score = model.decision_function(X_test)
            else:
                y_score = None
        except Exception as e:
            # Fallback: fit on train split then predict
            model.fit(X_train, y_train)
            y_pred = model.predict(X_test)
            if hasattr(model, "predict_proba"):
                y_score = model.predict_proba(X_test)[:, 1]
            elif hasattr(model, "decision_function"):
                y_score = model.decision_function(X_test)
            else:
                y_score = None

        m = fold_metrics(y_test, y_pred, y_score)
        m["left_out"] = left_out
        m["fold"] = fold
        records.append(m)

        # record misclassifications for analysis
        for i, yi in enumerate(y_test):
            if yi != int(y_pred[i]):
                mis_list.append(
                    {
                        "left_out": left_out,
                        "test_idx_in_group": i,
                        "true": int(yi),
                        "pred": int(y_pred[i]),
                    }
                )

        fold += 1

    folds_df = pd.DataFrame(records)
    summary = folds_df.mean(numeric_only=True).to_dict()
    return folds_df, summary, mis_list


def save_fold_metrics_csv(metrics_df: pd.DataFrame, out_path: str):
    """Save a fold-level metrics DataFrame to CSV, creating directories as needed."""
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    metrics_df.to_csv(out_path, index=False)
    print("Saved fold metrics CSV:", out_path)


def save_feature_importances(model, feature_cols: List[str], out_path: str):
    """
    Extracts feature importances from model (if available) and saves to CSV.
    Supports tree-based .feature_importances_ or permutation importance fallback.
    """
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    importances = None
    try:
        if hasattr(model, "feature_importances_"):
            importances = model.feature_importances_
        elif hasattr(model, "steps") and "rf" in dict(model.steps):
            importances = dict(model.named_steps)["rf"].feature_importances_
        else:
            importances = None
    except Exception:
        importances = None

    if importances is not None:
        fi = pd.DataFrame({"feature": feature_cols, "importance": importances})
        fi = fi.sort_values("importance", ascending=False)
        fi.to_csv(out_path, index=False)
        print("Saved feature importances to:", out_path)
        return fi
    else:
        print("No direct feature importances found on model. Skipping.")
        return None


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model", type=str, default="../../models/tuned_random_forest_model.joblib"
    )
    parser.add_argument(
        "--csv", type=str, default="../../data/processed/modeling_dataset.csv"
    )
    parser.add_argument("--outdir", type=str, default="../../results/modeling")
    args = parser.parse_args()

    df = pd.read_csv(os.path.abspath(args.csv))
    drop_cols = {"participantId", "task_id", "tlx", "High_Load"}
    feature_cols = [c for c in df.columns if c not in drop_cols]

    model = joblib.load(os.path.abspath(args.model))
    folds_df, summary, mis = evaluate_louo(model, df, feature_cols)
    os.makedirs(args.outdir, exist_ok=True)
    folds_df.to_csv(
        os.path.join(args.outdir, "rf_fold_metrics_ultrarealistic.csv"), index=False
    )
    pd.DataFrame([summary]).to_csv(
        os.path.join(args.outdir, "rf_summary_ultrarealistic.csv"), index=False
    )
    save_feature_importances(
        model,
        feature_cols,
        os.path.join(args.outdir, "feature_importances_ultrarealistic_summary.csv"),
    )
    print("Saved evaluation outputs to", args.outdir)
