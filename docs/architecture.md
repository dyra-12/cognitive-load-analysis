# CogniViz System Architecture

## Overview

CogniViz is a browser-native, sensor-free framework for real-time cognitive load inference from natural interaction behavior. The system is designed as a closed-loop Human–AI Interaction (HAI) pipeline that continuously senses user interaction, infers cognitive load using an interpretable machine learning model, and applies cognitively grounded interface adaptations in near real time.

The architecture prioritizes four core design goals:

1. **Low-latency responsiveness** – to enable moment-to-moment cognitive state tracking during interaction.
2. **Interpretability** – to ensure that workload inferences are explainable and psychologically meaningful.
3. **Deployability** – to operate entirely within standard web environments without specialized hardware or plugins.
4. **Human-centered adaptation** – to support proportional, transparent, and non-intrusive interface responses.

CogniViz operates entirely on behavioral telemetry derived from standard browser events (e.g., pointer, input, focus, drag), avoiding physiological sensors or retrospective self-reports during task execution.

---

## High-Level Architecture

CogniViz follows a three-layer, event-driven architecture:

1. **Client / Browser Layer** – captures interaction events, aggregates behavioral metrics, renders predictions, and applies interface adaptations.
2. **Server / Inference Layer** – hosts the trained machine learning model, performs normalization and classification, and generates SHAP-based explanations.
3. **Adaptation Layer** – implements task-specific UI responses driven by inferred cognitive load and explanation signals.

The system executes as a continuous sensing–inference–explanation–adaptation loop with an end-to-end latency of approximately 150–400 ms per prediction cycle.

---

## 1. Client / Browser Layer

The client layer is implemented as a React-based web interface instrumented with native browser event listeners. It performs all sensing and primary feature aggregation locally.

### 1.1 Event Capture Module

The Event Capture Module instruments standard browser events:

- `pointermove`, `mousedown`, `mouseup`, `click`
- `input`, `change`, `keydown`, `keyup`
- `focus`, `blur`
- `dragstart`, `dragover`, `drop`
- `mouseenter`, `mouseleave`

These raw events are streamed into a local event buffer and time-stamped with millisecond resolution. No raw keystrokes or sensitive content leave the browser.

### 1.2 Event Processing Module

Raw interaction events are transformed into temporally structured activity segments using a rolling time window (150–300 ms). This module computes low-level interaction statistics, including:

- Input latencies and dwell times  
- Cursor trajectory length, velocity, and entropy  
- Idle bursts and hesitation intervals  
- Error and correction events  
- Hover oscillations and repeated transitions  

This temporal segmentation enables fine-grained tracking of interaction dynamics while maintaining computational efficiency.

### 1.3 Metric Extractor

The Metric Extractor aggregates low-level interaction statistics into higher-level behavioral features grounded in cognitive load theory and micro-interaction research. These include:

- Planning complexity indicators (e.g., scheduling difficulty, planning time ratio)  
- Conflict and constraint signals (e.g., constraint violation rate, budget management stress)  
- Uncertainty and indecision markers (e.g., decision reversals, hover oscillations)  
- Multitasking behavior (e.g., panel switching, concurrent interaction streams)  
- Recovery efficiency (e.g., speed and effectiveness of post-error correction)  
- Motor variability (e.g., mouse trajectory entropy)  

Only derived behavioral metrics are transmitted to the server. Raw interaction traces remain client-side, supporting privacy preservation and low bandwidth usage.

### 1.4 Load Indicator UI

The client renders a non-disruptive visual load indicator that reflects the current inferred cognitive state:

- Green – low load  
- Yellow – medium load  
- Red – high load  

This indicator updates automatically with each inference cycle and forms the basis for adaptive interface behavior.

---

## 2. Server / Inference Layer

The server layer hosts the machine learning inference service and explanation engine. It is implemented as a stateless FastAPI application.

### 2.1 Feature Normalization

Incoming behavioral metrics are normalized using precomputed training-set statistics to ensure consistent scaling across users, devices, and interaction styles. This prevents drift in feature magnitudes and stabilizes real-time predictions.

### 2.2 Random Forest Classifier

CogniViz employs a tuned Random Forest classifier trained to predict elevated cognitive load (binary classification: TLX > 60). The model:

- Captures non-linear interactions among behavioral features  
- Supports post-hoc explanation via SHAP  
- Generalizes across users under Leave-One-User-Out validation  
- Performs inference in approximately 5–10 ms per instance  

The model is pre-loaded into memory to minimize inference latency.

### 2.3 Real-Time SHAP Engine

For every prediction, CogniViz generates SHAP (SHapley Additive exPlanations) attributions that quantify the marginal contribution of each behavioral feature to the inferred load state.

These explanations:

- Support both global (model-level) and local (instance-level) interpretability  
- Reveal which interaction patterns drive elevated workload  
- Distinguish associative correlations from conditional predictive influence  
- Enable explanation-driven adaptation logic  

SHAP computation is optimized for real-time use by caching background distributions and restricting feature sets to those used in inference.

### 2.4 Inference API

The FastAPI service exposes a lightweight HTTPS endpoint that accepts JSON payloads of aggregated behavioral metrics and returns:

- Predicted cognitive load probability  
- Binary load classification  
- SHAP attribution vector  

The service is stateless and supports concurrent clients.

---

## 3. Adaptation Layer

The Adaptation Layer implements cognitively grounded, task-specific interface responses driven by inferred cognitive load and explanation signals.

### 3.1 Temporal Smoothing and Hysteresis

To prevent reactive or jittery adaptation, CogniViz applies temporal smoothing and hysteresis logic:

- Load state transitions require sustained evidence across multiple inference windows  
- Initial interaction periods are treated as calibration phases  
- Recovery to a lower load state requires sustained fluent interaction  

This design reflects the cognitive reality that workload emerges through breakdown–repair cycles rather than isolated pauses or single errors.

### 3.2 Task-Specific Adaptation Logic

CogniViz adapts interfaces proportionally and contextually:

- **Form Completion Tasks**  
  - Highlights valid input regions after repeated invalid entries  
  - Provides micro-guidance for persistent hesitation or correction loops  
  - Collapses secondary panels under sustained strain  

- **Exploratory Comparison Tasks**  
  - Introduces transient comparison overlays after sustained trade-off behavior  
  - Reduces filter density during high multitasking load  
  - Suppresses guidance during focused selection actions  

- **Planning and Scheduling Tasks**  
  - Highlights constraint conflicts after repeated violations  
  - Localizes guidance to the current subtask (e.g., specific time slots or budget components)  
  - Simplifies layout under sustained breakdown patterns  

Adaptations are lightweight DOM updates triggered only when workload probabilities exceed configurable thresholds.

### 3.3 Explanation-Driven Adaptation

SHAP attributions are used not only for transparency but also as control signals for adaptation:

- Planning-related features trigger scheduling guidance  
- Constraint-related features trigger conflict highlighting  
- Recovery-efficiency features modulate intervention aggressiveness  

This ensures that adaptations are psychologically aligned with the user’s observed difficulty rather than generic or task-agnostic.

---

## 4. End-to-End Interaction Flow

1. User interacts with the web interface  
2. Browser captures raw interaction events  
3. Event Processing Module aggregates low-level interaction statistics  
4. Metric Extractor derives behavioral features  
5. Features are transmitted to the inference server  
6. Server normalizes features and runs Random Forest inference  
7. SHAP explanations are generated  
8. Predictions and explanations are returned to the client  
9. Load Indicator UI updates  
10. Adaptation Layer applies task-specific UI responses  
11. Loop repeats every 150–400 ms  

---

## 5. Performance Characteristics

- **Inference latency (model only):** ~5–10 ms  
- **End-to-end loop latency:** 150–400 ms  
- **Client computation:** O(1) per window  
- **Server throughput:** supports concurrent clients  
- **Data transmitted:** derived behavioral metrics only  
- **Raw interaction storage:** client-side only  

This performance envelope satisfies real-time responsiveness requirements for interactive systems.

---

## 6. Privacy and Deployability

CogniViz is designed for privacy-preserving deployment:

- No raw keystrokes or content are transmitted  
- Only derived behavioral metrics leave the browser  
- No physiological sensors or specialized hardware required  
- No browser extensions or plugins required  
- Compatible with standard modern browsers  

The architecture supports scalable deployment across platforms and contexts without additional instrumentation.

---

## 7. Architectural Contributions

CogniViz introduces several architectural innovations:

1. **Sensor-free, real-time cognitive load inference** from natural interaction behavior  
2. **Explainability as a first-class architectural component**, not a post-hoc diagnostic  
3. **Closed-loop adaptive UI control** grounded in behavioral evidence  
4. **Browser-native deployment** without hardware dependencies  
5. **Explanation-driven adaptation logic** aligned with cognitive theory  

Together, these elements position CogniViz as an end-to-end, human-centered cognitive state modeling system suitable for real-world interactive environments.

---

## 8. Design Rationale

The architecture reflects three guiding principles:

- **Behavior over physiology:** prioritize scalable, unobtrusive sensing  
- **Interpretability over opacity:** support trust and design relevance  
- **Adaptation over diagnosis:** treat cognitive load as an actionable system signal  

By treating cognitive load as an emergent interaction phenomenon rather than a static task label, CogniViz aligns machine learning inference with human-centered interface design.

---

## 9. Summary

CogniViz implements a real-time, interpretable, and deployable cognitive load inference architecture grounded in natural interaction behavior. By uniting behavioral telemetry, explainable machine learning, and adaptive interface control within a single end-to-end pipeline, the system demonstrates a practical foundation for cognitively aware interactive systems that respond intelligently to users’ mental state without intrusive sensing.

