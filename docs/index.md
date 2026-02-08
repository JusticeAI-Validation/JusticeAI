# JusticeAI

**Fairness Analysis for ML in Production**

JusticeAI is a Python library for evaluating and monitoring fairness in machine learning models, with a focus on production environments and Brazilian compliance requirements (LGPD/BACEN).

## Key Features

✨ **Simple API** - One-line fairness audits
📊 **Beautiful Reports** - Interactive HTML reports with visualizations
🎯 **Production-Ready** - Built for real-world ML systems
🇧🇷 **LGPD Compliant** - Brazilian data protection and banking regulations
🔧 **Framework Agnostic** - Works with sklearn, XGBoost, LightGBM, and more
📈 **Comprehensive Metrics** - Pre-training and post-training fairness metrics

## Quick Example

```python
from justiceai import audit
from sklearn.ensemble import RandomForestClassifier

# Train your model
model = RandomForestClassifier()
model.fit(X_train, y_train)

# Audit fairness with one line
report = audit(
    model=model,
    X=X_test,
    y_true=y_test,
    sensitive_attrs=gender,
    output_path='fairness_report.html',
    show=True
)

# Check results
print(f"Fairness Score: {report.get_overall_score()}/100")
print(f"Passes Fairness: {report.passes_fairness()}")
```

## Installation

```bash
pip install justiceai
```

For development:

```bash
git clone https://github.com/JusticeAI-Validation/JusticeAI.git
cd JusticeAI
poetry install
```

## Core Components

### FairnessEvaluator

High-level API for comprehensive fairness evaluation:

```python
from justiceai import FairnessEvaluator

evaluator = FairnessEvaluator(fairness_threshold=0.05)
report = evaluator.evaluate(model, X_test, y_test, sensitive_attrs)
```

### Fairness Metrics

**Pre-training metrics:**
- Class Balance
- Concept Balance (correlation with sensitive attributes)
- KL Divergence
- JS Divergence

**Post-training metrics:**
- Statistical Parity Difference
- Disparate Impact Ratio
- Equal Opportunity Difference
- Equalized Odds
- Calibration by Group

### Interactive Reports

Generate beautiful HTML reports with:
- Overall fairness score
- Metric breakdowns by group
- Interactive visualizations
- Actionable recommendations

## Use Cases

### Credit Risk Assessment
Ensure fair loan decisions across demographic groups

### Hiring Systems
Validate fairness in recruitment ML models

### Healthcare Predictions
Monitor fairness in medical outcome predictions

### Regulatory Compliance
Meet LGPD and BACEN fairness requirements

## Why JusticeAI?

### For Data Scientists
- **Easy Integration**: Works with your existing ML workflow
- **Clear Insights**: Understand exactly where bias exists
- **Quick Iteration**: Fast feedback during model development

### For ML Engineers
- **Production Ready**: Built for real-world systems
- **Framework Agnostic**: Adapters for all major ML frameworks
- **Performance**: Efficient metrics calculation with caching

### For Compliance Teams
- **LGPD Compliance**: Meets Brazilian data protection requirements
- **BACEN Guidelines**: Follows banking regulation standards
- **Audit Trail**: Complete documentation of fairness assessments

## Getting Started

1. [Installation Guide](getting-started/installation.md) - Get up and running
2. [Quick Start](getting-started/quickstart.md) - Your first fairness audit
3. [Basic Concepts](getting-started/concepts.md) - Understand fairness metrics
4. [Tutorials](tutorials/index.md) - In-depth examples

## Community & Support

- 📖 [Documentation](https://justiceai-validation.github.io/JusticeAI/)
- 🐛 [Issue Tracker](https://github.com/JusticeAI-Validation/JusticeAI/issues)
- 💬 [Discussions](https://github.com/JusticeAI-Validation/JusticeAI/discussions)

## License

MIT License - see [LICENSE](https://github.com/JusticeAI-Validation/JusticeAI/blob/main/LICENSE) for details.

## Citation

If you use JusticeAI in your research, please cite:

```bibtex
@software{justiceai2026,
  title = {JusticeAI: Fairness Analysis for ML in Production},
  author = {Haase, Gustavo},
  year = {2026},
  url = {https://github.com/JusticeAI-Validation/JusticeAI}
}
```
