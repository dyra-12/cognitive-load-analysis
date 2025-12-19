#!/usr/bin/env python3
"""
compute_features.py

Feature extraction pipeline that reads raw JSON logs from `data/raw/` (or a raw-matching folder)
and produces the modeling CSV with engineered features. If the raw JSON contains a
`computed_metrics` block, those values are used directly (perfect-reconstruction mode).
Otherwise, the script computes features from events.

Outputs:
 - ./data/processed/modeling_dataset.csv

Usage:
    python compute_features.py --raw-dir ../../data/raw --out-csv ../../data/processed/modeling_dataset.csv
"""

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict

import numpy as np
import pandas as pd
from load_data import load_all_raw, to_dataframe  # relative import in package usage

REQUIRED_FEATURES = [
    "form_hesitation_index",
    "form_error_rate",
    "form_efficiency",
    "zip_code_struggle",
    "filter_optimization_score",
    "decision_uncertainty",
    "exploration_breadth",
    "planning_time_ratio",
    "multitasking_load",
    "constraint_violation_rate",
    "budget_management_stress",
    "scheduling_difficulty",
    "recovery_efficiency",
    "action_density",
    "idle_time_ratio",
    "mouse_entropy_avg",
]


def compute_features_from_raw(obj: Dict[str, Any]) -> Dict[str, Any]:
    """
    Compute engineered features from a single raw JSON object.
    If `computed_metrics` exists, return that block directly (perfect reconstruction).
    Otherwise compute approximations from available fields.
    """
    if "computed_metrics" in obj and obj["computed_metrics"] is not None:
        # Use copy to avoid mutation issues
        cm = dict(obj["computed_metrics"])
        # ensure keys exist
        for k in REQUIRED_FEATURES:
            if k not in cm:
                cm[k] = None
        return cm

    task = obj.get("task") or obj.get("task_id")
    cm = {k: None for k in REQUIRED_FEATURES}

    # Basic heuristics: safe fallbacks if some logs are missing
    # Task 1: form metrics
    if task and "form" in task:
        # field_interactions => form_hesitation_index (sum focus_time_ms)
        fields = obj.get("field_interactions") or []
        cm["form_hesitation_index"] = float(
            sum([fi.get("focus_time_ms", 0) for fi in fields])
        )
        # error rate approximated from summary or backspace counts
        cm["form_error_rate"] = float(
            obj.get("summary_metrics", {}).get("error_count", 0)
        ) / max(1, (cm["form_hesitation_index"] or 1))
        cm["form_efficiency"] = float(
            obj.get("summary_metrics", {}).get("total_time_ms", 1)
        ) / max(1, len(fields))
        cm["zip_code_struggle"] = float(
            obj.get("task_specific_metrics", {}).get("zip_code_corrections", 0)
        )
        # action density & mouse entropy
        mouse_path = obj.get("mouse_path") or obj.get("mouse_data") or []
        cm["action_density"] = float(len(mouse_path)) / max(
            1, (obj.get("summary_metrics", {}).get("total_time_ms", 1000))
        )
        cm["mouse_entropy_avg"] = float(
            np.std([p.get("x", 0) for p in mouse_path]) + 1e-6
        )
        # fill other defaults
        cm["filter_optimization_score"] = None
        cm["decision_uncertainty"] = None
        cm["exploration_breadth"] = None
        cm["planning_time_ratio"] = None
        cm["multitasking_load"] = 0.0
        cm["constraint_violation_rate"] = 0.0
        cm["budget_management_stress"] = 0.0
        cm["scheduling_difficulty"] = 0.0
        cm["recovery_efficiency"] = (
            obj.get("summary_metrics", {}).get("success", True) and 1.0 or 0.0
        )
        cm["idle_time_ratio"] = float(
            sum([p.get("duration_ms", 0) for p in (obj.get("idle_periods") or [])])
        ) / max(1, obj.get("summary_metrics", {}).get("total_time_ms", 1))
        return cm

    # Task 2: product metrics
    if task and "product" in task:
        prod = obj.get("product_exploration", {})
        viewed = prod.get("products_viewed", [])
        cm["exploration_breadth"] = float(len(viewed))
        cm["decision_uncertainty"] = float(
            obj.get("product_exploration", {}).get("rapid_hover_switches", 0)
        )
        cm["filter_optimization_score"] = (
            float(
                obj.get("filter_interactions", [{}])[0].get("value_after", 0)
                and 0.8
                or 0.6
            )
            if obj.get("filter_interactions")
            else 0.8
        )
        cm["planning_time_ratio"] = (
            float(obj.get("summary_metrics", {}).get("total_time_ms", 0))
            and 0.02
            or 0.0
        )
        mouse_path = obj.get("mouse_path") or []
        cm["mouse_entropy_avg"] = float(
            np.std([p.get("x", 0) for p in mouse_path]) + 1e-6
        )
        cm["action_density"] = float(len(mouse_path)) / max(
            1, obj.get("summary_metrics", {}).get("total_time_ms", 1)
        )
        # default others
        cm["form_hesitation_index"] = 0.0
        cm["form_efficiency"] = 0.0
        cm["zip_code_struggle"] = 0.0
        cm["multitasking_load"] = float(
            obj.get("component_switches") and len(obj.get("component_switches")) or 0.0
        )
        cm["constraint_violation_rate"] = float(
            obj.get("constraint_violations")
            and len(obj.get("constraint_violations"))
            or 0.0
        )
        cm["budget_management_stress"] = float(
            obj.get("budget", {}).get("overrun_events", 0)
        )
        cm["scheduling_difficulty"] = float(
            obj.get("meetings", [{}])[0].get("drag_attempts", 0)
        )
        cm["recovery_efficiency"] = 1.0 - cm["decision_uncertainty"] / max(
            1, (cm["exploration_breadth"] or 1)
        )
        cm["idle_time_ratio"] = float(
            sum([p.get("duration_ms", 0) for p in (obj.get("idle_periods") or [])])
        ) / max(1, obj.get("summary_metrics", {}).get("total_time_ms", 1))
        return cm

    # Task 3: travel metrics
    if task and "travel" in task:
        cm["multitasking_load"] = float(len(obj.get("component_switches", [])))
        cm["constraint_violation_rate"] = float(
            len(obj.get("constraint_violations", []))
        ) / max(1, obj.get("summary_metrics", {}).get("total_time_ms", 1))
        cm["budget_management_stress"] = float(
            len(obj.get("budget", {}).get("updates", []))
        ) / max(1, (obj.get("summary_metrics", {}).get("total_time_ms", 1) / 1000))
        cm["scheduling_difficulty"] = float(
            obj.get("meetings", [{}])[0].get("drag_attempts", 0)
        )
        cm["recovery_efficiency"] = (
            float(obj.get("computed_metrics", {}).get("recovery_efficiency", 0.0))
            if "computed_metrics" in obj
            else 0.05
        )
        cm["action_density"] = float(len(obj.get("mouse_path", []))) / max(
            1, obj.get("summary_metrics", {}).get("total_time_ms", 1)
        )
        cm["mouse_entropy_avg"] = float(
            np.std([p.get("x", 0) for p in obj.get("mouse_path", [])]) + 1e-6
        )
        cm["idle_time_ratio"] = float(
            sum([p.get("duration_ms", 0) for p in obj.get("idle_periods", [])])
        ) / max(1, obj.get("summary_metrics", {}).get("total_time_ms", 1))
        # fill form/product defaults
        cm["form_hesitation_index"] = 0.0
        cm["form_error_rate"] = 0.0
        cm["form_efficiency"] = 0.0
        cm["zip_code_struggle"] = 0.0
        cm["filter_optimization_score"] = 0.0
        cm["decision_uncertainty"] = (
            float(obj.get("product_exploration", {}).get("rapid_hover_switches", 0))
            if obj.get("product_exploration")
            else 0.0
        )
        cm["exploration_breadth"] = (
            float(len(obj.get("product_exploration", {}).get("products_viewed", [])))
            if obj.get("product_exploration")
            else 0.0
        )
        cm["planning_time_ratio"] = 0.0
        return cm

    # fallback - empty defaults
    return {k: None for k in REQUIRED_FEATURES}


def build_modeling_dataframe(raw_dir: str):
    """Build the modeling DataFrame by computing features for all raw objects.

    Parameters
    - raw_dir: str -- directory with raw JSON files

    Returns
    - pandas.DataFrame: modeling dataset with engineered features and metadata
    """
    raw_objects = load_all_raw(raw_dir)
    rows = []
    for obj in raw_objects:
        # Skip TLX-only files in this pass
        if (obj.get("task") or "").lower().find("tlx") != -1:
            continue
        pid = obj.get("participantId")
        task = obj.get("task") or obj.get("task_id")
        tlx = obj.get("raw_tlx") or (
            obj.get("tlx_scores") and obj["tlx_scores"].get("raw_tlx")
        )
        feats = compute_features_from_raw(obj)
        row = {
            "participantId": pid,
            "task_id": task,
            "tlx": (
                float(tlx)
                if tlx is not None
                else (feats.get("raw_tlx") if "raw_tlx" in feats else None)
            ),
            "High_Load": int((float(tlx) if tlx is not None else 0) > 60),
        }
        for k in REQUIRED_FEATURES:
            row[k] = feats.get(k)
        rows.append(row)
    df = pd.DataFrame(rows)
    # Some basic cleaning/sanity
    # Convert empty strings and np.nan appropriately
    for c in REQUIRED_FEATURES:
        if c not in df.columns:
            df[c] = None
    return df


def main():
    """CLI entrypoint to build and save the modeling dataset CSV.

    This reads raw JSONs from `--raw-dir`, constructs features, and writes
    the resulting CSV to `--out-csv`.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw-dir",
        type=str,
        default="../../data/raw",
        help="Directory containing raw JSONs",
    )
    parser.add_argument(
        "--out-csv",
        type=str,
        default="../../data/processed/modeling_dataset.csv",
        help="Output CSV path",
    )
    args = parser.parse_args()

    raw_dir = os.path.abspath(args.raw_dir)
    out_csv = os.path.abspath(args.out_csv)
    Path(os.path.dirname(out_csv)).mkdir(parents=True, exist_ok=True)

    print("Loading raw files from:", raw_dir)
    df = build_modeling_dataframe(raw_dir)
    # If tlx missing, try to fetch from TLX folder
    # Basic fix: if idx missing tlx but nasa_tlx folder has values, join - left as exercise
    df.to_csv(out_csv, index=False)
    print("Saved processed modeling CSV to:", out_csv)
    print("Rows:", len(df))


if __name__ == "__main__":
    main()
