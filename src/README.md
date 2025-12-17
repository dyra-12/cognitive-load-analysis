# Source Code

This folder contains the complete machine learning pipeline for cognitive load prediction. It includes modules for data preparation and feature extraction from behavioral logs, model training using Leave-One-User-Out cross-validation, baseline comparisons, and model interpretation through SHAP analysis. The codebase supports reproducible experiments for predicting user cognitive load from interaction patterns.

## Structure

### 📥 `data_preparation/`
Data loading and feature engineering:
- `load_data.py` - Load raw NASA-TLX and behavioral data
- `compute_features.py` - Extract interaction features from behavioral logs

### 🤖 `modeling/`
Machine learning model training and evaluation:
- `train_louo_random_forest.py` - Leave-One-User-Out cross-validation
- `baselines.py` - Baseline model implementations
- `hyperparameter_search.py` - Hyperparameter tuning
- `evaluate_model.py` - Model performance evaluation

### 🔍 `interpretation/`
Model explainability and feature analysis:
- `feature_importance.py` - Feature importance extraction
- `shap_analysis.py` - SHAP value computation and visualization
- `shap_clustering.py` - Cluster SHAP patterns

### 🛠️ `utils/`
Utility functions:
- `io_utils.py` - File I/O operations
- `metrics.py` - Evaluation metrics
- `plot_utils.py` - Visualization helpers

## Usage

Import modules as needed:
```python
from src.data_preparation import load_data, compute_features
from src.modeling import train_louo_random_forest
from src.interpretation import shap_analysis
```
