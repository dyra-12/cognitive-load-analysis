# Reproducibility Guide

This document describes how to reproduce the main CogniViz results (feature generation, modeling, and interpretability artifacts) from a clean environment.

## 1) System Requirements

- macOS / Linux / Windows
- Python 3.10+ (recommended)
- Enough RAM for SHAP computations (small dataset, but SHAP can be memory-intensive)

## 2) Environment Setup

From the repository root:

```bash
python -m venv .venv
source .venv/bin/activate  # macOS/Linux
# .venv\Scripts\activate   # Windows PowerShell

python -m pip install --upgrade pip
```

### Install Python dependencies

This repository does not currently ship a pinned `requirements.txt`. Install the core packages used by the pipeline:

```bash
python -m pip install \
  numpy pandas \
  scikit-learn joblib \
  matplotlib seaborn \
  shap \
  scipy statsmodels
```

If you plan to run notebooks:

```bash
python -m pip install jupyter ipykernel
python -m ipykernel install --user --name cogniviz --display-name "CogniViz (.venv)"
```

## 3) Data Inputs

CogniViz supports two common modes:

1. **Synthetic / demo reproduction** (recommended for reviewers): the pipeline can generate synthetic modeling data and “raw-matching” JSONs and then recompute features from those.
2. **Real dataset reproduction** (if you have access): place raw files under `data/raw/` and ensure the processed CSV exists under `data/processed/`.

The dataset format and feature definitions are documented in:

- `docs/DATA.md`

## 4) End-to-End Pipeline (Model + SHAP)

Run the full pipeline:

```bash
python run_all.py
```

Notes:

- By default, `run_all.py` generates synthetic data for `--n-participants 25` and writes `data/processed/modeling_dataset.csv`.
- It then trains/evaluates models with Leave-One-User-Out (LOUO), generates SHAP artifacts, and saves results under `results/`.

Optional flags (see `python run_all.py --help`):

- `--do-search` to run the grouped hyperparameter search before training.
- `--skip-generate` to skip synthetic generation (useful if you already have `data/processed/modeling_dataset.csv`).
- `--skip-compute` to skip recomputing features from raw.

## 5) Statistical Analyses (NASA-TLX)

The ANOVA and correlation scripts live under `analysis/statistics/`.

Typical runs:

```bash
python analysis/statistics/run_anova.py
python analysis/statistics/run_correlations.py
```

Outputs are written into `analysis/results/` (see the `analysis/results/` folder for example outputs).

## 6) Expected Outputs

After a successful end-to-end run (`python run_all.py`), you should see:

- `data/processed/modeling_dataset.csv`
- `models/tuned_random_forest_model.joblib`
- `results/modeling/` (metrics, fold summaries)
- `results/interpretation/` (SHAP arrays, plots, cluster assignments)
- `logs/run_all.log`

## 7) Reproducibility Notes (Determinism)

- Most scripts set or rely on scikit-learn randomness. For fully deterministic reruns, ensure that `random_state` is set consistently across training and clustering steps.
- Some operations (parallelism, BLAS) can introduce small numerical differences across machines/OS.

## 8) Troubleshooting

- **`ModuleNotFoundError`**: install the missing package in the active `.venv`.
- **SHAP is slow**: reduce complexity (e.g., smaller model or fewer background samples) or run on a faster machine.
- **Notebook kernel mismatch**: ensure the notebook uses the `CogniViz (.venv)` kernel.

## 9) What This Repo Produces

- Modeling dataset: one row per participant-task instance with behavioral features + TLX label
- LOUO evaluation summaries
- Interpretable model artifacts (feature importances and SHAP explanations)

For the broader study context and design, see `docs/experiments.md` and `docs/SYSTEM.md`.
