# 🧠 CogniViz

**Real-Time Cognitive Load Detection from Behavioral Interaction Patterns**

CogniViz is a sensor-free, behavior-based framework that detects user cognitive load in real time using everyday browser interactions (mouse, keyboard, cursor dynamics). It enables adaptive user interfaces that respond intelligently to mental effort—without EEG, eye tracking, or physiological sensors.

---

## 🚀 Why CogniViz?

Most cognitive load detection systems rely on intrusive hardware or lab-only setups. CogniViz demonstrates that standard web interaction telemetry alone is sufficient, interpretable, and deployable in real interfaces.

**Key contributions:**

- Cognitive load prediction using only behavioral signals
- User-independent modeling (no personalization leakage)
- SHAP-based interpretability aligned with cognitive load theory
- Design-ready insights for adaptive UI systems

---

## 📊 Key Results

| Metric | Value |
|--------|-------|
| **Participants** | 25 |
| **Tasks per participant** | 3 (low → medium → high load) |
| **Total samples** | 75 |
| **Validation method** | Leave-One-User-Out (LOUO) |

### Model Performance (Random Forest)

- **Accuracy:** 0.96
- **F1-score (LOUO mean):** 0.82
- **ROC-AUC:** 0.95

### Strongest Behavioral Predictors

1. Scheduling difficulty
2. Constraint violation rate
3. Budget management stress
4. Idle time ratio

These results show that cognitive load can be inferred reliably from behavior alone.

---

## 🧩 What's Inside This Repository?

- Behavioral feature engineering from raw interaction logs
- Statistical validation (NASA-TLX, repeated-measures ANOVA)
- Machine learning models with user-independent evaluation
- SHAP explanations (global, local, clustering)
- Adaptive UI design implications
- Full reproducibility pipeline

---

## 📁 Repository Navigation

### Start Here
📘 **[Full Research Report](docs/research_report.md)**

### Core Documentation

- **[Methodology](docs/methodology.md)** - Research design and experimental setup
- **[System Architecture](docs/system_architecture.md)** - Technical implementation details
- **[ML Results](docs/ML_Insights.md)** - Model performance and evaluation
- **[SHAP Interpretability](docs/SHAP_Insights.md)** - Feature importance and explanations
- **[Behavioral Metrics](docs/behavioral_metrics.md)** - Feature definitions and rationale
- **[Reproducibility Guide](docs/reproducibility.md)** - How to replicate experiments
- **[Ethics Statement](docs/ethics_statement.md)** - Privacy and responsible use
- **[Threats to Validity](docs/threats_to_validity.md)** - Limitations and constraints

---

## 🔁 Reproducibility

All experiments can be reproduced end-to-end:
```bash
pip install -r requirements.txt
python run_all.py
```

See **[docs/reproducibility.md](docs/reproducibility.md)** for full details.

---

## ⚖️ Ethics & Responsible Use

- Non-invasive behavioral data only
- No raw keystroke content or personal identifiers stored
- IRB-exempt, minimal-risk study with informed consent
- Full anonymization and privacy safeguards

Details: **[docs/ethics_statement.md](docs/ethics_statement.md)**

---

## 🧠 Research Positioning

CogniViz sits at the intersection of:

- **Human-Computer Interaction (HCI)**
- **Cognitive Load Theory**
- **Explainable Machine Learning**
- **Human-Centered AI**

It is designed as a research artifact, not a commercial product.

---

## 📬 Contact

For questions, feedback, or collaboration:

- Open a [GitHub Issue](../../issues)
- Or contact **Dyra**

---

## ⭐ Star This Repository

If you find this work useful, consider starring the repository to support open research in cognitive load detection and human-centered AI.

---


