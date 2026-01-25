# CogniViz Model Documentation

## Overview

This document describes the machine learning architecture underlying CogniViz, a browser-native, sensor-free framework for real-time cognitive load inference from natural interaction behavior. It details:

- Feature representation  
- Target operationalization  
- Model selection rationale  
- Training and validation protocol  
- Hyperparameter optimization  
- Error characteristics  
- SHAP-based explainability internals  

The design prioritizes participant-independent generalization, interpretability, real-time feasibility, and cognitive grounding.

---

## 1. Problem Formulation

CogniViz frames cognitive load inference as a supervised binary classification task.

### 1.1 Input Representation

Each instance corresponds to a single participant–task session and is represented as a fixed-length feature vector of **16 primary behavioral metrics**:

- Temporal features (hesitation, idle time, planning time)  
- Decision complexity features (scheduling difficulty, budget stress)  
- Constraint-related features (constraint violation rate)  
- Multitasking features  
- Motor variability features (mouse entropy)  
- Error recovery features  

All features are derived from browser interaction telemetry.

---

### 1.2 Target Variable

Cognitive load is operationalized using subjective workload ratings from NASA-TLX.

- **High Load:** NASA-TLX > 60  
- **Low Load:** NASA-TLX ≤ 60  

This threshold reflects a widely adopted separation between moderate and elevated subjective workload.

The resulting label distribution exhibits moderate imbalance.

---

## 2. Model Selection Rationale

Three models of increasing complexity were evaluated:

1. **Majority-Class Baseline**  
   - Establishes a lower bound under class imbalance  

2. **Logistic Regression**  
   - Tests linear separability of cognitive load signatures  
   - Supports coefficient-based interpretability  
   - Acts as a simple discriminative benchmark  

3. **Random Forest (Tuned)**  
   - Captures nonlinear interactions among behavioral features  
   - Robust to feature scaling  
   - Supports SHAP-based explanation  
   - Suitable for real-time inference  

The Random Forest was selected as the primary deployment model due to:

- Superior participant-independent performance  
- Strong generalization under Leave-One-User-Out validation  
- Compatibility with TreeSHAP  
- Low inference latency  
- Resistance to overfitting under constrained data  

---

## 3. Feature Preprocessing

### 3.1 Normalization

Feature normalization is applied server-side using statistics computed from the training set.

- StandardScaler for Logistic Regression  
- No scaling required for Random Forest  

All normalization parameters are computed per fold to prevent leakage.

---

### 3.2 Leakage Prevention

- No participant appears in both training and test sets within a fold  
- No feature statistics computed on test data  
- Hyperparameters tuned exclusively on training splits  

---

## 4. Validation Protocol

### 4.1 Leave-One-User-Out (LOUO)

To evaluate participant-independent generalization:

- In each fold:
  - Train on 24 participants  
  - Test on the remaining participant  
- Total folds: 25  

This mirrors real-world deployment conditions for adaptive interfaces.

---

### 4.2 Class Imbalance Handling

- Class weights set to `balanced` for Logistic Regression  
- Class weights set to `balanced` for Random Forest  
- F1-score used as primary metric  

---

## 5. Hyperparameter Optimization

### 5.1 Random Forest Grid Search

Hyperparameters were optimized using grid search within each training fold.

**Key parameters:**

- `n_estimators`: ~300  
- `max_depth`: ~10  
- `min_samples_split`: 2  
- `min_samples_leaf`: 1  
- `max_features`: "sqrt"  
- `class_weight`: "balanced"  
- `bootstrap`: True  

Grid search optimized for F1-score.

---

## 6. Training Procedure

For each LOUO fold:

1. Split data into training and test sets  
2. Compute normalization statistics on training data  
3. Apply normalization  
4. Run grid search for Random Forest  
5. Train final model using optimal hyperparameters  
6. Evaluate on held-out participant  
7. Store predictions and SHAP explanations  

Models are trained independently per fold.

---

## 7. Performance Summary

| Model                | Accuracy | Precision | Recall | F1   | ROC-AUC |
|----------------------|----------|-----------|--------|------|---------|
| Majority Baseline    | 0.73     | 0.05      | 0.02   | 0.03 | 0.50    |
| Logistic Regression  | 0.92     | 0.68      | 0.72   | 0.69 | 0.84    |
| Random Forest        | 0.96     | 0.88      | 0.86   | 0.87 | 0.95    |

The Random Forest demonstrates robust nonlinear modeling of cognitive load signals.

---

## 8. Error Characteristics

Misclassifications are concentrated near borderline NASA-TLX values (≈55–62).

Two systematic error modes:

### 8.1 Under-Reporters

- Behavioral strain present  
- Low subjective TLX  
- Model predicts high load  

### 8.2 Over-Reporters

- High subjective TLX  
- Efficient interaction behavior  
- Model predicts low load  

These discrepancies reflect inherent noise in subjective workload labels.

---

## 9. SHAP Explainability Internals

Interpretability is a first-class modeling requirement.

CogniViz uses **TreeSHAP** to generate exact, fast, and consistent feature attributions for Random Forest predictions.

---

### 9.1 SHAP Objective

SHAP quantifies:

- The marginal contribution of each feature  
- To the predicted probability of high cognitive load  
- Conditioned on the presence of all other features  

This ensures additive completeness:

$$
f(x) = \phi_0 + \sum_{i=1}^{N} \phi_i
$$

Where:

- $f(x)$ is the model prediction  
- $\phi_0$ is the base value  
- $\phi_i$ is the SHAP value of feature $i$  

---

### 9.2 TreeSHAP Implementation

CogniViz uses TreeSHAP for:

- Exact Shapley values for tree ensembles  
- Linear-time complexity per tree  
- Deterministic explanations  

The explainer is initialized with:

- The trained Random Forest model  
- A background dataset sampled from training data  

---

### 9.3 Global Explanations

Global SHAP is computed as:

- Mean absolute SHAP value per feature  
- Aggregated across all task instances  

This yields a ranking of marginal predictive influence.

---

### 9.4 Local Explanations

For each inference instance:

- SHAP values are computed for all 16 features  
- The explanation vector is returned alongside predictions  
- Feature contributions sum to the predicted log-odds  

Local explanations support:

- Instance-level interpretability  
- Explanation-driven adaptation logic  
- Behavioral diagnosis  

---

### 9.5 SHAP and Correlation Divergence

SHAP does not measure correlation.

It measures:

- Conditional marginal contribution  
- Given correlated features  

This explains why:

- Some features with high Pearson correlation  
- Have lower SHAP influence  
- Due to shared variance  

---

## 10. Explanation-Based Clustering

To discover recurring explanation patterns:

1. Extract SHAP vectors for the high-load class  
2. Apply PCA for dimensionality reduction  
3. Perform K-means clustering (k = 2)  

This reveals:

- Distinct explanation profiles  
- Through which cognitive load manifests  

---

## 11. Real-Time SHAP Optimization

To support real-time inference:

- Background distributions are cached  
- Feature dimensionality is restricted  
- SHAP is computed server-side  
- Only required attributions are generated  

This yields:

- SHAP latency: < 20 ms  
- End-to-end inference latency: 150–400 ms  

---

## 12. Model Design Principles

The modeling stack reflects four guiding principles:

1. **Behavior over physiology**  
2. **Generalization over personalization**  
3. **Interpretability over opacity**  
4. **Real-time feasibility over maximal complexity**  
 
---

## 13. Summary

The CogniViz model demonstrates that cognitive load can be inferred from natural interaction behavior alone using a nonlinear, interpretable machine learning architecture. By integrating TreeSHAP explanations directly into the inference pipeline, CogniViz treats interpretability as infrastructure rather than a post-hoc diagnostic, enabling explanation-driven adaptive interface behavior in real time.

