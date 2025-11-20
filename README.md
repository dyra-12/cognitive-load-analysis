# Cognitive Load Analysis in Multi-Task Interaction Environments

**A Behavioral Modeling, UX Analytics, and Explainable AI Framework**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Documentation](https://img.shields.io/badge/docs-latest-brightgreen.svg)](docs/00_overview.md)

---

## Abstract

This repository presents a comprehensive research framework for measuring and predicting cognitive load in multi-task digital environments. Using a combination of behavioral telemetry, NASA-TLX self-report, machine learning modeling, and SHAP-based interpretability, the study demonstrates that interaction patterns—such as scheduling complexity, constraint violations, and resource-management strain—serve as strong indicators of mental workload.

**Key Achievement:** A tuned Random Forest classifier achieved **96% accuracy** under Leave-One-User-Out (LOUO) validation, with SHAP analysis revealing interpretable cognitive-load signatures.

---

## Table of Contents

- [Research Context](#research-context)
- [Experimental Design](#experimental-design)
- [Repository Structure](#repository-structure)
- [Principal Findings](#principal-findings)
- [Methodology](#methodology)
- [Design Guidelines](#design-guidelines)
- [Dataset Card](#dataset-card)
- [Reproducibility](#reproducibility)
- [Citation](#citation)
- [Contact](#contact)

---

## Research Context

This project explores whether behavioral signals during interactive digital tasks can be used to predict cognitive load reliably and transparently.

### Key Research Questions

1. **Which behaviors are most indicative of high cognitive load?**
2. **Can machine learning predict load using behavioral features alone?**
3. **How can this knowledge inform adaptive UI design?**

---

## Experimental Design

Participants completed three web-based tasks intentionally varied by difficulty:

| Task | Description | Cognitive Demands | Expected Load |
|------|-------------|-------------------|---------------|
| **Task 1: Form Entry** | Simple address form | Minimal working memory | Low |
| **Task 2: Product Exploration** | Browsing, filtering, comparing items | Decision-making under uncertainty | Medium |
| **Task 3: Travel Planning** | Budgeting, scheduling, constraint handling | High complexity & resource allocation | High |

### Data Collection

**Telemetry captured:**
- Mouse events (clicks, movements, hovers)
- Keyboard activity
- Drag actions
- Constraint errors
- Idle periods

**Self-Report:** NASA-TLX administered after each task

---

## Repository Structure

```
.
├── data/
│   ├── raw/                      # Original telemetry logs
│   ├── processed/                # Cleaned and engineered features
│   └── examples/                 # Sample data for testing
│
├── src/
│   ├── data_preparation/         # ETL and preprocessing scripts
│   ├── modeling/                 # ML training and validation
│   ├── interpretation/           # SHAP analysis and explanations
│   └── utils/                    # Helper functions
│
├── analysis/
│   ├── notebooks/                # Jupyter exploratory analysis
│   ├── statistics/               # ANOVA, correlation tests
│   └── results/                  # Model outputs and metrics
│
├── demo/
│   ├── 01_scenarios/             # Task scenario descriptions
│   ├── 02_mockups/               # UI wireframes
│   └── 03_adaptive_ui_examples/  # Interactive adaptive UI prototypes
│
├── docs/
│   ├── 00_overview.md            # Research methodology
│   ├── reproducibility.md        # Step-by-step reproduction guide
│   ├── feature_correlation_summary.md
│   ├── ML_Insights.md            # Model architecture and tuning
│   ├── SHAP_Insights.md          # Interpretability analysis
│   ├── insights.md               # Key findings summary
│   └── threats_to_validity.md    # Limitations and ethical considerations
│
├── figures/
│   ├── TLX/                      # NASA-TLX visualizations
│   ├── correlations/             # Feature correlation heatmaps
│   ├── pipeline/                 # Processing flowcharts
│   └── shap/                     # SHAP importance plots
│
├── modeling_dataset.csv          # Final engineered dataset
├── requirements.txt              # Python dependencies
├── run_all.py                    # Master execution script
└── README.md                     # This file
```

---

## Principal Findings

### 1. Task Difficulty Validation

Repeated-measures ANOVA confirmed significant load differences:

**F(2,148) = 87.3, p < .001, η² = 0.54**

**Load Order:** Task 1 < Task 2 < Task 3

![NASA-TLX Distribution](figures/TLX/tlx_distribution_by_task.png)

*Figure 1: NASA-TLX score distribution demonstrates clear separation between task difficulty levels*

---

### 2. Behavioral Correlates of Cognitive Load

Top correlated features:

| Feature | Pearson's r | Interpretation |
|---------|-------------|----------------|
| **Scheduling difficulty** | .81 | Temporal & constraint complexity |
| **Constraint violation rate** | .80 | Cognitive strain under rule conflict |
| **Budget management stress** | .80 | Resource-allocation difficulty |
| **Multitasking load** | .73 | Fragmented attention |
| **Idle time ratio** | .69 | Processing pauses |

![Feature Correlation Heatmap](figures/correlations/top_features_correlation.png)

*Figure 2: Correlation heatmap showing relationship between behavioral features and NASA-TLX scores*

---

### 3. Machine Learning Model Performance

**Tuned Random Forest (LOUO validation):**

| Metric | Score |
|--------|-------|
| **Accuracy** | 0.96 |
| **Precision** | 0.94 |
| **Recall** | 0.89 |
| **F1-score** | 0.91 |
| **ROC-AUC** | 0.95 |

![Confusion Matrix](figures/pipeline/confusion_matrix.png)

*Figure 3: Confusion matrix demonstrating strong classification performance*

![ROC Curve](figures/pipeline/roc_curve.png)

*Figure 4: ROC curve showing excellent discrimination (AUC = 0.95)*

---

### 4. SHAP Interpretability

![SHAP Feature Importance](figures/shap/shap_global_importance.png)

*Figure 5: SHAP global feature importance reveals key cognitive load predictors*

**Top SHAP predictors:**
1. Scheduling difficulty
2. Constraint violation rate
3. Budget management stress
4. Idle time variance
5. Mouse movement entropy

![SHAP User Profiles](figures/shap/shap_user_profiles.png)

*Figure 6: Two distinct SHAP-based user profiles emerged: efficient/low-load (left) and overloaded/high-load (right)*

---

## Methodology

### Comprehensive Documentation

For detailed methodology, see:

- **[Overview](docs/00_overview.md)** - Research design and approach
- **[Feature Correlation Summary](docs/feature_correlation_summary.md)** - Statistical relationships
- **[ML Insights](docs/ML_Insights.md)** - Model architecture and tuning
- **[SHAP Insights](docs/SHAP_Insights.md)** - Explainability analysis

### Pipeline Overview

```mermaid
graph LR
    A[Raw Telemetry] --> B[Preprocessing]
    B --> C[Feature Engineering]
    C --> D[Statistical Analysis]
    D --> E[ML Modeling]
    E --> F[SHAP Interpretation]
    F --> G[Design Guidelines]
```

![Processing Pipeline](figures/pipeline/methodology_flowchart.png)

*Figure 7: End-to-end processing pipeline from data collection to actionable insights*

**Coverage:**
- ✔ Data collection protocols
- ✔ Feature engineering techniques
- ✔ Statistical hypothesis testing
- ✔ ML model selection and validation
- ✔ SHAP-based interpretability

---

## Design Guidelines

### Adaptive UI Rules Derived from Cognitive Load Signals

#### When High Load is Detected
**Condition:** `scheduling_difficulty > 0.6`

**Interventions:**
- 🤖 Offer auto-scheduling or smart snapping
- 📉 Reduce visible options
- 🎯 Add progressive disclosure
- 💡 Provide contextual hints

#### When Hesitation Behaviors Arise
**Condition:** `form_hesitation_index > 2s`

**Interventions:**
- ✂️ Simplify input fields
- 🏷️ Strengthen label affordances
- ✅ Add inline validation
- 📝 Provide examples

#### When Decision Uncertainty is Detected
**Condition:** High `rapid_hovers` (>5/min)

**Interventions:**
- 📊 Add quick-compare panels
- 🎯 Highlight key differentiators
- 🔍 Reduce filter complexity
- 💡 Show recommended options

![Adaptive UI Example](demo/03_adaptive_ui_examples/adaptive_interface_preview.png)

*Figure 8: Example adaptive interface responding to detected cognitive load*

### Implementation

These rules are implemented in interactive prototypes:
- See: [`/demo/03_adaptive_ui_examples/`](demo/03_adaptive_ui_examples/)

---

## Dataset Card

### Dataset Overview

| Property | Value |
|----------|-------|
| **Name** | `modeling_dataset.csv` |
| **Rows** | 75 |
| **Columns** | 47 behavioral features + TLX + labels |
| **Tasks** | Form entry, product filtering, travel planning |
| **Target Variable** | `High Load` (TLX > 60) |

### Intended Use

- ✅ Cognitive load modeling
- ✅ Behavioral UX analysis
- ✅ Explainable AI experiments
- ✅ Adaptive UI research
- ✅ Educational purposes

### Ethical Notes

- ✔️ **Fully anonymized** - No personal identifiers
- ✔️ **Privacy-preserving** - Time-stamped behavioral telemetry only
- ✔️ **Consent obtained** - All participants provided informed consent
- ✔️ **IRB approved** - Study protocol reviewed and approved

### Sample Features

```python
# Behavioral Features (Examples)
- scheduling_difficulty: float [0-1]
- constraint_violation_rate: float [0-1]
- budget_management_stress: float [0-1]
- form_hesitation_index: float (seconds)
- mouse_movement_entropy: float
- idle_time_ratio: float [0-1]
- rapid_hovers_per_minute: int
```

---

## Reproducibility

### Environment Setup

```bash
# Clone repository
git clone https://github.com/yourusername/cognitive-load-analysis.git
cd cognitive-load-analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run Complete Pipeline

```bash
python run_all.py
```

**This executes:**
1. ✅ Data preprocessing
2. ✅ Feature engineering
3. ✅ ANOVA + correlation analysis
4. ✅ Random Forest training
5. ✅ SHAP analysis
6. ✅ Figure generation

### Step-by-Step Reproduction

For detailed instructions:
➡️ **[Reproducibility Guide](docs/reproducibility.md)**

### System Requirements

- **Python:** 3.8+
- **RAM:** 8GB minimum
- **Storage:** 2GB available space
- **OS:** Windows, macOS, Linux

---

## Citation

If you use this work in your research, please cite:

```bibtex
@misc{dyra2025cogload,
  title={Cognitive Load Analysis in Multi-Task Interaction Environments: 
         A Behavioral Modeling, UX Analytics, and Explainable AI Framework},
  author={Dyra},
  year={2025},
  howpublished={\url{https://github.com/yourusername/cognitive-load-analysis}},
  note={Accessed: 2025-11-20}
}
```

---

## Contact

**Dyra**  
📧 [your.email@domain.com](mailto:your.email@domain.com)  
🔗 [GitHub Profile](https://github.com/yourusername)  
🐦 [Twitter](https://twitter.com/yourhandle)  
💼 [LinkedIn](https://linkedin.com/in/yourprofile)

---

## Ethical Considerations & Limitations

This research acknowledges several important considerations:

- **Sample Size:** Limited to 25 participants
- **Task Generalizability:** Three specific task types
- **Self-Report Bias:** NASA-TLX subject to individual interpretation
- **Temporal Validity:** Behavioral patterns may shift with user experience

For comprehensive discussion:
➡️ **[Threats to Validity](docs/threats_to_validity.md)**

---

## Acknowledgments

We thank all participants who contributed their time and cognitive effort to this study. Special thanks to the HCI research community for valuable feedback during development.

---

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**⭐ Star this repository if you find it useful!**

![Research Workflow](figures/pipeline/research_workflow_banner.png)

*Building the future of adaptive interfaces through explainable AI*

</div>