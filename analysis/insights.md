# Insights & Design Implications Report

_A comprehensive interpretation of behavioral, cognitive, and machine-learning findings._

## 1. Overview

This report summarizes key findings from the cognitive load study across three tasks:

- Task 1 — Form Entry (Low Load)
- Task 2 — Product Exploration (Medium Load)
- Task 3 — Travel Planning (High Load)

### 1.1 Cognitive Load Gradient Across Tasks

The NASA-TLX scores show a clear stepwise increase across tasks, validating the experimental design and supporting the primary hypothesis.

| Task   | Description         | TLX (≈) |
|--------|----------------------|---------|
| Task 1 | Form Entry           | 28      |
| Task 2 | Product Selection    | 45      |
| Task 3 | Travel Planning      | 72      |

## 2. Strongest Behavioral Indicators of Cognitive Load

### 2.1 High-Load Predictors (Positive Correlation with TLX)

These features were the strongest indicators of cognitive load in both statistical and ML analyses:

| Rank | Feature                     | Pearson r | Strength       | Interpretation                               |
|------|-----------------------------|-----------|----------------|-----------------------------------------------|
| 1    | `scheduling_difficulty`     | 0.81      | Very Strong 🔥 | Multiple failed attempts to schedule/drag     |
| 2    | `constraint_violation_rate` | 0.80      | Very Strong 🔥 | Repeated invalid actions                      |
| 3    | `budget_management_stress`  | 0.80      | Very Strong 🔥 | Multiple cost recalculations                  |
| 4    | `multitasking_load`         | 0.73      | Strong 🔥      | Excessive component switching                 |
| 5    | `drag_attempts`             | 0.66      | Strong 🔥      | Repeated failing drag operations              |

These metrics peaked in Task 3, reinforcing its role as the high-load condition.

### 2.2 Low-Load Predictors (Negative Correlation with TLX)

| Feature                    | Pearson r | Interpretation                    |
|---------------------------|-----------|------------------------------------|
| `recovery_efficiency`     | -0.62     | Fast, low-effort error correction |
| `form_efficiency`         | -0.58     | Smooth, efficient form entry      |
| `form_hesitation_index`   | -0.53     | Clear fields → low hesitation     |

Dominant in Task 1 (low-load condition).

### 2.3 SHAP Feature Importance

Global feature importance (higher = stronger influence on model):

1. `scheduling_difficulty`
2. `constraint_violation_rate`
3. `budget_management_stress`
4. `multitasking_load`
5. `drag_attempts`
6. `mouse_entropy_avg`
7. `recovery_efficiency` (negative influence)
8. `form_efficiency` (negative influence)
9. `form_hesitation_index` (negative influence)

Note: The top three features collectively explain ~68% of TLX variance.

## 3. UX Design Guidelines (Metric-Driven)

### 3.0 High-Load Thresholds

| Feature                     | Threshold | Meaning                    |
|----------------------------|-----------|----------------------------|
| `scheduling_difficulty`    | > 0.65    | Time-placement failures    |
| `constraint_violation_rate`| > 0.45    | Rule-breaking attempts     |
| `budget_management_stress` | > 0.55    | Budget recalculation loops |
| `multitasking_load`        | > 0.45    | Frequent UI switching      |
| `drag_attempts`            | > 4       | Drag failures              |
| `form_hesitation_index`    | > 2.5s    | Unclear form labels        |
| `form_efficiency`          | < 0.018   | Slow form completion       |
| `recovery_efficiency`      | < -0.45   | Expensive recovery effort  |

### 3.1 Complete Guidelines

1) Reduce Scheduling Complexity
	 - Trigger: `scheduling_difficulty` > 0.65 or `drag_attempts` > 4
	 - Interpretation: Cognitive overload from planning
	 - Fixes: Auto-snap scheduling; highlight valid regions

2) Prevent Constraint Violations
	 - Trigger: `constraint_violation_rate` > 0.45
	 - Interpretation: Users attempt invalid actions repeatedly
	 - Fixes: Inline validation; disable invalid actions

3) Simplify Budget Interactions
	 - Trigger: `budget_management_stress` > 0.55
	 - Interpretation: Users struggle with cost calculations
	 - Fixes: Dynamic totals; cost forecasts

4) Reduce UI Fragmentation
	 - Trigger: `multitasking_load` > 0.45
	 - Interpretation: Excessive context switching across panels/components
	 - Fixes: Consolidate panels; reduce switching

5) Optimize Form Entry
	 - Trigger: Low `form_efficiency`
	 - Interpretation: Users spend too long completing forms
	 - Fixes: Autofill; input examples

6) Lower Form Hesitation
	 - Trigger: `form_hesitation_index` > 2.5s
	 - Interpretation: Unclear or intimidating inputs
	 - Fixes: Clearer labels; examples/microcopy

7) Tame Drag-and-Drop Burden
	 - Trigger: `drag_attempts` > 4
	 - Interpretation: Interaction pattern is too demanding
	 - Fixes: Switch to click-to-place pattern

8) Make Error Recovery Fast
	 - Trigger: `recovery_efficiency` < -0.45
	 - Interpretation: Recovery is costly and frustrating
	 - Fixes: Undo; non-destructive edits

## 4. Demo Scenarios (Behavior → Prediction → Fix)

- Scenario 1 — Form Confusion
	- hesitation: 3.1s; corrections: 3
	- prediction: 63% high load
	- fix: better microcopy; autofill

- Scenario 2 — Filter Overload
	- rapid hovers: 19; resets: 4
	- prediction: 71% high load
	- fix: grouped filters

- Scenario 3 — Comparison Overload
	- exploration breadth: 0.31
	- prediction: 78% high load

- Scenario 4 — Scheduling Failure
	- scheduling_difficulty: 0.72
	- prediction: 94% high load

- Scenario 5 — Budget Stress
	- budget_stress: 0.63
	- prediction: 91% high load

- Scenario 6 — Multitasking Breakdown
	- multitasking_load: 0.52
	- prediction: 89% high load

## 5. Real-World Validation Cases

- Amazon (Task 2 analog)
	- Matches high: `decision_uncertainty`, `multitasking_load`
	- Prediction: Medium–High load

- Airline Booking Sites (Task 3 analog)
	- Matches high: `budget_stress`, `constraint_violations`
	- Prediction: High load

- Government Forms (Task 1 analog)
	- Matches high: `hesitation`, low efficiency
	- Prediction: Medium–High load

…and additional cases follow similarly.

## 6. Model Performance Summary

| Model                | Acc  | Prec | Recall | F1   | ROC-AUC |
|---------------------|------|------|--------|------|---------|
| Baseline (majority) | 0.73 | 0.00 | 0.00   | 0.00 | —       |
| Logistic Regression | 0.92 | 0.68 | 0.72   | 0.69 | 0.88    |
| Tuned Random Forest | 0.96 | 0.68 | 0.66   | 0.82 | 0.94    |

## 7. Behavioral Model Pipeline

User Interaction → Features → ML → Cognitive Load Alerts

Clicks, drags, hovers, errors, navigation → hesitation, violations, scheduling → Random Forest (F1 ≈ 0.82) → UI warnings and adaptive simplification

## 8. Final Takeaways

- Behavioral telemetry can reliably detect cognitive load.
- Metrics directly guide adaptive UX design.
- Models predict user struggle before failure occurs.
