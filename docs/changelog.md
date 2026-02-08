# Changelog

All notable changes to JusticeAI will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added
- Complete MkDocs documentation
- Tutorial notebooks
- Contributing guidelines

## [0.1.0] - 2026-02-08

### Added
- Initial release of JusticeAI
- `FairnessEvaluator` - Main API for fairness evaluation
- `audit()` - One-line convenience function
- `FairnessReport` - Interactive HTML reports
- Model adapters for sklearn (XGBoost and LightGBM planned)
- Comprehensive fairness metrics:
  - Pre-training: Class Balance, Concept Balance, KL/JS Divergence
  - Post-training: Statistical Parity, Disparate Impact, Equal Opportunity, Equalized Odds
- Beautiful HTML reports with visualizations
- 192 tests with 90%+ coverage
- Type hints with mypy strict mode
- Poetry-based dependency management

### Documentation
- Installation guide
- Quick start tutorial
- Basic concepts explanation
- API reference
- FAQ

### Compliance
- LGPD-focused fairness thresholds
- BACEN compliance guidelines
- Audit trail support

## [0.0.1] - 2026-01-15

### Added
- Initial project structure
- Core metrics implementation
- Basic reporting functionality

---

## Release Notes

### v0.1.0 - First Public Release

JusticeAI's first public release provides a complete toolkit for ML fairness evaluation:

**Highlights:**
- ✨ Simple one-line API: `audit(model, X, y, sensitive_attrs)`
- 📊 Beautiful interactive HTML reports
- 🎯 Production-ready with 90%+ test coverage
- 🇧🇷 LGPD and BACEN compliance focus

**Quick Example:**
```python
from justiceai import audit

report = audit(
    model=my_model,
    X=X_test,
    y_true=y_test,
    sensitive_attrs=gender,
    show=True
)
```

**What's Next (v0.2.0):**
- XGBoost and LightGBM adapters
- Intersectional fairness analysis (multiple attributes)
- Threshold optimization tools
- Production monitoring features
- Custom report templates

---

[Unreleased]: https://github.com/JusticeAI-Validation/JusticeAI/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/JusticeAI-Validation/JusticeAI/releases/tag/v0.1.0
[0.0.1]: https://github.com/JusticeAI-Validation/JusticeAI/releases/tag/v0.0.1
