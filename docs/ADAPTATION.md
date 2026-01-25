# CogniViz Adaptation Engine  
## UI Logic & Human–Computer Interaction Theory

## Overview

This document describes the adaptive interface layer of CogniViz, a browser-native, sensor-free framework for real-time cognitive load inference from natural interaction behavior. While the modeling stack infers cognitive load and generates explanations, the Adaptation Engine operationalizes these inferences into **proportional, interpretable, and psychologically grounded UI responses**.

The adaptation layer is not reactive automation. It is a **human-centered control system** that modulates interface complexity based on sustained behavioral evidence of cognitive strain.

Core design commitments:

1. Preserve user agency  
2. Avoid pathologizing productive effort  
3. Ground adaptations in explanation, not prediction alone  
4. Align UI changes with cognitive theory  
5. Prevent reactive or jittery intervention  

---

## 1. Adaptation Philosophy

CogniViz rejects the view of cognitive load as a binary error state.

Instead, cognitive load is treated as:

- A **dynamic interaction state**  
- Emerging from sustained breakdown–repair cycles  
- Context-dependent across task types  
- Heterogeneously expressed across users  

Therefore:

> The goal of adaptation is not to reduce effort indiscriminately,  
> but to reduce **breakdown-induced friction** while preserving productive reasoning.

---

## 2. Architectural Position of Adaptation

The Adaptation Engine sits downstream of:

- Behavioral telemetry  
- Cognitive load inference  
- SHAP explanation generation  

The adaptation pipeline receives:

- Predicted load probability  
- Binary load state  
- SHAP attribution vector  
- Task context metadata  

It outputs:

- UI state modifications  
- Visual feedback signals  
- Guidance affordances  
- Layout adjustments  

---

## 3. Temporal Smoothing and Hysteresis

To prevent reactive or jittery UI behavior, CogniViz applies **temporal smoothing and hysteresis**.

### 3.1 Calibration Phase

- Initial interaction period is treated as calibration  
- No adaptation is applied  
- Behavioral baselines are established  

---

### 3.2 Load Escalation

Transition into a high-load state requires:

- Sustained high-load probability  
- Persistence across multiple inference windows  
- Repeated breakdown indicators  

This reflects:

> Cognitive strain accumulates over repeated interaction failures,  
> not isolated pauses or single errors.

---

### 3.3 Load Recovery

Transition back to a lower-load state requires:

- Sustained fluent interaction  
- Efficient recovery behavior  
- Reduction in breakdown indicators  

This avoids:

- Premature withdrawal of helpful adaptations  
- Oscillatory UI behavior  

---

## 4. Explanation-Driven Control Logic

CogniViz does not adapt solely based on scalar load scores.

Instead, it uses **SHAP attributions as control signals**.

This enables:

- Localized adaptation  
- Psychologically aligned guidance  
- Avoidance of generic UI simplification  

---

### 4.1 Feature-to-Intervention Mapping

| Dominant SHAP Feature         | Interpretation                     | Adaptation Triggered                          |
|-------------------------------|------------------------------------|-----------------------------------------------|
| Constraint violation rate     | Conflict resolution breakdown      | Highlight valid regions, surface constraints  |
| Scheduling difficulty         | Planning overload                  | Localized scheduling guidance                 |
| Budget management stress      | Resource trade-off overload        | Budget previews, cost impact overlays         |
| Idle time ratio               | Cognitive pausing / stalled action | Micro-guidance, reduced visual clutter       |
| Multitasking load             | Attentional fragmentation          | Collapse secondary panels                     |
| Recovery efficiency (low)     | Inefficient breakdown repair       | Stepwise correction hints                     |

This mapping ensures:

> The system adapts to *why* the user is struggling, not just *that* they are struggling.

---

## 5. Task-Specific Adaptation Policies

CogniViz applies **contextual, task-specific adaptation** rather than global UI reduction.

---

### 5.1 Form Completion Task

**Behavioral signals monitored:**

- Hesitation duration  
- Field-level error frequency  
- Idle bursts  
- Recovery efficiency  

**Adaptation strategies:**

- Highlight valid input regions after repeated invalid entries  
- Provide micro-guidance for persistent hesitation  
- Surface inline validation cues  
- Collapse secondary interface panels under sustained strain  

**HCI grounding:**

- Error prevention heuristics  
- Recognition over recall  
- Feedback immediacy  
- Progressive disclosure  

---

### 5.2 Product Exploration Task

**Behavioral signals monitored:**

- Exploration breadth  
- Decision reversals  
- Hover oscillations  
- Multitasking load  

**Adaptation strategies:**

- Introduce transient comparison overlays  
- Summarize differences between frequently compared items  
- Reduce filter density during sustained overload  
- Suppress guidance during focused selection actions  

**HCI grounding:**

- Information foraging theory  
- Sensemaking loops  
- Bounded rationality  
- Attention economy  

---

### 5.3 Planning and Scheduling Task

**Behavioral signals monitored:**

- Constraint violations  
- Scheduling conflicts  
- Budget overflows  
- Repeated drag failures  
- Recovery efficiency  

**Adaptation strategies:**

- Highlight conflicting time slots or budget elements  
- Localize guidance to the current subtask  
- Surface constraint previews  
- Simplify layout under sustained breakdown  

**HCI grounding:**

- Breakdown–repair models  
- Distributed cognition  
- Executive control theory  
- Cognitive load theory  

---

## 6. Productive Load vs. Breakdown Load

CogniViz distinguishes between:

- **Productive cognitive effort**  
- **Breakdown-induced strain**

---

### 6.1 Productive Load

Characterized by:

- Sustained exploration  
- Focused navigation  
- Low constraint conflict  
- High recovery efficiency  

System behavior:

- No intervention  
- No UI simplification  
- Suppressed guidance  

---

### 6.2 Breakdown Load

Characterized by:

- Repeated invalid actions  
- Prolonged idle time  
- Multitasking spikes  
- Inefficient recovery  

System behavior:

- Progressive disclosure  
- Constraint highlighting  
- Micro-guidance  
- Localized UI simplification  

This avoids:

> Treating all effort as error  
> or all difficulty as failure.

---

## 7. Proportional Intervention Policy

Adaptation intensity scales with:

- Magnitude of inferred cognitive load  
- Persistence of breakdown signals  
- Strength of explanation signals  

---

### 7.1 Low Intensity

- Subtle visual cues  
- Highlighting  
- Transient overlays  

---

### 7.2 Medium Intensity

- Localized guidance  
- Panel collapse  
- Filter reduction  

---

### 7.3 High Intensity

- Layout simplification  
- Task decomposition  
- Constraint previews  
- Focus mode  

This prevents:

- Over-assistance  
- Learned helplessness  
- Interface authoritarianism  

---

## 8. Interpretability and Trust

Each adaptation is:

- Tied to an explanation signal  
- Legible to the user  
- Contextually grounded  

Examples:

- Highlighted conflicts correspond to detected violations  
- Guidance appears only after repeated breakdown  
- UI simplification reverses after fluent recovery  

This supports:

- User trust  
- Perceived control  
- Explanation coherence  

---

## 9. Human–AI Interaction Principles

The adaptation engine is grounded in:

### 9.1 Human-Centered AI

- Support, not replacement  
- Agency preservation  
- Transparency  
- Proportionality  

---

### 9.2 Cognitive Load Theory

- Reduce extraneous load  
- Preserve germane load  
- Avoid eliminating productive effort  

---

### 9.3 Breakdown–Repair Theory

- Detect sustained breakdown  
- Support repair  
- Avoid over-intervention  

---

### 9.4 Progressive Disclosure

- Reveal assistance only when needed  
- Hide secondary complexity under strain  

---

## 10. Design Rationale

The adaptation design reflects five guiding constraints:

1. **Avoid reactive behavior**  
2. **Avoid global simplification**  
3. **Avoid opaque automation**  
4. **Avoid one-size-fits-all logic**  
5. **Avoid treating effort as error**  

---


## 11. Summary

The CogniViz Adaptation Engine operationalizes cognitive load inference into a human-centered, explanation-driven UI control system. By grounding interventions in sustained behavioral evidence and aligning responses with psychological theory, CogniViz demonstrates how adaptive interfaces can support cognition without undermining autonomy, trust, or productive effort.

Rather than reacting to predicted internal states, CogniViz adapts to **interaction breakdowns**, treating cognitive load as an emergent system signal that informs proportional, interpretable, and context-sensitive interface behavior.

