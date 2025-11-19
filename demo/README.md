# 📁 Demo — Cognitive Load Interaction Examples

> A comprehensive visual demonstration of task scenarios, UI mockups, and adaptive interface behavior from the thesis project.

---

## 📘 Overview

The `demo/` directory contains all visual artifacts used to illustrate the effects of cognitive load across different tasks and how adaptive interfaces respond in real time. This collection serves as a visual companion to the thesis, bridging theory and practice.

### Purpose

This folder supports the thesis in three key ways:

1. **Task Design Visualization** — Shows the original task designs (A/B/C tasks) and their cognitive requirements
2. **Load Variation Analysis** — Demonstrates how cognitive load changes with UI complexity and interaction patterns
3. **Adaptive System Behavior** — Illustrates an adaptive UI system responding to predicted cognitive load in real time

### Theoretical Foundation

These examples are directly grounded in:

- **Behavioral Features** — Engineered in Phase 2 from raw interaction data
- **Predictive Modeling** — Cognitive load predictions from the Random Forest model
- **Interpretability Analysis** — SHAP feature importance and cluster analysis
- **Cognitive Load Theory** — Decomposition into intrinsic, extraneous, and germane load

---

## 🚀 How To Use

| Action | Description |
|--------|-------------|
| **Explore Scenarios** | Open the Markdown storyboards in `01_scenarios/` to understand task contexts |
| **Review Mockups** | Browse UI mockups under `02_mockups/` organized by task type |
| **Study Walkthroughs** | Follow end-to-end scenarios in `03_scenario_walkthroughs/` |
| **Present Findings** | Use these assets directly in slides, papers, and thesis chapters |

---

## 📂 Folder Structure
```
demo/
├── 01_scenarios/              # Task storyboards showing load progression
├── 02_mockups/                # UI designs organized by task type
└── 03_scenario_walkthroughs/  # Complete narratives from intent to outcome
```

---

## 📋 Scenarios (`01_scenarios/`)

These Markdown storyboards illustrate how cognitive load scales with task demands:

| Scenario | Task Type | Load Level | Description |
|----------|-----------|------------|-------------|
| `scenario_1_form_lowload.md` | Form Entry | **Low** | Baseline interaction with minimal complexity |
| `scenario_2_product_medload.md` | Product Exploration | **Medium** | Multi-criteria decision-making with filters |
| `scenario_3_travel_highload.md` | Travel Planning | **High** | Complex scheduling with conflicting constraints |

### Key Behavioral Indicators

Each scenario documents:
- **Interaction patterns** — Click sequences, hesitations, corrections
- **Temporal dynamics** — Pause durations, session length, pacing
- **Cognitive markers** — Back navigation, input corrections, exploration breadth

---

## 🎨 Mockups (`02_mockups/`)

High-fidelity UI states organized by task type, showing progression from simple to complex:

### Forms (`forms/`)
- **Minimal** → Simple field entry with clear progression
- **Moderate** → Multi-step forms with validation feedback
- **Overloaded** → Complex conditional logic with frequent corrections

**Behavioral markers**: Hesitation rates, correction frequency, field sequencing patterns

### Product Exploration (`product_exploration/`)
- **Simple** → Single-attribute browsing with clear options
- **Multi-filter** → Simultaneous criteria evaluation with comparisons
- **Overwhelming** → Choice paralysis with excessive options and attributes

**Behavioral markers**: Filter toggling, comparison depth, decision latency

### Travel Planning (`travel_planning/`)
- **Guided** → Linear booking flow with minimal constraints
- **Semi-complex** → Multi-step planning with budget considerations
- **Conflict-heavy** → Schedule optimization with competing priorities

**Behavioral markers**: Scheduling friction, constraint violations, backtracking frequency

---

## 📖 Scenario Walkthroughs (`03_scenario_walkthroughs/`)

End-to-end narratives demonstrating the complete interaction lifecycle:
```
User Intent → Interaction Patterns → Behavioral Signals → 
Load Prediction → UI Adaptation → Design Implications
```

### What Each Walkthrough Contains

- **Context Setting** — User goals and task requirements
- **Interaction Sequence** — Step-by-step behavioral log
- **Feature Extraction** — How behaviors map to cognitive load features
- **Model Response** — Predicted load level and confidence
- **Adaptive Action** — Interface modifications based on prediction
- **Design Rationale** — Why these adaptations reduce extraneous load

Use these walkthroughs to:
- Communicate the full research story in presentations
- Ground design decisions in empirical evidence
- Demonstrate the practical impact of cognitive load modeling

---

## 🔗 Grounding & References

### Data Processing & Feature Engineering
- **Behavioral Features**: `src/data_preparation/compute_features.py`
- **Pattern Discovery**: `analysis/statistics/behavioral_pattern_discovery.py`

### Modeling & Evaluation
- **Training Pipeline**: `src/modeling/train_louo_random_forest.py`
- **Results**: `results/modeling/`

### Interpretability & Insights
- **SHAP Analysis**: `docs/SHAP_Insights.md`
- **Visualizations**: `figures/shap/`
- **Interactive Notebooks**: `notebooks/SHAP_visualization.ipynb`

### Statistical Validation
- **TLX Analysis**: `analysis/notebooks/tlx_anova_analysis.ipynb`
- **Results Summary**: `analysis/results/`

---

## 📝 Notes

- All paths are relative to the repository root
- If you add or rename assets, update this README to maintain accuracy
- For questions about specific scenarios or mockups, refer to the corresponding analysis notebooks
- These materials are designed to be modular — use individual components or complete walkthroughs as needed

---

## 🏷️ Tags

![Demo](https://img.shields.io/badge/Demo-UI_Scenarios-blue)
![Mockups](https://img.shields.io/badge/Mockups-Low/Med/High_Load-green)
![Adaptive UI](https://img.shields.io/badge/Adaptive_UI-Enabled-orange)
![Cognitive Load](https://img.shields.io/badge/Cognitive_Load-Behavioral_Model-purple)
![Diagrams](https://img.shields.io/badge/Includes-Diagrams_&_Storyboards-yellow)

---

**Last Updated**: November 2025  
**Maintainer**: Thesis Project Team  
**License**: Research Use Only