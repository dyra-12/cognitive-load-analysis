# Results

This folder contains all outputs from machine learning experiments and model interpretation analyses. It includes trained model predictions, out-of-fold probability estimates, feature correlation summaries, SHAP values for explainability, and execution logs tracking model training performance across cross-validation folds.

## Structure

### 📊 Root Files
- `modeling_dataset_with_oof_probs.csv` - Dataset with out-of-fold prediction probabilities
- `feature_correlation_summary.csv` - Correlation matrix between features and TLX scores

### 🤖 `modeling/`
Model performance metrics and summaries:
- Feature importance rankings
- Cross-validation fold metrics
- Model comparison results
- Random forest performance summaries

### 🔍 `interpretation/`
Model explainability artifacts:
- `shap_values_pos.npy` - SHAP values for positive class
- `shap_clusters_assignments.csv` - Clustering of SHAP patterns
- `shap_cluster_centroids.json` - Cluster centroid coordinates
- `shap_metadata.json` - Metadata for SHAP analysis

### 📝 `logs/`
Training and execution logs:
- Model training progress
- Hyperparameter tuning results
- Error messages and warnings

## Quick Access

**Model metrics**: Check `modeling/` for performance summaries  
**Explainability**: View `interpretation/` for SHAP analysis outputs  
**Predictions**: Use `modeling_dataset_with_oof_probs.csv` for model predictions
