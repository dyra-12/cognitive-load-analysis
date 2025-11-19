# Scenario 3 — Travel Planning (High Cognitive Load)

## Overview
This scenario captures a participant engaging with **Task 3: Travel Planning**, the most cognitively demanding task involving scheduling, budgeting, and multi-step decision-making.

---

## Participant Summary
**Participant:** p-0011  
**Task:** task_3_travel  
**TLX Score:** 81.7 → **High Load (1)**  
**Model Prediction:** High Load (0.92 probability)

---

## Behavioral Metrics
| Metric | Value | Interpretation |
|--------|-------|----------------|
| budget_management_stress | **0.67** | Frequent adjustments + budget overruns |
| constraint_violation_rate | **0.52** | Multiple invalid selections |
| scheduling_difficulty | **0.63** | Many drag attempts & conflicts |
| multitasking_load | **0.58** | Rapid switching between UI components |
| idle_time_ratio | **0.32** | Long pauses (planning hesitation) |
| drag_attempts | **7** | High struggle assigning meetings |
| planning_time_ratio | **0.41** | Long delay before first meaningful action |

*All key metrics exceed high-load thresholds.*

---

## Behavioral Narrative
This user exhibits classic signs of cognitive overload:
- Repeatedly tries invalid flight & hotel combinations  
- Struggles dragging meetings to conflict-free slots  
- Switches rapidly between tabs (Flights → Hotels → Meetings → Back)  
- Long pauses while recalculating budget impact  
- Attempts multiple planning sequences but abandons midway  

Overall, the user appears disoriented and cognitively taxed.

---

## Model Reasoning (SHAP Summary)
Top features pushing the prediction **strongly upward**:
- **Constraint Violations** → strongest positive SHAP  
- **Scheduling Difficulty** → major contributor  
- **Budget Stress** → reflects multi-constraint problem solving  
- **Idle Time Ratio** → prolonged uncertainty  
- **Multitasking Load** → fragmented attention  

The model is highly confident in high-load classification.

---

## UI Implications
Adaptive UI response recommended:
- Enable **“Auto-plan smart suggestions”**  
- Disable or gray-out invalid dates  
- Provide constraint-aware itineraries  
- Reduce information density (collapse sidebars)  
- Highlight only feasible meeting slots  

The system should transition to a **"supportive mode"** for overloaded users.

---

## Takeaway
This scenario is the clearest example of **true cognitive overload**, reflected in both the TLX score and strong behavioral signatures. It demonstrates the practical necessity of adaptive UX interventions.
