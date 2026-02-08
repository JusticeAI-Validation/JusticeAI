"""
JusticeAI Reports - Fairness Report Generation.

This module provides tools for creating professional fairness reports
from machine learning model metrics.

Main classes:
    - FairnessReport: Main interface for creating reports
    - FairnessCalculator: Calculate fairness metrics
    - ChartFactory: Create interactive charts
    - HTMLRenderer: Render HTML reports

Example:
    >>> from justiceai.reports import FairnessReport
    >>> report = FairnessReport.from_predictions(y_true, y_pred, sensitive)
    >>> report.save_html('report.html')
    >>> report.show()
"""

from justiceai.reports.fairness_report import FairnessReport

__all__ = ["FairnessReport"]
