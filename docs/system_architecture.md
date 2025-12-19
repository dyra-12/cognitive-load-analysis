# System Architecture – CogniViz

CogniViz is a real-time behavioral inference framework that detects cognitive load directly from everyday user interaction patterns — without physiological sensors — and enables adaptive interfaces that respond intelligently to fluctuations in mental effort.

This document provides a high-level overview of the system architecture, data pipeline, and key design principles.

## 1. System Goals

### 🎯 Primary Objectives

- **Sensor-Free Load Detection** — infer cognitive load purely from browser interaction telemetry (mouse, keyboard, cursor dynamics).
- **Real-Time Responsiveness** — achieve end-to-end inference latency under 400 ms to support adaptive UIs.
- **Interpretability & Transparency** — provide SHAP-based explanations with every prediction.
- **Scalable, Browser-Native Deployment** — operate entirely within standard web environments using existing event APIs.

### 🌐 Core Capabilities

- Continuous workload estimation
- Live feature attribution via SHAP
- Adaptive UI simplification, guidance, and decluttering
- Privacy-preserving event capture (no raw keystrokes or personal data)

## 2. System Architecture

CogniViz follows a three-layer pipeline:

**Event Capture → Inference Backend → Adaptive UI Response**

### 2.1 Front-End (Event Capture Layer)

- **Technology:** React + TypeScript
- **Purpose:** Record fine-grained browser events including pointer, input, focus, and drag actions.
- **Sampling:** Aggregates raw events into behavioral metrics every 150–300 ms. Feature aggregation is performed locally in the browser before transmission, ensuring low latency and minimizing data exposure.
- **Privacy:** Logs only derived metrics (no keystroke content or identifiers).
- **Output:** Lightweight JSON payloads transmitted to backend via WebSocket or REST.

#### Captured Signals

| Category | Example Events | Derived Metrics |
|----------|----------------|-----------------|
| **Temporal** | Idle gaps, dwell time | `idle_time_ratio`, `planning_time_ratio` |
| **Motor** | Mouse trajectory, drag attempts | `mouse_entropy_avg`, `drag_attempts` |
| **Cognitive** | Constraint resolution, multitasking | `constraint_violation_rate`, `multitasking_load` |

### 2.2 Inference Backend (Server Layer)

- **Technology:** Python + FastAPI
- **Model:** Tuned Random Forest classifier trained on behavioral metrics.
- **Preprocessing:** Normalization using training-set statistics.
- **Inference Time:** 5–10 ms per sample (median end-to-end latency ≈ 210 ms).
- **Outputs:**
  - Predicted cognitive-load probability
  - SHAP explanation vector (per feature)

#### Design Characteristics

- Stateless service supporting multiple concurrent users.
- Pre-loaded model kept in memory for low latency.
- Returns both prediction and interpretability metadata in a single response.

### 2.3 Adaptive Interface Controller (Client Layer)

- **Role:** Adjust interface presentation dynamically based on predicted workload.
- **Adaptation Triggers:** High-load probability > threshold (default = 0.65, configurable per deployment).
- **Adaptations Include:**
  - Collapsing optional panels
  - Simplifying layouts or filter menus
  - Highlighting valid actions or conflict resolutions
  - Displaying contextual micro-guidance
- **Feedback:** Color-coded indicator
  - 🟢 Low 🟡 Moderate 🔴 High Load

All adaptations occur within the same perceptual frame (sub-second), maintaining user flow and minimizing distraction. If predictions are uncertain or unavailable, the interface defaults to its non-adaptive baseline to avoid disruptive behavior.

## 3. Interaction Flow

```
┌─────────────────────┐
│ 1. User Interaction │
│  (mouse, keyboard)  │
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│ 2. Event Processing │
│ (aggregate metrics) │
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│ 3. FastAPI Inference│
│   (Random Forest +  │
│    SHAP computation)│
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│ 4. Load Prediction  │
│   + Explanations    │
└─────────┬───────────┘
          ↓
┌─────────────────────┐
│ 5. Adaptive UI      │
│   (simplify, guide) │
└─────────────────────┘
```

This loop repeats every 150–400 ms, enabling moment-to-moment adaptation without interrupting user tasks.

## 4. Real-Time Performance

| Metric | Median | 95th Percentile |
|--------|--------|-----------------|
| **Inference Time** | 10 ms | 21 ms |
| **Network RTT** | 140 ms | 280 ms |
| **End-to-End Latency** | 210 ms | 338 ms |

Performance meets interactive-system standards for real-time feedback and ensures UI responses remain perceptually instantaneous.

## 5. Interpretability Framework

CogniViz integrates SHAP (SHapley Additive exPlanations) to ensure each prediction is explainable and auditable.

### 5.1 Global Explanations

Highlight overall feature importance across participants and tasks:
- `scheduling_difficulty`
- `constraint_violation_rate`
- `budget_management_stress`
- `idle_time_ratio`

### 5.2 Local Explanations

Per-user waterfall plots visualize additive feature effects for specific trials, revealing whether high load arises from constraint conflicts, extended planning, or idle pauses.

### 5.3 SHAP Clustering

PCA + K-means on SHAP vectors uncovers behavioral archetypes:
- **Cluster 0:** Efficient, low-conflict interactions
- **Cluster 1:** High-strain, error-prone patterns

These clusters validate the behavioral interpretability of the model and guide design adaptations.

## 6. Adaptive Interface Demonstration

A browser-based demo illustrates CogniViz in action:

| Context | Adaptation Trigger | Adaptive Behavior |
|---------|-------------------|-------------------|
| **Travel Planning** | High scheduling difficulty | Simplify layout, highlight valid time slots |
| **Product Filtering** | Elevated uncertainty or hover switching | Collapse menus, hide metadata, group filters |
| **Form Entry** | Low effort | Maintain full layout (no adaptation) |

Pilot users described adaptations as "helpful", "subtle", and "non-intrusive", supporting usability and cognitive relief without breaking task flow.

## 7. Key Design Principles

| Principle | Description |
|-----------|-------------|
| **Transparency** | Every inference includes an explanation vector for developer or research inspection. |
| **Responsiveness** | Adaptations triggered within 400 ms to preserve interaction continuity. |
| **Privacy-Preserving** | No sensitive content or personal identifiers logged. |
| **Scalability** | Runs in any modern browser — no hardware or plugins required. |
| **Modularity** | Independent front-end and back-end modules for easy integration. |

## 8. Summary

CogniViz represents a new paradigm in behavior-based adaptive interfaces:

- End-to-end real-time inference pipeline (React + FastAPI)
- Participant-independent modeling (F1 = 0.82, AUC = 0.95)
- SHAP-driven interpretability and adaptive feedback
- Lightweight, deployable, and sensor-free

This framework demonstrates that standard web telemetry can serve as a reliable, explainable signal for cognitive state estimation — paving the way toward truly human-aware, adaptive digital environments.

---

### ✅ See also:

- `docs/methodology.md` — study design, data collection, and statistical methods
- `docs/ML_Insights.md` — model analysis, SHAP visualizations, and performance evaluation