#!/usr/bin/env python3
"""
load_data.py

Utilities to load raw JSON logs from data/raw.
Provides functions to:
 - load all raw jsons into a list/dict
 - create a simple DataFrame view
 - read per-task files

Usage:
    python load_data.py --raw-dir ../../data/raw --list
"""

import argparse
import json
import os
from pathlib import Path
from typing import Any, Dict, List

import pandas as pd


def list_raw_files(raw_dir: str):
    raw_dir = Path(raw_dir)
    files = []
    for root, _, filenames in os.walk(raw_dir):
        for f in filenames:
            if f.endswith(".json"):
                files.append(os.path.join(root, f))
    return sorted(files)


def load_json_file(path: str) -> Dict:
    """Load a single JSON file and return the parsed object.

    Parameters
    - path: str -- path to a JSON file

    Returns
    - dict: parsed JSON content
    """

    with open(path, "r") as f:
        return json.load(f)


def load_all_raw(raw_dir: str) -> List[Dict]:
    """Load all JSON files found under `raw_dir`.

    Parameters
    - raw_dir: str -- root directory to recurse for JSON files

    Returns
    - list[dict]: list of parsed JSON objects, each annotated with `_source_file` path
    """
    files = list_raw_files(raw_dir)
    data = []
    for p in files:
        try:
            item = load_json_file(p)
            item["_source_file"] = p
            data.append(item)
        except Exception as e:
            print(f"Warning: failed reading {p}: {e}")
    return data


def to_dataframe(raw_objects: List[Dict]) -> pd.DataFrame:
    """
    Convert list of raw objects into a DataFrame with columns:
    participantId, task (or task_id), raw_tlx (if present), computed_metrics (dict) and source file.
    """
    rows = []
    for obj in raw_objects:
        row = {
            "participantId": obj.get("participantId"),
            "task": obj.get("task") or obj.get("task_id"),
            "raw_tlx": obj.get("raw_tlx")
            or (obj.get("tlx_scores") and obj["tlx_scores"].get("raw_tlx")),
            "computed_metrics": obj.get("computed_metrics"),
            "_source_file": obj.get("_source_file"),
        }
        rows.append(row)
    return pd.DataFrame(rows)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--raw-dir",
        type=str,
        default="../../data/raw",
        help="Path to raw JSON folder (root)",
    )
    parser.add_argument(
        "--out-csv",
        type=str,
        default=None,
        help="Optionally write a summary CSV listing all raw files",
    )
    args = parser.parse_args()

    files = list_raw_files(args.raw_dir)
    print(f"Found {len(files)} json files under {args.raw_dir}")
    data = load_all_raw(args.raw_dir)
    df = to_dataframe(data)
    print(df.head(10).to_string(index=False))

    if args.out_csv:
        df.to_csv(args.out_csv, index=False)
        print("Wrote summary CSV:", args.out_csv)


if __name__ == "__main__":
    main()
