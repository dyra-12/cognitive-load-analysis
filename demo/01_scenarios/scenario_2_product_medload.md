# Scenario 2 — Product Filtering (Moderate Cognitive Load)

## Overview
This scenario demonstrates a participant engaging with **Task 2: Product Exploration**, where moderate filtering complexity leads to measurable but not overwhelming cognitive load.

---

## Participant Summary
**Participant:** p-0014  
**Task:** task_2_product  
**TLX Score:** 56.7 → **Low/Moderate Load (0)**  
**Model Prediction:** Moderate Load (0.42 probability of high load)

---

## Behavioral Metrics
| Metric | Value | Interpretation |
|--------|-------|----------------|
| filter_optimization_score | **0.44** | Some filter toggling before settling |
| decision_uncertainty | **0.12** | A few rapid hovers but not excessive |
| exploration_breadth | **0.039** | Moderate product comparison |
| planning_time_ratio | **0.18** | Noticeable delay before first filter |
| multitasking_load | **0.36** | Several component switches |
| idle_time_ratio | **0.17** | Medium hesitation during comparison |

---

## Behavioral Narrative
User flow shows:
- Initial uncertainty while selecting filters  
- Moderate back-and-forth between product cards  
- Occasional pauses before making selections  
- Some redundant interactions (reset → reapply filters)

This reflects a typical **medium-load shopping experience**—neither effortless nor overwhelming.

---

## Model Reasoning (SHAP Summary)
Contributors **increasing** high-load probability:
- Moderately elevated **multitasking_load**
- Noticeable **idle_time_ratio**

Contributors **reducing** high-load probability:
- Low constraint violations  
- Efficient hovers and comparisons  

The model assigns a moderate probability but ultimately predicts **low load**, consistent with TLX 56.7.

---

## UI Implications
Mild adaptive interventions could help:
- Highlight top relevant filters based on behavior  
- Offer simplified comparison view  
- Reduce unnecessary re-filter cycles

---

## Takeaway
This scenario represents a **moderate cognitive load state**, driven by exploration-driven uncertainty rather than task structure difficulty.
