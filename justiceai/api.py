"""
Convenience API functions.

This module provides simple one-liner functions for common tasks.
"""

from typing import Any

import numpy as np
import pandas as pd

from justiceai.fairness_evaluator import FairnessEvaluator
from justiceai.reports import FairnessReport


def audit(
    model: Any,
    X: pd.DataFrame | np.ndarray,
    y_true: np.ndarray | pd.Series,
    sensitive_attrs: dict[str, pd.Series] | pd.Series,
    fairness_threshold: float = 0.05,
    output_path: str | None = None,
    show: bool = False,
) -> FairnessReport:
    """
    One-liner for complete fairness audit.

    This function performs a complete fairness analysis and optionally
    saves/displays the report.

    Args:
        model: Trained ML model
        X: Test features
        y_true: True labels
        sensitive_attrs: Sensitive attributes
        fairness_threshold: Threshold for fairness violations (default: 0.05)
        output_path: Optional path to save HTML report
        show: Whether to open report in browser (default: False)

    Returns:
        FairnessReport with complete analysis

    Example:
        Quick analysis:
        >>> from justiceai import audit
        >>> report = audit(model, X_test, y_test, gender)
        >>> print(f"Score: {report.get_overall_score()}/100")

        Save and show:
        >>> report = audit(
        ...     model, X_test, y_test, gender,
        ...     output_path='report.html',
        ...     show=True
        ... )
    """
    # Create evaluator
    evaluator = FairnessEvaluator(fairness_threshold=fairness_threshold)

    # Evaluate
    report = evaluator.evaluate(model, X, y_true, sensitive_attrs)

    # Save if requested
    if output_path:
        report.save_html(output_path)

    # Show if requested
    if show:
        if output_path:
            report.show(output_path)
        else:
            report.show()

    return report
