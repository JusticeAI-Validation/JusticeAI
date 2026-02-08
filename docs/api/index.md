# API Reference

Complete API documentation for JusticeAI.

## Main API

The primary interfaces for fairness evaluation:

- [Main Package](justiceai.md) - Top-level imports and version info
- [FairnessEvaluator](justiceai/fairness_evaluator.md) - High-level evaluation API
- [audit()](justiceai/api.md) - One-line convenience function
- [FairnessReport](justiceai/reports/fairness_report.md) - Report generation and display

## Core Components

### Model Adapters

Framework-agnostic model interfaces:

- [Adapters Overview](justiceai/core/adapters.md) - Adapter system
- [BaseModelAdapter](justiceai/core/adapters/base_adapter.md) - Base class
- [SklearnAdapter](justiceai/core/adapters/sklearn_adapter.md) - scikit-learn support

### Metrics

Fairness metrics calculation:

- [Post-training Metrics](justiceai/core/metrics/posttrain.md) - Statistical parity, equal opportunity, etc.
- [Pre-training Metrics](justiceai/core/metrics/pretrain.md) - Class balance, KL divergence, etc.
- [Metrics Calculator](justiceai/core/metrics/calculator.md) - Unified metrics interface

### Reports

Report generation and visualization:

- [FairnessReport](justiceai/reports/fairness_report.md) - Main report class

## Quick Links

### Common Tasks

**Evaluate a model:**
```python
from justiceai import FairnessEvaluator
evaluator = FairnessEvaluator()
report = evaluator.evaluate(model, X, y, sensitive_attrs)
```

**Quick audit:**
```python
from justiceai import audit
report = audit(model, X, y, sensitive_attrs, show=True)
```

**Work with predictions:**
```python
report = evaluator.evaluate_predictions(y_true, y_pred, sensitive_attrs)
```

### Important Classes

- [`FairnessEvaluator`](justiceai/fairness_evaluator.md) - Main evaluation class
- [`FairnessReport`](justiceai/reports/fairness_report.md) - Report with methods like `get_overall_score()`, `passes_fairness()`
- [`BaseModelAdapter`](justiceai/core/adapters/base_adapter.md) - Create custom adapters

## Module Organization

```
justiceai/
├── __init__.py              # Main exports
├── fairness_evaluator.py    # FairnessEvaluator class
├── api.py                   # Convenience functions
├── core/
│   ├── adapters/            # Model adapters
│   ├── metrics/             # Fairness metrics
│   └── evaluators/          # Threshold analysis
├── reports/                 # Report generation
│   ├── fairness_report.py
│   ├── charts/              # Visualizations
│   ├── renderers/           # HTML rendering
│   └── transformers/        # Data transformation
└── compliance/              # LGPD/BACEN compliance
```

## Navigation

Browse the API reference using the navigation on the left, or use the search function to find specific classes and methods.

For usage examples, see the [Tutorials](../tutorials/index.md) section.
