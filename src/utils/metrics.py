#!/usr/bin/env python3
"""
metrics.py
Common ML metrics used across LOUO, baselines, and interpretation.

Functions:
 - compute_fold_metrics
 - aggregate_metrics
 - collect_misclassifications
"""

import numpy as np
from sklearn.metrics import (
    accuracy_score,
    f1_score,
    precision_score,
    recall_score,
    roc_auc_score,
)

# ------------------------------------------------------------------
# Fold-level metrics
# ------------------------------------------------------------------


def compute_fold_metrics(y_true, y_pred, y_score=None):
    """Compute metrics for a single fold, safely handling edge cases."""
    m = {}
    m["accuracy"] = float(accuracy_score(y_true, y_pred))
    m["precision_pos"] = float(precision_score(y_true, y_pred, zero_division=0))
    m["recall_pos"] = float(recall_score(y_true, y_pred, zero_division=0))
    m["f1_pos"] = float(f1_score(y_true, y_pred, zero_division=0))

    # ROC AUC only valid if both classes appear
    if y_score is not None and len(np.unique(y_true)) > 1:
        try:
            m["roc_auc"] = float(roc_auc_score(y_true, y_score))
        except:
            m["roc_auc"] = float("nan")
    else:
        m["roc_auc"] = float("nan")

    return m


# ------------------------------------------------------------------
# Aggregation
# ------------------------------------------------------------------


def aggregate_metrics(fold_df):
    """Return {metric_name: value} for mean ± std across folds."""
    summary = {}
    for col in ["accuracy", "precision_pos", "recall_pos", "f1_pos", "roc_auc"]:
        if col in fold_df:
            summary[col] = {
                "mean": float(fold_df[col].mean()),
                "std": float(fold_df[col].std()),
            }
    return summary


# ------------------------------------------------------------------
# Misclassification tracking
# ------------------------------------------------------------------


def collect_misclassifications(y_true, y_pred, fold_id, left_out_id):
    """Return list of misclassified sample info."""
    records = []
    for i, (yt, yp) in enumerate(zip(y_true, y_pred)):
        if int(yt) != int(yp):
            records.append(
                {
                    "fold": fold_id,
                    "left_out": left_out_id,
                    "true": int(yt),
                    "pred": int(yp),
                    "index": i,
                }
            )
    return records
