# CogniViz

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)  
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)  
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://react.dev/)

## Interpretable, Sensor-Free Cognitive Load Inference for Adaptive Interfaces

---

*A browser-native framework for inferring cognitive load from natural interaction behavior and enabling explanation-driven, human-centered interface adaptation.*

---

## Abstract

Cognitive load critically shapes how people interact with complex digital systems, influencing performance, error rates, and decision quality. Yet most interfaces remain blind to users’ moment-to-moment mental demands, relying on retrospective self-reports or intrusive physiological sensors that are impractical for everyday use.

This repository presents **CogniViz**, a sensor-free, real-time framework that infers cognitive load directly from natural interaction behavior and uses these inferences to support interpretable, cognitively grounded adaptive interfaces.

CogniViz models cognitive load from high-resolution browser telemetry—including cursor dynamics, hesitation patterns, error recovery, constraint violations, multitasking behavior, and planning pauses—captured during realistic web-based tasks. Using cognitively grounded behavioral features and a participant-independent Random Forest model, CogniViz achieves strong predictive performance (F1 = 0.87, ROC-AUC = 0.95) under Leave-One-User-Out validation when predicting elevated subjective workload (NASA-TLX > 60).

To ensure transparency and design relevance, CogniViz integrates SHAP-based explanations directly into the inference pipeline. These explanations reveal how specific interaction patterns drive inferred load states and are used as control signals for task-specific UI adaptation.

By uniting behavioral modeling, explainable machine learning, and adaptive interface design within a single end-to-end system, CogniViz demonstrates that cognitive load can be sensed, explained, and acted upon using interaction data alone—without reliance on intrusive sensors or opaque automation.

---

## How to Read This Repository

**Start here for a conceptual overview**, then explore:

- [`ARCHITECTURE.md`](ARCHITECTURE.md) — System design and data flow  
- [`MODEL.md`](MODEL.md) — Machine learning architecture and SHAP internals  
- [`DATA.md`](DATA.md) — Dataset structure, features, and labeling  
- [`EXPERIMENTS.md`](EXPERIMENTS.md) — Experimental protocols and evaluation setup  
- [`RESULTS.md`](RESULTS.md) — Empirical findings and interpretation  
- [`ADAPTATION.md`](ADAPTATION.md) — UI logic and HCI-theoretic grounding  
- [`INSIGHTS_AND_STORYTELLING.md`](INSIGHTS_AND_STORYTELLING.md) — Narrative synthesis and design meaning  
- [`SYSTEM.md`](SYSTEM.md) — Deployment and runtime architecture  
- [`ETHICS.md`](ETHICS.md) — Privacy, agency, consent, and responsible use  

---

## Core Idea

**Most interfaces respond to *what users do*.**  
**CogniViz responds to *how difficult interaction becomes*.**

At runtime, CogniViz:

1. **Captures natural interaction behavior** via standard browser events  
2. **Derives interpretable behavioral features** grounded in cognitive theory  
3. **Infers cognitive load in real time** using a nonlinear ML model  
4. **Generates SHAP explanations** for each prediction  
5. **Adapts the interface** based on explanation-driven control logic  

This separation makes cognitive state modeling:

- **Inspectable**  
- **Explainable**  
- **Actionable**  
- **Deployable without sensors**  

---

## System Architecture

CogniViz is a closed-loop Human–AI Interaction (HAI) system composed of:

### 1. Behavioral Sensing Layer  
Captures pointer, input, focus, drag, and hover events from the browser and aggregates them into cognitively grounded behavioral metrics.

### 2. Cognitive Load Inference Model  
A tuned Random Forest classifier predicts elevated workload (NASA-TLX > 60) using 16 interpretable behavioral features.

### 3. Explainability Engine  
TreeSHAP generates exact feature attributions for every inference, enabling both transparency and explanation-driven adaptation.

### 4. Adaptation Engine  
Applies proportional, task-specific UI changes based on sustained behavioral breakdown patterns and SHAP explanation signals.

**Key properties:**

- No physiological sensors  
- No raw content logging  
- No parametric policy learning  
- No opaque automation  
- No global UI simplification  

See [`ARCHITECTURE.md`](ARCHITECTURE.md) for details.

---

## Cognitive Load as an Interaction Phenomenon

CogniViz reframes cognitive load as:

> A dynamic interaction state emerging from sustained breakdown–repair cycles.

High cognitive load is driven primarily by:

- Constraint conflict  
- Scheduling difficulty  
- Budget trade-offs  
- Prolonged planning pauses  
- Multitasking overload  

Low cognitive load—even under complexity—is characterized by:

- Fluent execution  
- Rapid recovery  
- Efficient navigation strategies  

This reframing treats cognitive load as *behaviorally legible and design-actionable*.

---

## Interpretability as Infrastructure

CogniViz treats explainability as a **first-class system component**, not a post-hoc diagnostic.

SHAP explanations are used to:

- Justify cognitive load inferences  
- Drive task-specific adaptation logic  
- Distinguish productive effort from breakdown-induced strain  
- Support user trust and design relevance  

This reframes AI in interfaces from:

> “Predictor of internal states”  
to  
> “Interpreter of interaction dynamics.”

---

## Experiments and Evaluation

CogniViz is evaluated through:

### Controlled Task Study

- N = 25 participants  
- Three web-based tasks (Form Completion, Product Exploration, Travel Planning)  
- NASA-TLX subjective workload ground truth  
- 75 total task instances  

---

### Machine Learning Evaluation

- Leave-One-User-Out (LOUO) validation  
- Logistic Regression and Random Forest baselines  
- SHAP-based global and local explainability  
- Explanation-based clustering  

**Key result:**  
Random Forest achieves F1 = 0.87, ROC-AUC = 0.95.

See [`EXPERIMENTS.md`](EXPERIMENTS.md) and [`RESULTS.md`](RESULTS.md).

---

## Human–Centered Adaptation

Rather than reacting to scalar load scores, CogniViz adapts based on:

- Sustained behavioral breakdown patterns  
- Explanation dominance  
- Task context  
- Proportional intervention logic  

This avoids:

- Over-assistance  
- Learned helplessness  
- Pathologizing productive effort  
- Opaque automation  

See [`ADAPTATION.md`](ADAPTATION.md).

---

## Ethics, Responsibility, and Scope

This repository presents **minimal-risk, non-clinical research**.

- No physiological sensors  
- No raw keystrokes or content logging  
- No covert monitoring  
- No productivity surveillance  
- No manipulative adaptation  

CogniViz preserves:

- User agency  
- Interpretability  
- Proportional intervention  
- Explicit consent  

See [`ETHICS.md`](ETHICS.md) for detailed discussion.

---

## Repository Structure

```
├── README.md
├── docs/
│   ├── ARCHITECTURE.md
│   ├── MODEL.md
│   ├── DATA.md
│   ├── EXPERIMENTS.md
│   ├── RESULTS.md
│   ├── ADAPTATION.md
│   ├── INSIGHTS_AND_STORYTELLING.md
│   ├── SYSTEM.md
│   └── figures/
├── ETHICS.md
├── CODE_OF_CONDUCT.md
├── CONTRIBUTING.md
├── CITATION.cff
├── src/
├── experiments/
├── results/
└── tests/
```

---

## Reproducibility

- Participant-independent cross-validation  
- Controlled random seeds  
- Logged feature pipelines  
- Offline SHAP computation  
- Deterministic TreeSHAP explanations  

See [`REPRODUCIBILITY.md`](REPRODUCIBILITY.md) for step-by-step instructions.

---

## Intended Use

**Intended for:**

- Human–computer interaction research  
- Cognitive load modeling  
- Explainable AI in interfaces  
- Adaptive UI design  
- Human-centered AI systems  

**Not intended for:**

- Covert monitoring  
- Productivity surveillance  
- Manipulative interfaces  
- Clinical or diagnostic use  
- High-stakes decision systems  

---

## Citation

If you use or build on this work, please cite it as described in [`CITATION.cff`](../CITATION.cff).

---

## Summary

CogniViz demonstrates that cognitive load can be inferred, interpreted, and operationalized in real time using interaction behavior alone.

By uniting behavioral telemetry, explainable machine learning, and adaptive interface control within a single end-to-end framework, CogniViz provides a practical and human-centered foundation for cognitively aware interactive systems.

Rather than treating cognitive state as a hidden internal variable, CogniViz reframes it as a legible interaction phenomenon—making mental effort visible, explainable, and design-actionable.

---

**Last Updated**: January 2026  
**Repository Status**: Active research development | Preparing for preprint submission