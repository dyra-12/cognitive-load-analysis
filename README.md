# CogniViz

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)  
[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)  
[![FastAPI](https://img.shields.io/badge/FastAPI-0.100+-green.svg)](https://fastapi.tiangolo.com/)  
[![React](https://img.shields.io/badge/React-18+-61DAFB.svg)](https://react.dev/)

## Interpretable, Sensor-Free Cognitive Load Inference for Adaptive Interfaces

---

*A browser-native research framework for inferring cognitive load from natural interaction behavior and enabling explanation-driven, human-centered interface adaptation.*

---

## Abstract

Cognitive load critically shapes how users interact with complex digital systems, influencing performance, error rates, and decision quality. Yet most interfaces remain blind to users’ moment-to-moment mental demands, relying on retrospective self-reports or intrusive physiological sensors that are impractical for real-world deployment.

This repository presents **CogniViz**, a sensor-free, real-time framework that infers cognitive load directly from natural interaction behavior and uses these inferences to support interpretable, cognitively grounded adaptive interfaces.

CogniViz models cognitive load from high-resolution browser telemetry—including cursor dynamics, hesitation patterns, error recovery, constraint violations, multitasking behavior, and planning pauses—captured during three realistic web-based tasks. Using cognitively grounded behavioral features and a participant-independent Random Forest classifier, CogniViz achieves strong predictive performance (F1 = 0.87, ROC-AUC = 0.95) under Leave-One-User-Out validation when predicting elevated subjective workload (NASA-TLX > 60).

To ensure transparency and design relevance, CogniViz integrates SHAP-based explanations directly into the inference pipeline. These explanations reveal how specific interaction patterns drive inferred load states and are used as control signals for task-specific UI adaptation.

By uniting behavioral modeling, explainable machine learning, and adaptive interface design within a single end-to-end system, CogniViz demonstrates that cognitive load can be sensed, explained, and acted upon using interaction data alone—without reliance on intrusive sensors or opaque automation.

---

## Core Contribution

CogniViz reframes cognitive load as a **dynamic interaction state** rather than a static task label or retrospective self-report.

At runtime, CogniViz:

1. Captures natural interaction behavior via standard browser events  
2. Derives interpretable, cognitively grounded behavioral features  
3. Infers cognitive load in real time using a nonlinear ML model  
4. Generates SHAP explanations for each prediction  
5. Applies explanation-driven UI adaptation  

This separation makes cognitive state modeling:

- Inspectable  
- Explainable  
- Design-actionable  
- Deployable without sensors  

---

## Technical Summary

**Model**

- Random Forest classifier  
- 16 interpretable behavioral features  
- Binary cognitive load target  
- Ground truth: NASA-TLX (> 60 = High Load)  
- Validation: Leave-One-User-Out (LOUO)  

**Performance**

- F1 = 0.87  
- ROC-AUC = 0.95  
- Robust participant-independent generalization  

**Explainability**

- TreeSHAP for exact feature attributions  
- Global and local explanations  
- Explanation-based behavioral clustering  
- Explanations used as control signals for adaptation  

---

## Human-Centered Adaptation

CogniViz applies UI adaptations only under **sustained behavioral breakdown patterns**, not isolated hesitation.

Adaptation is:

- Proportional  
- Reversible  
- Task-specific  
- Explanation-driven  

The system distinguishes **productive cognitive effort** from **breakdown-induced strain**, avoiding over-assistance and pathologizing exploration.

---

## Experimental Evaluation

**Study Design**

- N = 25 participants  
- Three realistic web-based tasks:
  - Form Completion (low load)  
  - Product Exploration (medium load)  
  - Travel Planning (high load)  
- 75 total task instances  
- NASA-TLX subjective workload  

**Key Findings**

- Strong behavioral correlates of cognitive load  
- Robust participant-independent inference  
- Discrepancies reveal limits of subjective workload  
- Cognitive load emerges from breakdown–repair cycles  

---

## Ethics and Scope

CogniViz is designed as **minimal-risk, human-centered research**.

- No physiological sensors  
- No raw keystrokes or content logging  
- No covert monitoring  
- No productivity surveillance  
- No manipulative adaptation  
- Explicit user consent required  

See [`ETHICS.md`](ETHICS.md) for detailed discussion.

---

## Repository Navigation

This README provides a high-level overview for rapid review.

For the full technical narrative, experimental detail, and system documentation, see:

> **[`docs/README_RESEARCH.md`](docs/README_RESEARCH.md)**  
> *(Primary research documentation entry point)*

Additional technical documents:

- `docs/ARCHITECTURE.md` — System design  
- `docs/MODEL.md` — ML + SHAP internals  
- `docs/DATA.md` — Dataset + features  
- `docs/EXPERIMENTS.md` — Evaluation protocol  
- `docs/RESULTS.md` — Empirical findings  
- `docs/ADAPTATION.md` — UI logic + HCI theory  
- `docs/SYSTEM.md` — Deployment + runtime  
- `ETHICS.md` — Privacy, agency, consent  

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

## Summary

CogniViz demonstrates that cognitive load can be inferred, interpreted, and operationalized in real time using interaction behavior alone.

By uniting behavioral telemetry, explainable machine learning, and adaptive interface control within a single end-to-end framework, CogniViz provides a practical and human-centered foundation for cognitively aware interactive systems.

Rather than treating cognitive state as a hidden internal variable, CogniViz reframes it as a legible interaction phenomenon—making mental effort visible, explainable, and design-actionable.

---

**Repository Status**: Active research development  
**Documentation Entry Point**: [`docs/README_RESEARCH.md`](docs/README_RESEARCH.md)  
**Last Updated**: January 2026  
