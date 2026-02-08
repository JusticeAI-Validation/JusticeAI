# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Sprint 5: Polish & Release (In Progress)
- Simplified compliance reporters for better FairnessReport integration
- Fixed all compliance tests (9/9 passing)
- Improved code quality and consistency

## [0.4.0] - 2024-02-08

### Added - Sprint 4: Compliance Brasil + Monitoring

#### Compliance Module 🇧🇷
- **LGPDComplianceReporter**: LGPD Art. 20 compliance reporting
- **BACENComplianceReporter**: BACEN Resolution 4.658/2018 compliance
- Portuguese language support with native templates

#### Monitoring Module 📈
- **FairnessDriftDetector**: Three detection methods (threshold, PSI, KS)
- **MetricsDriftMonitor**: Continuous monitoring with history
- **FairnessAlerting**: Multi-channel alerts (Console, Email, Slack, Webhook)

#### Examples & Tests
- continuous_monitoring.py example
- 33 new tests (24 monitoring + 9 compliance)
- Total: 223 tests passing

## [0.3.0] - 2024-02-08

### Added - Sprint 3: API + Adapters
- XGBoostAdapter and LightGBMAdapter
- FairnessEvaluator main API
- audit() one-liner function
- MkDocs documentation (20+ pages)
- 3 Jupyter notebook tutorials

## [0.2.0] - 2024-02-07

### Added - Sprint 2: Reports
- FairnessReport with HTML export
- Interactive Plotly charts
- Standalone reports (offline-capable)

## [0.1.0] - 2024-02-06

### Added - Sprint 1: Metrics
- 15+ fairness metrics (pre and post-training)
- FairnessCalculator facade
- ThresholdAnalyzer
- 95%+ test coverage

## [0.0.1] - 2024-02-05

### Added - Sprint 0: Foundation
- Poetry project setup
- CI/CD with GitHub Actions
- Development tools (ruff, pytest, mypy)

---

**Target Release**: v1.0.0
**Maintainer**: Gustavo Haase
**License**: MIT
