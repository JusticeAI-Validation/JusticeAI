# JusticeAI Examples

This directory contains example scripts demonstrating how to use JusticeAI for fairness analysis.

## Available Examples

### 1. Simple Report Example
**File:** `simple_report_example.py`

Basic usage of JusticeAI to create a fairness report from model predictions.

**Features demonstrated:**
- Synthetic dataset generation with intentional bias
- Training a RandomForest classifier
- Creating fairness report from predictions
- Getting summary statistics
- Extracting issues and recommendations
- Saving HTML report

**Run:**
```bash
cd examples
python simple_report_example.py
```

**Output:**
- Console summary with fairness metrics
- HTML report: `fairness_report_example.html`

## Quick Start

### Basic Usage

```python
from justiceai.reports import FairnessReport
import numpy as np
import pandas as pd

# Your model predictions
y_true = np.array([1, 0, 1, 0, 1, 0])
y_pred = np.array([1, 0, 1, 0, 0, 1])
sensitive = pd.Series(['A', 'A', 'A', 'B', 'B', 'B'])

# Create report
report = FairnessReport.from_predictions(
    y_true=y_true,
    y_pred=y_pred,
    sensitive_attr=sensitive
)

# Check fairness
if report.passes_fairness():
    print(f"✓ Model is fair! Score: {report.get_overall_score():.1f}/100")
else:
    print("⚠️ Model has fairness violations:")
    for issue in report.get_issues():
        print(f"  - {issue['message']}")

# Save report
report.save_html('report.html')
report.show()  # Opens in browser
```

### With Full Features

```python
from justiceai.reports import FairnessReport

report = FairnessReport.from_predictions(
    y_true=y_test,                    # Ground truth labels
    y_pred=y_pred,                    # Model predictions
    sensitive_attr=sensitive,         # Protected attribute
    X=X_test,                         # Features (optional)
    y_pred_proba=probabilities,       # Probabilities (optional)
    fairness_threshold=0.05           # Custom threshold
)

# Access metrics
summary = report.get_summary()
issues = report.get_issues()
recommendations = report.get_recommendations()

# Generate report
report.save_html('comprehensive_report.html')
```

### From Pre-calculated Metrics

```python
from justiceai.core.metrics.calculator import FairnessCalculator
from justiceai.reports import FairnessReport

# Calculate metrics separately
calculator = FairnessCalculator()
metrics = calculator.calculate_all(y_true, y_pred, sensitive, X)

# Create report from metrics
report = FairnessReport.from_metrics(metrics)
report.save_html('report.html')
```

## Requirements

All examples require:
- `numpy`
- `pandas`
- `scikit-learn` (for examples with ML models)
- `justiceai` (installed via `poetry install`)

## More Information

For detailed documentation, see:
- Main README: `../README.md`
- API Documentation: `../docs/`
- Sprint Documentation: `../desenvolvimento/sprints/`
