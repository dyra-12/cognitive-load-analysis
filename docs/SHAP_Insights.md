# 📘 SHAP Insights Report

Interpretability Analysis for Cognitive Load Modeling

---

## Table of Contents
- [Overview](#overview)
- [Objectives of the SHAP Analysis](#objectives-of-the-shap-analysis)
- [Global Explanations](#global-explanations)
	- [SHAP Summary Bar Plot](#shap-summary-bar-plot)
	- [SHAP Beeswarm Distribution](#shap-beeswarm-distribution)
- [Local Explanations](#local-explanations)
	- [Participant Waterfall Plots](#participant-waterfall-plots)
	- [Force Plot](#force-plot)
- [SHAP-Based Clustering](#shap-based-clustering)
	- [PCA Mapping](#pca-mapping)
	- [Cluster Characteristics](#cluster-characteristics)
	- [Cluster Centroids](#cluster-centroids)
- [Key Behavioral Predictors](#key-behavioral-predictors)
- [Theory-Driven Interpretation](#theory-driven-interpretation)
- [Implications for HCI & UX Design](#implications-for-hci--ux-design)
- [Limitations & Considerations](#limitations--considerations)
- [Conclusion](#conclusion)

---

## Overview

This document summarizes interpretability results from machine learning models that predict cognitive load using behavioral metrics. We use SHAP (SHapley Additive exPlanations) to provide:

- Transparent model reasoning at global and local levels
- Feature influence magnitudes and directions
- Individual-level behavioral signatures
- Emergent structure via explanation-based clustering

The analysis reflects the tuned Random Forest model, which achieved 96% accuracy and 95% ROC-AUC under Leave-One-User-Out (LOUO) cross-validation. Accuracy is reported alongside F1-score (0.82) and ROC-AUC to account for class imbalance and high-load detection performance.

Figures referenced here are under `figures/shap/` and related artifacts under `results/interpretation/`.

---

## Objectives of the SHAP Analysis

We use SHAP to answer four questions:

1. Which behavioral features most strongly predict cognitive load?
2. How do individual features influence predictions (local explanations)?
3. Do participants exhibit distinct behavioral "load profiles" (clusters)?
4. Are SHAP-derived explanations consistent with cognitive load theory?

---

## Global Explanations

### SHAP Summary Bar Plot

File: [`figures/shap/shap_summary_bar.png`](../figures/shap/shap_summary_bar.png)

![SHAP summary bar](../figures/shap/shap_summary_bar.png)

This plot shows mean |SHAP| values across all samples, ranking global predictors of high cognitive load.

Top global predictors of higher cognitive load:

1. `scheduling_difficulty` — complex temporal planning
2. `constraint_violation_rate` — repeated invalid actions
3. `budget_management_stress` — financial reasoning strain
4. `idle_time_ratio` — uncertainty or extended planning
5. `planning_time_ratio` — long delay before first action → higher intrinsic load
6. `multitasking_load` — frequent context switching → increased cognitive cost

Summary: High-load behavior manifests as planning complexity, constraint failures, and inefficient resource navigation—consistent with intrinsic and extraneous load sources.

### SHAP Beeswarm Distribution

File: [`figures/shap/shap_summary_beeswarm.png`](../figures/shap/shap_summary_beeswarm.png)

![SHAP beeswarm](../figures/shap/shap_summary_beeswarm.png)

Key observations:

- High `constraint_violation_rate` is uniformly positive → strong indicator of struggling users.
- `idle_time_ratio` shows mixed effects → depends on whether the pause is confusion vs. deliberate planning.
- Certain Task 1 features cluster near zero → limited relevance to high cognitive load.

---

## Local Explanations

Local SHAP explanations show how the model predicts cognitive load for specific participant–task trials.

### Participant Waterfall Plots

Examples:

- [`shap_waterfall_idx_0.png`](../figures/shap/shap_waterfall_idx_0.png)
- [`shap_waterfall_idx_10.png`](../figures/shap/shap_waterfall_idx_10.png)
- [`shap_waterfall_idx_20.png`](../figures/shap/shap_waterfall_idx_20.png)

Interpretation (idx 0 example):

- High `constraint_violation_rate` and `scheduling_difficulty` push the prediction upward.
- Higher `recovery_efficiency` pulls the prediction downward.

These plots illustrate the opposing feature contributions that produce the final classification.

### Force Plot

Interactive HTML (if generated): [`figures/shap/shap_force_idx_0.html`](../figures/shap/shap_force_idx_0.html)

The force plot visualizes the magnitude and direction of explanatory factors and is suitable for presentations and theses.

---

## SHAP-Based Clustering

We reduce SHAP values for the positive class using PCA (2D) and cluster them via KMeans (k=2). Clustering is exploratory and intended to reveal recurring explanation patterns, not to define fixed user types.

Artifacts:

- PCA visualization: [`figures/shap/shap_clusters_pca.png`](../figures/shap/shap_clusters_pca.png)
- Cluster centroids: [`results/interpretation/shap_cluster_centroids.json`](../results/interpretation/shap_cluster_centroids.json)
- Cluster assignments: [`results/interpretation/shap_clusters_assignments.csv`](../results/interpretation/shap_clusters_assignments.csv)
- Raw positive-class SHAP values: [`results/interpretation/shap_values_pos.npy`](../results/interpretation/shap_values_pos.npy)

### PCA Mapping

![SHAP clusters PCA](../figures/shap/shap_clusters_pca.png)

### Cluster Characteristics

- Cluster 1 — High Load Profiles
	- High constraint violations, idle time, scheduling difficulty
	- Higher planning time ratio and budgeting stress
	- Contains nearly all Task 3 trials with TLX > 60

- Cluster 0 — Low/Moderate Load Profiles
	- More efficient interaction patterns, low entropy
	- Minimal conflicts, faster decisions
	- Mostly Task 1 + Task 2 trials and low-load Task 3 trials

### Cluster Centroids

Stored in [`shap_cluster_centroids.json`](../results/interpretation/shap_cluster_centroids.json); each centroid represents the "average explanation pattern" per cluster.

---

## Key Behavioral Predictors

| Category               | Features                                      | Cognitive Interpretation                 |
|------------------------|-----------------------------------------------|------------------------------------------|
| Planning Burden        | `scheduling_difficulty`, `planning_time_ratio`| Increased intrinsic load                 |
| Cognitive Interruptions| `constraint_violation_rate`                   | Extraneous load, system mismatch         |
| Resource Overload      | `budget_management_stress`                    | Multi-constraint problem solving         |
| Multitasking Pressure  | `multitasking_load`                           | High switching cost                      |
| Processing Inefficiency| `idle_time_ratio`                             | Uncertainty, mental fatigue              |

Low-weight signals (e.g., zip code struggle, rapid hovers, trait skill/cautious) indicate that isolated micro-interactions are weak predictors of cognitive load on their own.

---

## Theory-Driven Interpretation

| Load Type       | Supported by SHAP Features                          | Interpretation               |
|-----------------|------------------------------------------------------|------------------------------|
| Intrinsic Load  | `planning_time_ratio`, `scheduling_difficulty`       | Core task difficulty         |
| Extraneous Load | `constraint_violation_rate`                          | UI design conflicts          |
| Germane Load    | `recovery_efficiency`                                | Productive cognitive effort  |

These alignments triangulate intrinsic, extraneous, and germane load components present in the observed interaction behavior.

---

## Implications for HCI & UX Design

- High `planning_time_ratio` → provide guided workflows, reduce options, offer auto-planning suggestions.
- Spikes in `constraint_violation_rate` → improve validation clarity, affordances, and adaptive error feedback.
- High `idle_time_ratio` → surface contextual hints or highlight the next step.
- Elevated `budget_management_stress` → simplify comparisons and reduce cognitive overhead in multi-parameter decisions.

SHAP yields actionable insights, enabling adaptive interfaces that respond to user cognitive state.

---

## Limitations & Considerations

- SHAP explanations depend on model stability; retraining can slightly shift attributions.
- The dataset size is modest (N = 75), which may underrepresent rare or edge-case behavioral patterns.
- PCA reduces dimensionality and may simplify complex explanation vectors.

---

## Conclusion

- Behavioral metrics provide strong, interpretable predictors of cognitive load.
- High-load behavior patterns cluster consistently across participants.
- Explanations align with established cognitive load theory.
- The Random Forest model captures psychologically meaningful structure.
- SHAP helps translate model intelligence into practical UX guidance.

Overall, this analysis strengthens the scientific credibility of the modeling pipeline and offers a robust interpretability foundation for both research and applied interactive systems.