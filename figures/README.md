# Figures

This folder contains all visualization outputs from statistical analyses, machine learning experiments, and model interpretation. Figures include model performance plots, SHAP explainability visualizations, and NASA-TLX score distributions used throughout the research documentation and presentations.

## Structure

### 🤖 `modeling/`
Model performance visualizations:
- `confusion_matrices_louo.png` - Confusion matrices for Leave-One-User-Out CV
- `model_comparison.png` - Performance comparison across models
- `roc_curves.png` - ROC curves for classification
- `precision_recall_foldwise.png` - Precision-recall across folds

### 🔍 `shap/`
SHAP explainability visualizations:
- `shap_summary_beeswarm.png` - Feature impact summary (beeswarm plot)
- `shap_summary_bar.png` - Mean absolute SHAP values
- `shap_clusters_pca.png` - PCA visualization of SHAP clusters
- `shap_waterfall_idx_*.png` - Individual prediction explanations
- `shap_force_idx_0.html` - Interactive force plot

### 📊 `TLX/`
NASA-TLX analysis visualizations:
- `tlx_hist_ultrarealistic.png` - Distribution of TLX scores
- `tlx_vs_pred_prob.png` - Predicted probability vs actual TLX scores

## Usage

Reference these figures in documentation, presentations, or reports. All plots are publication-ready with appropriate labels and legends.
