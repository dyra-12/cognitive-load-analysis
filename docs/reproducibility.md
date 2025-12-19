# Reproducibility Guide

**How to Reproduce All Data Processing, Modeling, and Analysis**

This document provides a step-by-step guide to fully reproduce the dataset, feature engineering, machine learning models, SHAP analysis, statistical tests, and figures presented in the project.

All steps assume the repository's root directory as the working directory.

---

## 1. Requirements

### 1.1 Python Version

Python 3.10+

### 1.2 Install Dependencies

For full reproducibility, we recommend using a virtual environment (e.g., `venv` or `conda`) before installing dependencies.

Run:
```bash
pip install -r requirements.txt
```

**Key packages include**:
- `pandas`, `numpy`
- `scikit-learn`
- `scipy` & `statsmodels` (ANOVA + post-hoc tests)
- `shap`
- `matplotlib` (primary plotting)
- `seaborn` (optional, for correlation heatmaps)
- `jupyter notebook`
- `tqdm`

### 1.3 Compute Requirements

All experiments were run on a standard laptop-class CPU; no GPU is required.

---

## 2. Data Locations

### Raw data
```
data/raw/
   nasa_tlx/
   task1_form/
   task2_product/
   task3_travel/
```

**Note:** Depending on ethics and consent constraints, raw interaction logs may not be publicly distributed. When unavailable, example schemas and processed feature tables are provided to enable full pipeline execution.

### Example schemas
```
data/examples/
```

### Processed datasets

(These will be generated when you run preprocessing)
```
data/processed/
   modeling_dataset.csv
   features.csv
```

---

## 3. Step-by-Step Reproducibility Pipeline

The full pipeline consists of:

1. Ingestion
2. Feature extraction
3. Statistical analysis
4. Model training (LOUO)
5. Model comparison
6. Interpretability (SHAP)
7. Figure generation

The project includes scripts for each stage, located under:
```
src/data_preparation/
src/modeling/
src/interpretation/
```

---

## 4. Data Preprocessing

### 4.1 Load Raw JSON → Unified Table

Run:
```bash
python src/data_preparation/load_data.py \
    --raw-dir data/raw \
    --out-csv data/processed/raw_flattened.csv
```

**This script**:
- Scans all raw JSON folders
- Harmonizes schemas
- Merges participant-level TLX and behavioral logs
- Outputs a flat table for feature extraction

### 4.2 Feature Engineering

Run:
```bash
python src/data_preparation/compute_features.py \
    --in-csv data/processed/raw_flattened.csv \
   --out-csv data/processed/modeling_dataset.csv
```

**This script**:
- Computes all engineered features (20+ behavioral metrics)
- Applies per-task normalization where needed
- Adds TLX, High_Load label, task IDs, participant IDs

---

## 5. Statistical Analysis (Phase 2)

### 5.1 Repeated-Measures ANOVA

To reproduce the TLX-based validation (Task1 < Task2 < Task3):
```bash
python analysis/run_anova.py
```

**Outputs**:
```
figures/TLX/tlx_hist_ultrarealistic.png
figures/TLX/taskwise_TLX_boxplot.png
analysis/ANOVA_results.txt
```

### 5.2 Correlation Analysis

To compute Pearson correlations:
```bash
python analysis/run_correlations.py
```

**Outputs**:
```
figures/correlations/feature_correlation_heatmap.png
docs/feature_correlation_summary.md
```

---

## 6. Machine Learning (Phase 3)

### 6.1 Train Leave-One-User-Out (LOUO) Random Forest

Run:
```bash
python src/modeling/train_louo_random_forest.py
```

**Outputs**:
```
results/modeling/rf_fold_metrics_ultrarealistic.csv
results/modeling/rf_summary_ultrarealistic.csv
results/modeling/feature_importances_ultrarealistic_summary.csv

figures/modeling/confusion_matrices_louo.png
figures/modeling/precision_recall_foldwise.png
figures/modeling/roc_curves.png
```

### 6.2 Hyperparameter Search

Run:
```bash
python src/modeling/hyperparameter_search.py
```

**Outputs**:
```
results/modeling/rf_best_params.json
results/modeling/model_comparison_ultrarealistic.csv
```

### 6.3 Baseline Models

Run:
```bash
python src/modeling/baselines.py
```

**Outputs**:
```
results/modeling/baseline_metrics.csv
```

---

## 7. SHAP Interpretability

### Full SHAP Analysis

Run:
```bash
python src/interpretation/shap_analysis.py
```

**Outputs**:
```
figures/shap/shap_summary_bar.png
figures/shap/shap_summary_beeswarm.png
figures/shap/shap_waterfall_idx_0.png
figures/shap/shap_waterfall_idx_10.png
figures/shap/shap_waterfall_idx_20.png

results/interpretation/shap_metadata.json
results/interpretation/shap_values_pos.npy
```

### SHAP Clustering

Run:
```bash
python src/interpretation/shap_clustering.py
```

**Outputs**:
```
figures/shap/shap_clusters_pca.png
results/interpretation/shap_clusters_assignments.csv
results/interpretation/shap_cluster_centroids.json
```

---

## 8. Figure Regeneration

To regenerate all visualizations:
```bash
python run_all.py
```

This script sequentially executes the full pipeline from raw data ingestion through figure generation.

---

## 9. Jupyter Notebooks

The following notebooks reproduce analyses interactively:
```
notebooks/
   ANOVA_and_correlations.ipynb
   SHAP_visualization.ipynb
   ML_modeling_walkthrough.ipynb
```

Open with:
```bash
jupyter notebook
```

---

## 10. Reproducibility Checklist

| Component | Reproducible? | How |
|-----------|---------------|-----|
| Dataset generation | ✔️ | `load_data.py` + `compute_features.py` |
| Feature engineering | ✔️ | `compute_features.py` |
| ANOVA / correlations | ✔️ | analysis scripts |
| ML modeling (LOUO) | ✔️ | `train_louo_random_forest.py` |
| Hyperparameter search | ✔️ | `hyperparameter_search.py` |
| Baselines | ✔️ | `baselines.py` |
| SHAP global & local | ✔️ | `shap_analysis.py` |
| SHAP clustering | ✔️ | `shap_clustering.py` |
| Adaptive UI examples | Semi | UI logic reproducible; demo interactions illustrative |
| All figures | ✔️ | `run_all.py` |

---

## 11. Notes on Randomness

- All models use **fixed random seeds** for repeatability
- SHAP clustering uses deterministic PCA + k-means (seeded)
- Participant IDs are stable and deterministic

---

## 12. Contact

For reproducibility-related questions, please open a GitHub Issue.

---

**Last Updated**: December 2025  
**Version**: 1.0