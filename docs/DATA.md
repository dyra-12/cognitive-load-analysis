# CogniViz Dataset Documentation

## Overview

This document describes the dataset used to train and evaluate CogniViz, a browser-native, sensor-free framework for real-time cognitive load inference from natural interaction behavior. The dataset consists of high-resolution browser interaction telemetry collected during three realistic web-based tasks designed to elicit systematically varying levels of cognitive load.

The dataset integrates:

- Raw browser interaction events  
- Derived behavioral metrics  
- Subjective workload ground truth (NASA-TLX)  
- Task metadata and contextual variables  

It is designed to support participant-independent cognitive load modeling, interpretable behavioral analysis, and explainable machine learning.

---

## 1. Dataset Summary

| Attribute                  | Value                              |
|----------------------------|------------------------------------|
| Participants               | 25                                 |
| Tasks per participant      | 3                                  |
| Total task instances       | 75                                 |
| Interaction modality       | Mouse + keyboard                   |
| Platform                   | Desktop web browser                |
| Sampling resolution        | Event-based (millisecond time)    |
| Behavioral features        | 16 primary metrics                 |
| Ground truth               | NASA-TLX subjective workload       |
| Cognitive load labels      | Binary (TLX > 60 = High Load)      |
| Validation protocol        | Leave-One-User-Out (LOUO)          |

---

## 2. Study Design and Task Context

Each participant completed three web-based tasks designed to elicit increasing levels of cognitive load while preserving ecological validity.

### 2.1 Task 1: Form Completion (Low Cognitive Load)

Participants completed a linear shipping form requesting basic personal information.

**Characteristics:**
- Sequential interaction structure  
- Minimal branching or decision complexity  
- No explicit constraints or trade-offs  

**Expected behavioral profile:**
- Fluent input behavior  
- Low hesitation  
- Low correction frequency  

---

### 2.2 Task 2: Product Exploration (Medium Cognitive Load)

Participants browsed a product catalog, applied filters, compared items, and reset selections.

**Characteristics:**
- Moderate decision complexity  
- Iterative refinement of criteria  
- Selective attention and trade-off reasoning  

**Expected behavioral profile:**
- Exploratory navigation  
- Intermittent hesitation  
- Decision uncertainty  
- Moderate multitasking  

---

### 2.3 Task 3: Travel Planning (High Cognitive Load)

Participants constructed a travel itinerary including flights, accommodations, and meetings.

**Characteristics:**
- Multi-panel navigation  
- Drag-and-drop scheduling  
- Conflict detection and resolution  
- Budget constraints  
- Interdependent decision structure  

**Expected behavioral profile:**
- Prolonged planning pauses  
- Constraint violations  
- Repeated corrections  
- Multitasking behavior  
- Breakdown–repair cycles  

---

## 3. Data Collection Pipeline

### 3.1 Instrumentation

Interaction data were captured using native browser event listeners:

- Pointer events: `pointermove`, `mousedown`, `mouseup`, `click`  
- Input events: `keydown`, `keyup`, `input`, `change`  
- Focus events: `focus`, `blur`  
- Hover events: `mouseenter`, `mouseleave`  
- Drag events: `dragstart`, `dragover`, `drop`  

All events were time-stamped at millisecond resolution.

---

### 3.2 Privacy Preservation

To support privacy-preserving data collection:

- No raw keystrokes or text content were stored  
- No personally identifiable information (PII) was logged  
- Only derived behavioral metrics were transmitted to the server  
- Raw interaction traces remained client-side  
- All data were anonymized at source  

---

## 4. Raw Data Structure

Raw interaction logs (client-side) are structured as event streams with the following schema:

```json
{
  "participant_id": "p001",
  "task_id": "task_3_travel",
  "timestamp": 1712345678910,
  "event_type": "pointermove",
  "x": 812,
  "y": 433,
  "target_element": "calendar_slot",
  "context": {
    "panel": "schedule_view",
    "constraint_state": "invalid"
  }
}
```

**Fields:**

| Field | Description |
|-------|-------------|
| participant_id | Anonymized participant identifier |
| task_id | Task identifier |
| timestamp | Event timestamp (ms) |
| event_type | Browser event type |
| x, y | Pointer coordinates (if applicable) |
| target_element | UI element interacted with |
| context | Task- and UI-specific metadata |

---

## 5. Derived Behavioral Features

Raw interaction events are aggregated into 16 primary behavioral metrics grounded in cognitive load theory and micro-interaction research.

| Feature Name | Category | Description |
|--------------|----------|-------------|
| form_hesitation_index | Temporal | Average latency before form-field interactions |
| form_error_rate | Error-related | Proportion of invalid or corrected form submissions |
| form_efficiency | Performance | Ratio of completed fields to interaction time |
| zip_code_struggle | Error-related | Frequency of repeated edits in ZIP-code fields |
| filter_optimization_score | Decision complexity | Degree to which filter adjustments converge toward optimal constraints |
| decision_uncertainty | Decision complexity | Variability and reversals in choice behavior |
| exploration_breadth | Navigation | Number of distinct UI elements or products explored |
| planning_time_ratio | Temporal | Proportion of task time spent in planning states |
| multitasking_load | Temporal | Overlap of concurrent interaction streams |
| constraint_violation_rate | Error-related | Rate of actions violating task constraints |
| budget_management_stress | Decision complexity | Frequency of budget overflows and corrective actions |
| scheduling_difficulty | Decision complexity | Number of conflicting or rescheduled time selections |
| recovery_efficiency | Error-related | Speed and effectiveness of post-error correction |
| rapid_hovers | Motor behavior | Rate of short-duration hover events |
| idle_time_ratio | Temporal | Fraction of task time spent inactive |
| mouse_entropy_avg | Motor behavior | Entropy of pointer trajectories |

---

## 6. Contextual and Control Variables

In addition to primary behavioral features, the dataset includes contextual variables used for offline analysis and stability assessment:

| Variable Name | Description |
|---------------|-------------|
| trait_skill | Self-reported task proficiency |
| trait_cautious | Self-reported risk aversion |
| device_type | Desktop / laptop |
| screen_resolution | Browser viewport size |
| task_order | Counterbalancing order |

These variables were not used during real-time inference and were included solely for post-hoc analysis and evaluation.

---

## 7. Ground Truth Labels

### 7.1 NASA-TLX Scores

After each task, participants completed the NASA Task Load Index questionnaire.

**Six subscales:**

- Mental demand
- Physical demand
- Temporal demand
- Performance
- Effort
- Frustration

The overall workload score was computed as the unweighted mean.

### 7.2 Cognitive Load Labels

Cognitive load was operationalized as a binary label:

- **High Load:** NASA-TLX > 60
- **Low Load:** NASA-TLX ≤ 60

This threshold is widely used in cognitive workload research.

---

## 8. Final Dataset Format

The final modeling dataset consists of one row per participant–task instance.

```csv
participant_id,task_id,form_hesitation_index,form_error_rate,form_efficiency,zip_code_struggle,filter_optimization_score,decision_uncertainty,exploration_breadth,planning_time_ratio,multitasking_load,constraint_violation_rate,budget_management_stress,scheduling_difficulty,recovery_efficiency,rapid_hovers,idle_time_ratio,mouse_entropy_avg,nasa_tlx_score,load_label
p001,task_1_form,0.18,0.00,0.92,0.00,0.00,0.04,6,0.12,0.02,0.00,0.00,0.00,0.88,0.31,0.05,0.42,28,0
p001,task_2_product,0.42,0.03,0.71,0.00,0.61,0.19,15,0.28,0.13,0.07,0.14,0.08,0.62,0.44,0.17,0.51,45,0
p001,task_3_travel,0.73,0.08,0.48,0.00,0.00,0.31,9,0.56,0.41,0.29,0.37,0.62,0.29,0.58,0.34,0.69,72,1
```

---

## 9. Class Distribution

| Load Label | Count | Percentage |
|------------|-------|------------|
| Low Load | 47 | 62.7% |
| High Load | 28 | 37.3% |

The dataset exhibits moderate class imbalance.

---

## 10. Data Quality and Validation

### 10.1 Completeness

- No missing feature values
- All task instances include NASA-TLX scores
- All participants completed all three tasks

### 10.2 Consistency Checks

- Feature ranges verified across tasks
- Timestamp continuity validated
- Task metadata consistency verified

### 10.3 Behavioral Plausibility

- Behavioral feature distributions align with task difficulty
- High-load tasks exhibit higher planning difficulty, constraint violations, and idle time
- Low-load tasks exhibit higher efficiency and recovery performance

---

## 11. Limitations

- Modest dataset size (N = 75 task instances)
- Desktop-only interaction context
- Controlled task environments
- Binary operationalization of cognitive load
- Cultural and demographic homogeneity

---

## 12. Ethical Considerations

- No physiological sensors used
- No sensitive content logged
- Anonymized data collection
- Informed consent obtained
- No deceptive task design

Future deployments will require formal IRB approval for expanded data collection.

---

## 13. Reuse and Extension

The dataset is suitable for:

- Cognitive load classification
- Behavioral feature analysis
- Explainable ML research
- Human-centered adaptive UI design
- Breakdown–repair modeling
- Interaction telemetry research

Extensions may include:

- Larger participant populations
- Longitudinal data
- Mobile and touch interaction
- Multimodal calibration
- Continuous workload modeling

---

## 14. Summary

The CogniViz dataset integrates high-resolution interaction telemetry, cognitively grounded behavioral features, and subjective workload ground truth to support interpretable, participant-independent cognitive load modeling. It provides a rigorous foundation for research on sensor-free cognitive state inference and human-centered adaptive interfaces.