# Methodology – CogniViz

This document details the full methodological framework used in the CogniViz study — from experimental design and data collection to preprocessing, statistical analysis, and model validation. It is intended for inclusion in `docs/methodology.md`.

## 1. Study Design

### 1.1 Overview

CogniViz investigates whether cognitive load can be inferred directly from natural user interactions (e.g., mouse movements, keystrokes, and click dynamics) without requiring physiological sensors.

A within-subject experimental design was adopted, comprising 25 participants performing three web-based tasks designed to elicit increasing cognitive demand levels (low, medium, and high). This design enabled both intra-individual and cross-task comparisons.

### 1.2 Participant Recruitment

- **N = 25 participants** (balanced gender, aged 20–38)
- All participants were proficient in everyday computer use.
- Recruitment was voluntary through university mailing lists.
- Participants provided informed consent and were compensated with gift vouchers.

### 1.3 Experimental Setup

- Sessions were conducted in a controlled browser environment (React-based interface).
- Each participant completed all three tasks in counterbalanced order to mitigate sequence effects.
- Screen resolution and input devices (mouse + keyboard) were standardized.
- No physiological sensors were used; all telemetry derived from native web events.

### 1.4 Task Design

Each task captured distinct interaction modalities and difficulty levels:

| Task | Description | Cognitive Load Level | Behavioral Focus |
|------|-------------|---------------------|------------------|
| **Task 1 – Form Entry** | Linear data entry form (name, email, address, etc.) | Low | Input fluency, hesitation |
| **Task 2 – Product Exploration** | Filtered product catalog; attribute comparisons | Medium | Hover switching, exploration breadth |
| **Task 3 – Travel Planning** | Multi-panel scheduling with budget and time constraints | High | Conflict resolution, multitasking, constraint violations |

Each task was designed to systematically manipulate intrinsic and extraneous cognitive load dimensions.

## 2. Data Collection Procedures

### 2.1 Telemetry Capture

Front-end logging in React captured:
- Pointer events (movement, drag, hover, focus)
- Keystrokes and input timing
- Clicks, scrolls, and idle intervals
- **Sampling frequency:** 150–300 ms
- Logged as JSON payloads, serialized to the FastAPI backend.

**Raw keystrokes and sensitive content were never transmitted** — only derived behavioral metrics, ensuring privacy compliance.

### 2.2 Ground-Truth Labeling (NASA-TLX)

- After each task, participants completed the **NASA Task Load Index (TLX)**.
- **Six subscales:** Mental, Physical, Temporal Demand, Performance, Effort, and Frustration.
- Mean TLX score computed per task.
- **Binary labeling used:**
  - **High Load:** TLX > 60
  - **Low Load:** TLX ≤ 60

This threshold aligns with prior cognitive-state classification research.

### 2.3 Dataset Composition

- **Total samples:** 75 (25 × 3 tasks)
- **Per-sample data:** engineered behavioral metrics, contextual factors, and TLX score.
- Dataset stored as anonymized CSV for open release.

## 3. Preprocessing and Feature Engineering

### 3.1 Raw Event Aggregation

Low-level browser events were grouped into temporal windows to compute higher-level behavioral indicators. Feature values were computed over rolling windows to support both offline analysis and real-time inference consistency. Key computed metrics included:

| Metric | Description |
|--------|-------------|
| `form_hesitation_index` | Latency before field input |
| `constraint_violation_rate` | Number of rule/conflict breaches |
| `budget_management_stress` | Adjustments made due to cost limits |
| `multitasking_load` | Frequency of context switches |
| `idle_time_ratio` | Time spent inactive between actions |
| `mouse_entropy_avg` | Randomness in pointer trajectory |
| `recovery_efficiency` | Time from error to correction |

Additional features such as `trait_skill` and `trait_cautiousness` served as stabilizers for user-specific variability.

### 3.2 Feature Correlation

Pearson correlations between behavioral metrics and TLX showed:

**Strong positive correlates:**
- `scheduling_difficulty` (r = .81)
- `constraint_violation_rate` (r = .80)
- `budget_management_stress` (r = .80)

**Negative correlates:**
- `form_efficiency` (r = –.58)
- `recovery_efficiency` (r = –.62)

These align with Cognitive Load Theory — higher complexity and conflict correlate with elevated perceived load.

## 4. Statistical Analysis Plan

### 4.1 Hypotheses

1. Task complexity (form → product → travel) will produce a significant increase in TLX scores.
2. Behavioral features (hesitation, violations, idle time) will correlate positively with TLX.
3. Machine learning models can reliably classify cognitive load states using behavioral data alone.

### 4.2 Analytical Methods

- **Repeated-Measures ANOVA** on TLX scores to confirm task difficulty gradient (p < .001).
- **Pearson Correlations** for feature–load relationships.
- **Feature Importance Analysis** using Random Forest's mean decrease in impurity.
- **SHAP Explanations** for global and local interpretability:
  - **Global:** feature contribution to model output.
  - **Local:** per-instance decision logic (waterfall plots).
- **Cluster Analysis** (PCA + K-means) on SHAP vectors to reveal latent behavioral profiles.

### 4.3 Rationale

- ANOVA validates experimental manipulation of load.
- Correlations and SHAP ensure interpretability.
- Cluster analysis reveals behavioral archetypes of cognitive strain without supervision.

## 5. Model Training and Validation

### 5.1 Target Variable

Binary classification:
- **High Load (1)** = TLX > 60
- **Low Load (0)** = TLX ≤ 60

### 5.2 Validation Strategy

**Leave-One-User-Out (LOUO)** cross-validation:
- Trains on 24 participants, tests on 1 unseen participant.
- Ensures participant-independent generalization — critical for real-world deployment.

### 5.3 Models Compared

| Model | Preprocessing | Key Parameters | Purpose |
|-------|---------------|----------------|---------|
| Majority Baseline | None | — | Performance floor |
| Logistic Regression | StandardScaler | C=1.0, class_weight=balanced | Linear separability test |
| Random Forest (Tuned) | None | n_estimators≈300, max_depth≈10, class_weight=balanced | Nonlinear modeling + SHAP interpretability |

### 5.4 Performance Summary

| Metric | Majority | Logistic | Random Forest |
|--------|----------|----------|---------------|
| **Accuracy** | 0.73 | 0.92 | 0.96 |
| **Precision** | 0.00 | 0.68 | 0.68 |
| **Recall** | 0.00 | 0.72 | 0.66 |
| **F1-Score** | 0.00 | 0.69 | 0.82 |
| **ROC-AUC** | 0.50 | 0.89 | 0.95 |

The Random Forest achieved the best balance between predictive performance, interpretability (via SHAP), and real-time feasibility (<400 ms latency).

## 6. Interpretability and Validation

- **Global SHAP:** Top contributors → `scheduling_difficulty`, `constraint_violation_rate`, `budget_management_stress`, and `idle_time_ratio`.
- **Local SHAP:** Trial-level explanations highlighting individual differences (e.g., over-reporters vs. under-reporters).
- **SHAP Clustering:** Revealed two user archetypes —
  - **High-load:** conflict-heavy, erratic, slow.
  - **Efficient:** smooth, low-error, adaptive.

## 7. Ethical and Privacy Considerations

- Only anonymized behavioral data were recorded.
- No raw content, keystrokes, or identifiable information stored.
- Participants could withdraw at any point.
- The study was classified as IRB-exempt (minimal-risk behavioral research).
- Institutional ethics screening confirmed exemption status prior to data collection.

## 8. Summary

CogniViz demonstrates a sensor-free, behavior-based method for real-time cognitive load detection:

- Ecologically valid multi-task dataset.
- Participant-independent Random Forest classifier (F1 = 0.82).
- Fully functional browser pipeline (React + FastAPI).
- Sub-400 ms inference enabling adaptive UI behavior.

The methodology ensures reproducibility, interpretability, and ethical compliance, establishing CogniViz as a foundation for human-centered adaptive systems.


---

### ✅ See also:

- `docs/system_architecture.md` — system architecture and design principles
- `docs/ML_Insights.md` — model analysis, SHAP visualizations, and performance evaluation