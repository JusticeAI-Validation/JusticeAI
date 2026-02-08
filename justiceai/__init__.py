"""
justiceai - Fairness Analysis for ML in Production

A Python library for fairness analysis in machine learning,
focused on production monitoring and Brazilian compliance (LGPD/BACEN).

Main API:
    - FairnessEvaluator: High-level API for fairness evaluation
    - FairnessReport: Report generation and visualization
    - audit: Convenience function for quick analysis

Example:
    >>> from justiceai import FairnessEvaluator
    >>> evaluator = FairnessEvaluator()
    >>> result = evaluator.evaluate(model, X_test, y_test, sensitive_attrs)
    >>> result.show()
"""

__version__ = "0.1.0"
__author__ = "Gustavo Haase"
__email__ = "gustavo.haase@gmail.com"
__license__ = "MIT"

from justiceai.api import audit
from justiceai.fairness_evaluator import FairnessEvaluator
from justiceai.reports import FairnessReport

__all__ = ["FairnessEvaluator", "FairnessReport", "audit"]
