#!/usr/bin/env python3
"""
run_all.py

Orchestrator to run the complete pipeline end-to-end.

Steps:
 1. generate_synthetic_data.py  (--raw-matching)
 2. compute_features.py         (recreate modeling CSV from raw matching)
 3. baselines.py                (majority + logistic under LOUO)
 4. hyperparameter_search.py    (optional; Leave-One-Group-Out grid search)
 5. train_louo_random_forest.py (train final RF and evaluate under LOUO)
 6. shap_analysis.py            (compute and save SHAP plots / arrays)
 7. shap_clustering.py          (cluster SHAP vectors, save labels + PCA)
 8. feature_importance.py       (save RF importances + plot)

This script calls the individual scripts as subprocesses to keep them isolated.

Author: Generated for your project.
"""

import os
import subprocess
import argparse
import datetime
from pathlib import Path
import sys
import logging

# -------------------------
# Defaults / paths
# -------------------------
REPO_ROOT = Path(__file__).resolve().parent
SRC_DIR = REPO_ROOT / "src"
DATA_DIR = REPO_ROOT / "data"
RAW_MATCH_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"
MODELS_DIR = REPO_ROOT / "models"
RESULTS_DIR = REPO_ROOT / "results"
INTERP_RESULTS_DIR = RESULTS_DIR / "interpretation"
LOGS_DIR = REPO_ROOT / "logs"

# Script paths
GEN_SCRIPT = SRC_DIR / "data_preparation" / "generate_synthetic_data.py"
COMPUTE_SCRIPT = SRC_DIR / "data_preparation" / "compute_features.py"
BASELINE_SCRIPT = SRC_DIR / "modeling" / "baselines.py"
HYPER_SCRIPT = SRC_DIR / "modeling" / "hyperparameter_search.py"
TRAIN_SCRIPT = SRC_DIR / "modeling" / "train_louo_random_forest.py"
SHAP_ANALYSIS = SRC_DIR / "interpretation" / "shap_analysis.py"
SHAP_CLUSTER = SRC_DIR / "interpretation" / "shap_clustering.py"
FI_SCRIPT = SRC_DIR / "interpretation" / "feature_importance.py"

# Files
MODELING_CSV = PROCESSED_DIR / "modeling_dataset.csv"
GRID_OUT = MODELS_DIR / "rf_grid_search.joblib"
MODEL_OUT = MODELS_DIR / "tuned_random_forest_model.joblib"

# -------------------------
# Logging
# -------------------------
LOGS_DIR.mkdir(parents=True, exist_ok=True)
logging.basicConfig(
    filename=LOGS_DIR / "run_all.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
console = logging.StreamHandler()
console.setLevel(logging.INFO)
formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s", "%H:%M:%S")
console.setFormatter(formatter)
logging.getLogger().addHandler(console)


def run_cmd(cmd, cwd=None, env=None, fail_ok=False):
    """
    Run a command (list) with subprocess.run, stream output to log and console.
    If fail_ok is False, raises on non-zero exit.
    """
    logging.info("RUN: %s", " ".join(map(str, cmd)))
    try:
        proc = subprocess.run(cmd, cwd=cwd or str(REPO_ROOT), env=env, check=not fail_ok, capture_output=True, text=True)
        logging.info("Return code: %s", proc.returncode)
        if proc.stdout:
            logging.info("STDOUT:\n%s", proc.stdout.strip())
        if proc.stderr:
            logging.info("STDERR:\n%s", proc.stderr.strip())
        return proc
    except subprocess.CalledProcessError as e:
        logging.error("Command failed (code %s). Stdout:\n%s\nStderr:\n%s", e.returncode, e.stdout, e.stderr)
        if not fail_ok:
            raise
        return e


def ensure_dirs():
    for d in [DATA_DIR, RAW_MATCH_DIR, PROCESSED_DIR, MODELS_DIR, RESULTS_DIR, INTERP_RESULTS_DIR, LOGS_DIR]:
        Path(d).mkdir(parents=True, exist_ok=True)


def main(args):
    ensure_dirs()

    py = sys.executable  # use same python executable

    # 1) Generate synthetic data (CSV + raw matching)
    if not args.skip_generate:
        logging.info("STEP 1: Generating synthetic modeling CSV and raw-matching JSONs")
        cmd = [
            py,
            str(GEN_SCRIPT),
            "--out-csv", str(MODELING_CSV),
            "--n-participants", str(args.n_participants),
            "--raw-matching"
        ]
        run_cmd(cmd)
    else:
        logging.info("Skipping data generation (user requested).")

    # 2) Compute features from raw (sanity check / recompute modeling CSV from raw)
    if not args.skip_compute:
        logging.info("STEP 2: Running compute_features to regenerate modeling CSV from raw data (sanity check)")
        cmd = [
            py,
            str(COMPUTE_SCRIPT),
            "--raw-dir", str(RAW_MATCH_DIR),
            "--out-csv", str(MODELING_CSV)
        ]
        run_cmd(cmd)
    else:
        logging.info("Skipping compute_features (user requested).")

    # 3) Baselines
    if not args.skip_baselines:
        logging.info("STEP 3: Running baselines (majority + logistic) under LOUO")
        cmd = [
            py,
            str(BASELINE_SCRIPT),
            "--csv", str(MODELING_CSV),
            "--outdir", str(RESULTS_DIR / "modeling")
        ]
        run_cmd(cmd)
    else:
        logging.info("Skipping baseline evaluation.")

    # 4) Hyperparameter search (optional)
    if args.do_search:
        logging.info("STEP 4: Running grouped hyperparameter search (Leave-One-Group-Out)")
        cmd = [
            py,
            str(HYPER_SCRIPT),
            "--csv", str(MODELING_CSV),
            "--out", str(GRID_OUT),
            "--n-jobs", str(args.n_jobs)
        ]
        run_cmd(cmd)
    else:
        logging.info("Skipping hyperparameter search (user requested).")

    # 5) Train RF + LOUO evaluation
    logging.info("STEP 5: Train RandomForest and evaluate with LOUO")
    cmd = [
        py,
        str(TRAIN_SCRIPT),
        "--csv", str(MODELING_CSV),
        "--model-out", str(MODEL_OUT),
        "--results-outdir", str(RESULTS_DIR / "modeling")
    ]
    if args.do_search:
        cmd += ["--do-search", "--grid-out", str(GRID_OUT), "--n-jobs", str(args.n_jobs)]
    run_cmd(cmd)

    # 6) SHAP analysis
    logging.info("STEP 6: SHAP analysis (summary bar + beeswarm)")
    cmd = [
        py,
        str(SHAP_ANALYSIS),
        "--model", str(MODEL_OUT),
        "--csv", str(MODELING_CSV),
        "--outdir", str(INTERP_RESULTS_DIR)
    ]
    run_cmd(cmd)

    # 7) SHAP clustering
    logging.info("STEP 7: SHAP clustering (k=2) + PCA plot")
    cmd = [
        py,
        str(SHAP_CLUSTER),
        "--shap-values", str(INTERP_RESULTS_DIR / "shap_values.npy"),
        "--features", str(INTERP_RESULTS_DIR / "shap_feature_names.json"),
        "--csv", str(MODELING_CSV),
        "--outdir", str(INTERP_RESULTS_DIR)
    ]
    run_cmd(cmd)

    # 8) Feature importances & plot
    logging.info("STEP 8: Feature importances (bar plot + csv)")
    cmd = [
        py,
        str(FI_SCRIPT),
        "--model", str(MODEL_OUT),
        "--csv", str(MODELING_CSV),
        "--outdir", str(INTERP_RESULTS_DIR)
    ]
    run_cmd(cmd)

    logging.info("Pipeline finished successfully. Results saved under: %s", RESULTS_DIR)
    print("\nAll steps complete. Check logs at:", LOGS_DIR / "run_all.log")
    print("Key outputs:")
    print(" - Modeling CSV:", MODELING_CSV)
    print(" - Model:", MODEL_OUT)
    print(" - Results folder:", RESULTS_DIR)
    print(" - Interpretation results:", INTERP_RESULTS_DIR)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run the full pipeline end-to-end.")
    parser.add_argument("--n-participants", type=int, default=25, help="Number of synthetic participants to create")
    parser.add_argument("--do-search", action="store_true", help="Run grouped hyperparameter search before training")
    parser.add_argument("--n-jobs", type=int, default=1, help="Parallel jobs for grid search")
    parser.add_argument("--skip-generate", dest="skip_generate", action="store_true", help="Skip synthetic data generation")
    parser.add_argument("--skip-compute", dest="skip_compute", action="store_true", help="Skip feature computation step")
    parser.add_argument("--skip-baselines", dest="skip_baselines", action="store_true", help="Skip baseline evaluation")
    parser.add_argument("--no-search", dest="do_search", action="store_false", help="Alias to skip search")
    args = parser.parse_args()

    try:
        main(args)
    except Exception as e:
        logging.exception("Pipeline failed: %s", e)
        print("Pipeline failed. See logs:", LOGS_DIR / "run_all.log")
        raise
