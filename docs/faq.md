# Frequently Asked Questions

## General Questions

### What is JusticeAI?

JusticeAI is a Python library for evaluating fairness in machine learning models. It provides metrics, reports, and tools to identify and address bias in ML systems, with a focus on production environments and Brazilian compliance (LGPD/BACEN).

### Who should use JusticeAI?

- **Data Scientists** developing ML models
- **ML Engineers** deploying models to production
- **Compliance Teams** ensuring regulatory compliance
- **Product Managers** responsible for ethical AI

### What makes JusticeAI different?

- ✨ **Simple API**: One-line fairness audits
- 🇧🇷 **Brazilian Compliance**: LGPD and BACEN focused
- 📊 **Production Ready**: Built for real-world systems
- 🎨 **Beautiful Reports**: Interactive HTML visualizations
- 🔧 **Framework Agnostic**: Works with any ML framework

## Installation & Setup

### What Python version do I need?

Python 3.11 or higher is required.

### Can I use JusticeAI with my existing ML framework?

Yes! JusticeAI works with:
- scikit-learn (built-in)
- XGBoost (with adapter)
- LightGBM (with adapter)
- Any model with a `predict()` method

### How do I install optional dependencies?

```bash
# XGBoost support
pip install justiceai[xgboost]

# LightGBM support
pip install justiceai[lightgbm]

# All optional dependencies
pip install justiceai[all]
```

## Usage Questions

### What is a "sensitive attribute"?

A sensitive attribute (also called protected attribute) is a feature that should not influence model decisions, such as:
- Gender
- Race/ethnicity
- Age
- Religion
- Sexual orientation

### Can I analyze multiple sensitive attributes?

Currently, JusticeAI analyzes one sensitive attribute at a time. Pass multiple attributes as a dictionary, and the first one will be used:

```python
report = audit(
    model, X, y,
    sensitive_attrs={'gender': gender, 'age': age}
)
```

Intersectional analysis (multiple attributes simultaneously) is planned for a future release.

### What fairness threshold should I use?

The default threshold of 0.05 (5%) is recommended by LGPD guidelines. Adjust based on your requirements:

- **Strict**: 0.02 (2%)
- **Standard**: 0.05 (5%) - Default
- **Lenient**: 0.10 (10%)

```python
evaluator = FairnessEvaluator(fairness_threshold=0.05)
```

### How is the overall fairness score calculated?

The score (0-100) is based on:
1. Number of fairness metric violations
2. Severity of violations
3. Pre-training data quality

Higher scores indicate better fairness.

### What does "passes fairness" mean?

A model passes fairness if no metrics exceed the fairness threshold:
- Statistical Parity Difference < threshold
- Equal Opportunity Difference < threshold
- Disparate Impact ≥ 0.80
- Other metrics within acceptable ranges

### Can I use JusticeAI with pre-computed predictions?

Yes! Use `evaluate_predictions()`:

```python
report = evaluator.evaluate_predictions(
    y_true=y_test,
    y_pred=predictions,
    sensitive_attrs=gender,
    y_pred_proba=probabilities  # Optional
)
```

## Metrics Questions

### Which fairness metric should I use?

It depends on your use case:

| Use Case | Recommended Metric |
|----------|-------------------|
| Hiring | Disparate Impact (80% rule) |
| Loan Approval | Equal Opportunity |
| Medical Diagnosis | Equalized Odds |
| Marketing | Statistical Parity |
| Risk Scoring | Calibration |

See [Basic Concepts](getting-started/concepts.md) for details.

### Why can't I satisfy all fairness metrics?

Due to the [Fairness Impossibility Theorem](https://arxiv.org/abs/1609.05807), it's mathematically impossible to satisfy all fairness definitions simultaneously (except in trivial cases).

You must choose which metric(s) are most important for your use case.

### What's the difference between pre-training and post-training metrics?

- **Pre-training metrics**: Analyze the dataset before training (class balance, correlations)
- **Post-training metrics**: Analyze model predictions (statistical parity, equal opportunity)

Both are important for comprehensive fairness evaluation.

### What is the 80% rule (Disparate Impact)?

From US Equal Employment Opportunity Commission: the selection rate for the unprivileged group should be at least 80% of the rate for the privileged group.

Example:
- 60% of men approved → 60% × 0.80 = 48%
- Women approval rate must be ≥ 48%

## Reports & Visualization

### How do I save a report?

```python
# During audit
report = audit(model, X, y, gender, output_path='report.html')

# After evaluation
report.save_html('report.html')
```

### How do I view a report in the browser?

```python
# Automatically open in browser
report = audit(model, X, y, gender, show=True)

# Or manually
report.show()
```

### Can I customize the report?

Currently, reports use a standard template. Custom templates and styling are planned for a future release.

### Can I export results to JSON/CSV?

```python
# Get summary as dictionary
summary = report.get_summary()

# Convert to JSON
import json
with open('summary.json', 'w') as f:
    json.dump(summary, f)

# Get issues
issues = report.get_issues()
```

## Compliance Questions

### Is JusticeAI LGPD compliant?

JusticeAI helps you achieve LGPD compliance by providing fairness metrics and audit trails. However, compliance also requires:
- Proper data governance
- Privacy impact assessments
- Data protection policies

Consult with legal experts for complete compliance.

### What about BACEN regulations?

JusticeAI follows BACEN guidelines for ML fairness in banking systems. See [Compliance Guide](guide/compliance.md) for details.

### Can JusticeAI be used for regulatory audits?

Yes! The HTML reports provide documentation suitable for audits, including:
- Complete metric calculations
- Fairness violations identified
- Recommendations for improvement
- Timestamp and versioning

## Performance Questions

### Is JusticeAI fast enough for production?

Yes! JusticeAI is designed for production use with:
- Efficient metric calculations
- Caching for repeated analyses
- Minimal dependencies

### Can I use JusticeAI in a CI/CD pipeline?

Absolutely! Example:

```python
# In your test suite
def test_model_fairness():
    report = audit(model, X_test, y_test, sensitive_attrs)
    assert report.passes_fairness(), "Model failed fairness check"
    assert report.get_overall_score() >= 70, "Fairness score too low"
```

### How long does evaluation take?

Typical evaluation times:
- **Small datasets** (< 10k rows): < 1 second
- **Medium datasets** (10k-100k): 1-5 seconds
- **Large datasets** (> 100k): 5-30 seconds

Times vary based on number of metrics and features.

## Troubleshooting

### I get import errors after installation

Try:
```bash
pip uninstall justiceai
pip install --no-cache-dir justiceai
```

### My model isn't supported

If your model has a `predict()` method, it should work with the sklearn adapter fallback. For custom models, see [Model Adapters](guide/adapters.md).

### Metrics show NaN or infinity

This can happen with edge cases:
- Groups with zero samples
- Zero variance in predictions
- All predictions same class

Check your data for these issues.

### Reports don't open in browser

The `show()` method uses Python's `webbrowser` module. If it doesn't work:
```python
# Manually open the saved file
report.save_html('report.html')
# Then open report.html in your browser
```

## Contributing

### How can I contribute?

See [Contributing Guide](contributing.md) for details. We welcome:
- Bug reports
- Feature requests
- Documentation improvements
- Code contributions

### How do I report a bug?

[Open an issue](https://github.com/JusticeAI-Validation/JusticeAI/issues) on GitHub with:
- Python version
- JusticeAI version
- Minimal code to reproduce
- Error message

### Can I request new features?

Yes! [Open a feature request](https://github.com/JusticeAI-Validation/JusticeAI/issues/new) describing:
- Use case
- Proposed solution
- Why it's important

## Getting Help

### Where can I get support?

- 📖 [Documentation](https://justiceai-validation.github.io/JusticeAI/)
- 🐛 [Issue Tracker](https://github.com/JusticeAI-Validation/JusticeAI/issues)
- 💬 [Discussions](https://github.com/JusticeAI-Validation/JusticeAI/discussions)

### Can I use JusticeAI commercially?

Yes! JusticeAI is MIT licensed, allowing commercial use.

### Is there paid support available?

Currently, support is community-based through GitHub. Enterprise support may be available in the future.
