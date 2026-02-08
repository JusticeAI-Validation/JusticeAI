"""
FairnessEvaluator - Main API for fairness analysis.

This module provides the primary interface for evaluating ML model fairness.
"""

from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from justiceai.core.adapters import create_adapter
from justiceai.core.adapters.base_adapter import BaseModelAdapter
from justiceai.reports import FairnessReport


class FairnessEvaluator:
    """
    Main API for fairness evaluation.

    This class provides a simple, high-level interface for evaluating
    the fairness of machine learning models.

    Example:
        >>> from justiceai import FairnessEvaluator
        >>> from sklearn.ensemble import RandomForestClassifier
        >>>
        >>> # Train model
        >>> model = RandomForestClassifier()
        >>> model.fit(X_train, y_train)
        >>>
        >>> # Evaluate fairness
        >>> evaluator = FairnessEvaluator()
        >>> result = evaluator.evaluate(
        ...     model=model,
        ...     X=X_test,
        ...     y_true=y_test,
        ...     sensitive_attrs={'gender': gender_test}
        ... )
        >>>
        >>> # Generate report
        >>> result.save_html('fairness_report.html')
        >>> result.show()
    """

    def __init__(self, fairness_threshold: float = 0.05):
        """
        Initialize fairness evaluator.

        Args:
            fairness_threshold: Threshold for determining fairness violations
                               (default: 0.05)
        """
        self.fairness_threshold = fairness_threshold

    def evaluate(
        self,
        model: Any,
        X: pd.DataFrame | np.ndarray,
        y_true: np.ndarray | pd.Series,
        sensitive_attrs: dict[str, pd.Series] | pd.Series,
        return_probabilities: bool = True,
    ) -> FairnessReport:
        """
        Evaluate model fairness.

        Args:
            model: Trained ML model (sklearn, xgboost, lightgbm, etc.)
            X: Test features
            y_true: True labels
            sensitive_attrs: Sensitive attributes (e.g., {'gender': series})
                            or single Series for one attribute
            return_probabilities: Whether to compute probability-based metrics

        Returns:
            FairnessReport with analysis results

        Example:
            >>> evaluator = FairnessEvaluator()
            >>> result = evaluator.evaluate(
            ...     model=model,
            ...     X=X_test,
            ...     y_true=y_test,
            ...     sensitive_attrs=gender
            ... )
            >>> print(f"Fairness Score: {result.get_overall_score()}/100")
        """
        # Create adapter for model
        adapter = create_adapter(model)

        # Get predictions
        y_pred = adapter.predict(X)

        # Get probabilities if requested
        y_pred_proba = None
        if return_probabilities and adapter.supports_proba:
            y_pred_proba = adapter.predict_proba(X)

        # Handle sensitive attributes
        if isinstance(sensitive_attrs, dict):
            # For now, use the first sensitive attribute
            # TODO: Support multiple attributes in future
            sensitive_attr = list(sensitive_attrs.values())[0]
        else:
            sensitive_attr = sensitive_attrs

        # Ensure y_true is numpy array
        if isinstance(y_true, pd.Series):
            y_true = y_true.values

        # Convert X to DataFrame if needed
        X_df = None
        if isinstance(X, pd.DataFrame):
            X_df = X
        elif isinstance(X, np.ndarray):
            X_df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(X.shape[1])])

        # Create fairness report
        report = FairnessReport.from_predictions(
            y_true=y_true,
            y_pred=y_pred,
            sensitive_attr=sensitive_attr,
            X=X_df,
            y_pred_proba=y_pred_proba,
            fairness_threshold=self.fairness_threshold,
        )

        return report

    def evaluate_predictions(
        self,
        y_true: np.ndarray | pd.Series,
        y_pred: np.ndarray | pd.Series,
        sensitive_attrs: dict[str, pd.Series] | pd.Series,
        X: pd.DataFrame | np.ndarray | None = None,
        y_pred_proba: np.ndarray | None = None,
    ) -> FairnessReport:
        """
        Evaluate fairness from pre-computed predictions.

        Use this when you already have predictions and don't need to
        pass the model itself.

        Args:
            y_true: True labels
            y_pred: Model predictions
            sensitive_attrs: Sensitive attributes
            X: Optional features for pre-training metrics
            y_pred_proba: Optional predicted probabilities

        Returns:
            FairnessReport with analysis results

        Example:
            >>> evaluator = FairnessEvaluator()
            >>> result = evaluator.evaluate_predictions(
            ...     y_true=y_test,
            ...     y_pred=predictions,
            ...     sensitive_attrs=gender
            ... )
        """
        # Handle sensitive attributes
        if isinstance(sensitive_attrs, dict):
            sensitive_attr = list(sensitive_attrs.values())[0]
        else:
            sensitive_attr = sensitive_attrs

        # Ensure arrays
        if isinstance(y_true, pd.Series):
            y_true = y_true.values
        if isinstance(y_pred, pd.Series):
            y_pred = y_pred.values

        # Convert X to DataFrame if needed
        X_df = None
        if X is not None:
            if isinstance(X, pd.DataFrame):
                X_df = X
            elif isinstance(X, np.ndarray):
                X_df = pd.DataFrame(
                    X, columns=[f"feature_{i}" for i in range(X.shape[1])]
                )

        # Create report
        report = FairnessReport.from_predictions(
            y_true=y_true,
            y_pred=y_pred,
            sensitive_attr=sensitive_attr,
            X=X_df,
            y_pred_proba=y_pred_proba,
            fairness_threshold=self.fairness_threshold,
        )

        return report

    def quick_check(
        self,
        model: Any,
        X: pd.DataFrame | np.ndarray,
        y_true: np.ndarray | pd.Series,
        sensitive_attrs: dict[str, pd.Series] | pd.Series,
    ) -> dict[str, Any]:
        """
        Quick fairness check without full report generation.

        Returns key metrics without creating HTML report.

        Args:
            model: Trained ML model
            X: Test features
            y_true: True labels
            sensitive_attrs: Sensitive attributes

        Returns:
            Dictionary with key fairness metrics

        Example:
            >>> evaluator = FairnessEvaluator()
            >>> metrics = evaluator.quick_check(model, X_test, y_test, gender)
            >>> print(f"Score: {metrics['overall_score']}")
            >>> print(f"Passes: {metrics['passes_fairness']}")
        """
        report = self.evaluate(model, X, y_true, sensitive_attrs)

        return {
            "overall_score": report.get_overall_score(),
            "passes_fairness": report.passes_fairness(),
            "n_violations": len(report.get_issues()),
            "summary": report.get_summary(),
        }
