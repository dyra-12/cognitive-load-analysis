# Analysis

This folder contains statistical analyses examining the relationship between user behavior and cognitive load. It includes repeated measures ANOVA testing NASA-TLX scores across tasks, correlation analyses between interaction features and subjective workload ratings, and behavioral pattern discovery identifying common interaction sequences associated with different load levels.

## Structure

### 📓 `notebooks/`
Interactive analysis notebooks:
- `behavioral_patterns_notebook.ipynb` - Behavioral pattern discovery and visualization
- `tlx_anova_analysis.ipynb` - NASA-TLX repeated measures ANOVA analysis

### 📊 `results/`
Statistical analysis outputs:
- ANOVA results and post-hoc tests
- Correlation analyses (feature-TLX relationships)
- Task-wise descriptive statistics
- Detailed interpretation summaries

### 🔬 `statistics/`
Python scripts for statistical analysis:
- `run_anova.py` - Execute repeated measures ANOVA
- `run_correlations.py` - Compute feature-TLX correlations
- `behavioral_pattern_discovery.py` - Pattern mining from behavioral data
- `repeated_measures_anova.py` - Core ANOVA implementation

## Quick Start

**View analysis results**: Check `results/` for CSV and TXT summaries  
**Run statistical tests**: Execute scripts in `statistics/`  
**Interactive exploration**: Open notebooks in `notebooks/`
