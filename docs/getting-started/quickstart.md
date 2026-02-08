# Quick Start

Get started with JusticeAI in 5 minutes!

## Your First Fairness Audit

### 1. Import and Prepare Data

```python
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier

# Load your data
df = pd.read_csv('your_data.csv')

# Separate features, target, and sensitive attribute
X = df.drop(['target', 'gender'], axis=1)
y = df['target']
gender = df['gender']

# Split data
X_train, X_test, y_train, y_test, gender_train, gender_test = train_test_split(
    X, y, gender, test_size=0.2, random_state=42
)
```

### 2. Train Your Model

```python
# Train any sklearn-compatible model
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
```

### 3. Run Fairness Audit

The simplest way - one line:

```python
from justiceai import audit

report = audit(
    model=model,
    X=X_test,
    y_true=y_test,
    sensitive_attrs=gender_test,
    output_path='fairness_report.html',
    show=True
)
```

That's it! JusticeAI will:
- ✅ Make predictions with your model
- ✅ Calculate all fairness metrics
- ✅ Generate an interactive HTML report
- ✅ Open the report in your browser

### 4. Check Results

```python
# Get overall fairness score (0-100)
score = report.get_overall_score()
print(f"Fairness Score: {score}/100")

# Check if model passes fairness threshold
passes = report.passes_fairness()
print(f"Passes Fairness: {passes}")

# Get detailed summary
summary = report.get_summary()
print(f"Violations: {summary['n_violations']}")
print(f"Statistical Parity: {summary['statistical_parity_diff']:.3f}")
print(f"Disparate Impact: {summary['disparate_impact_ratio']:.3f}")
```

## Using FairnessEvaluator

For more control, use the `FairnessEvaluator` class:

```python
from justiceai import FairnessEvaluator

# Create evaluator with custom threshold
evaluator = FairnessEvaluator(fairness_threshold=0.05)

# Evaluate model
report = evaluator.evaluate(
    model=model,
    X=X_test,
    y_true=y_test,
    sensitive_attrs=gender_test
)

# Access results
print(f"Score: {report.get_overall_score()}")

# Get list of fairness violations
issues = report.get_issues()
for issue in issues:
    print(f"⚠️ {issue['metric']}: {issue['message']}")
```

## Quick Check During Development

For fast iteration without generating full reports:

```python
# Quick check returns a simple dictionary
metrics = evaluator.quick_check(
    model=model,
    X=X_test,
    y_true=y_test,
    sensitive_attrs=gender_test
)

print(f"Score: {metrics['overall_score']}")
print(f"Passes: {metrics['passes_fairness']}")
print(f"Violations: {metrics['n_violations']}")
```

## Working with Pre-computed Predictions

If you already have predictions:

```python
# Use evaluate_predictions instead of evaluate
report = evaluator.evaluate_predictions(
    y_true=y_test,
    y_pred=predictions,
    sensitive_attrs=gender_test,
    y_pred_proba=probabilities  # Optional
)
```

## Multiple Sensitive Attributes

Pass multiple attributes as a dictionary:

```python
report = audit(
    model=model,
    X=X_test,
    y_true=y_test,
    sensitive_attrs={
        'gender': gender_test,
        'age_group': age_test,
        'race': race_test
    }
)
```

!!! note
    Currently, JusticeAI analyzes one sensitive attribute at a time. Multi-attribute intersectional analysis is coming in a future release.

## Custom Fairness Threshold

Adjust the fairness threshold based on your requirements:

```python
# More strict (smaller differences allowed)
evaluator = FairnessEvaluator(fairness_threshold=0.02)

# More lenient
evaluator = FairnessEvaluator(fairness_threshold=0.10)

# LGPD recommended
evaluator = FairnessEvaluator(fairness_threshold=0.05)  # Default
```

## Next Steps

- [Basic Concepts](concepts.md) - Understand fairness metrics in depth
- [User Guide](../guide/overview.md) - Learn all features
- [Tutorials](../tutorials/index.md) - Step-by-step examples
- [API Reference](../api/index.md) - Complete API documentation

## Common Patterns

### Pattern 1: Model Comparison

```python
models = {
    'Random Forest': RandomForestClassifier(),
    'Logistic Regression': LogisticRegression(),
    'XGBoost': XGBClassifier()
}

for name, model in models.items():
    model.fit(X_train, y_train)

    metrics = evaluator.quick_check(
        model=model,
        X=X_test,
        y_true=y_test,
        sensitive_attrs=gender_test
    )

    print(f"{name}: {metrics['overall_score']}/100")
```

### Pattern 2: Monitoring in Production

```python
# Regular fairness checks
def check_model_fairness(model, recent_data):
    report = audit(
        model=model,
        X=recent_data['X'],
        y_true=recent_data['y'],
        sensitive_attrs=recent_data['gender']
    )

    if not report.passes_fairness():
        send_alert(report.get_issues())

    return report.get_overall_score()
```

### Pattern 3: A/B Testing Fairness

```python
# Compare fairness of model variants
def compare_variants(model_a, model_b, test_data):
    evaluator = FairnessEvaluator()

    report_a = evaluator.evaluate(model_a, test_data['X'],
                                   test_data['y'], test_data['gender'])
    report_b = evaluator.evaluate(model_b, test_data['X'],
                                   test_data['y'], test_data['gender'])

    return {
        'model_a': report_a.get_overall_score(),
        'model_b': report_b.get_overall_score()
    }
```
