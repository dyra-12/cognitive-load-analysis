#!/usr/bin/env python3
"""
io_utils.py
Central utilities for loading/saving data and files.
Keeps I/O consistent across the entire pipeline.

Used by:
 - data_preparation
 - modeling
 - interpretation
"""

import json
import os
from pathlib import Path

import pandas as pd

# ------------------------------------------------------------------
# Directory helpers
# ------------------------------------------------------------------


def ensure_dir(path: str):
    """Create directory if it doesn't exist."""
    p = Path(path)
    p.mkdir(parents=True, exist_ok=True)
    return str(p)


# ------------------------------------------------------------------
# JSON helpers
# ------------------------------------------------------------------


def read_json(path: str):
    """Safe JSON loader."""
    with open(path, "r") as f:
        return json.load(f)


def write_json(path: str, obj, indent=2):
    """Write Python object to JSON file, creating parent directory if needed.

    Parameters
    - path: str -- output file path
    - obj: any -- serializable Python object
    - indent: int -- JSON indentation
    """
    ensure_dir(os.path.dirname(path))
    with open(path, "w") as f:
        json.dump(obj, f, indent=indent)


# ------------------------------------------------------------------
# DataFrame helpers
# ------------------------------------------------------------------


def save_df(df: pd.DataFrame, path: str):
    """Save DataFrame to CSV, ensuring directory exists."""
    ensure_dir(os.path.dirname(path))
    df.to_csv(path, index=False)
    return path


def load_modeling_csv(path: str):
    """Load modeling dataset + basic checks."""
    df = pd.read_csv(path)
    if "participantId" not in df.columns:
        raise ValueError("modeling CSV missing 'participantId'")
    if "High_Load" not in df.columns:
        raise ValueError("modeling CSV missing 'High_Load'")
    return df


# ------------------------------------------------------------------
# Raw file discovery
# ------------------------------------------------------------------


def list_json_files(directory: str):
    """Recursively list all JSON files."""
    files = []
    for root, _, f in os.walk(directory):
        for x in f:
            if x.endswith(".json"):
                files.append(os.path.join(root, x))
    return sorted(files)


def load_all_json(directory: str):
    """Load all JSON files under a root directory."""
    file_list = list_json_files(directory)
    data = []
    for p in file_list:
        try:
            x = read_json(p)
            x["_source_file"] = p
            data.append(x)
        except Exception as e:
            print(f"WARNING: couldn't read {p}: {e}")
    return data
