"""
Unified fairness calculator (Facade pattern).

This module provides a single interface to calculate all fairness metrics
with caching and validation.
"""

from typing import Any, Optional

import numpy as np
import pandas as pd

from justiceai.core.metrics.posttrain import (
    accuracy_difference,
    calibration_by_group,
    confusion_matrix_by_group,
    disparate_impact,
    equal_opportunity,
    equalized_odds,
    false_negative_rate_difference,
    negative_predictive_parity,
    predictive_parity,
    statistical_parity,
    treatment_equality,
)
from justiceai.core.metrics.pretrain import (
    class_balance,
    concept_balance,
    group_distribution_difference,
    js_divergence,
    kl_divergence,
)


class FairnessCalculator:
    """
    Unified interface for calculating all fairness metrics.

    This class provides a facade for all fairness metric calculations,
    with optional caching and input validation.

    Example:
        >>> import numpy as np
        >>> import pandas as pd
        >>> from sklearn.ensemble import RandomForestClassifier
        >>>
        >>> # Prepare data
        >>> X = np.random.randn(100, 5)
        >>> y = np.random.randint(0, 2, 100)
        >>> sensitive = pd.Series(np.random.choice(['A', 'B'], 100))
        >>>
        >>> # Train model
        >>> model = RandomForestClassifier(random_state=42)
        >>> model.fit(X, y)
        >>>
        >>> # Calculate all metrics
        >>> calculator = FairnessCalculator(cache_results=True)
        >>> results = calculator.calculate_all(
        ...     y_true=y,
        ...     y_pred=model.predict(X),
        ...     sensitive_attr=sensitive,
        ...     X=X
        ... )
        >>> print(results.keys())
    """

    def __init__(self, cache_results: bool = True):
        """
        Initialize fairness calculator.

        Args:
            cache_results: Whether to cache metric results
        """
        self.cache_results = cache_results
        self.cache: dict[str, Any] = {} if cache_results else {}
        self._validated = False

    def _validate_inputs(
        self,
        y_true: Optional[np.ndarray] = None,
        y_pred: Optional[np.ndarray] = None,
        y_pred_proba: Optional[np.ndarray] = None,
        sensitive_attr: Optional[pd.Series] = None,
        X: Optional[pd.DataFrame] = None,
    ) -> None:
        """Validate input arrays."""
        if y_true is not None and y_pred is not None:
            if len(y_true) != len(y_pred):
                raise ValueError("y_true and y_pred must have same length")

        if y_pred is not None and sensitive_attr is not None:
            if len(y_pred) != len(sensitive_attr):
                raise ValueError("y_pred and sensitive_attr must have same length")

        if y_pred_proba is not None and y_true is not None:
            if len(y_pred_proba) != len(y_true):
                raise ValueError("y_pred_proba and y_true must have same length")

        if X is not None and y_true is not None:
            if len(X) != len(y_true):
                raise ValueError("X and y_true must have same length")

        self._validated = True

    def calculate_pretrain_metrics(
        self, X: pd.DataFrame, y: pd.Series, sensitive_attr: pd.Series
    ) -> dict[str, Any]:
        """
        Calculate all pre-training metrics (model-independent).

        Args:
            X: Feature matrix
            y: Target variable
            sensitive_attr: Sensitive attribute

        Returns:
            Dictionary with all pre-training metrics

        Example:
            >>> calculator = FairnessCalculator()
            >>> metrics = calculator.calculate_pretrain_metrics(X, y, sensitive)
            >>> print(metrics['class_balance'])
        """
        self._validate_inputs(y_true=y.values, sensitive_attr=sensitive_attr, X=X)

        cache_key = "pretrain"
        if self.cache_results and cache_key in self.cache:
            return self.cache[cache_key]

        results = {
            "class_balance": class_balance(y, sensitive_attr),
            "concept_balance": concept_balance(X, y, sensitive_attr),
            "group_distribution_difference": group_distribution_difference(
                y, sensitive_attr
            ),
        }

        if self.cache_results:
            self.cache[cache_key] = results

        return results

    def calculate_posttrain_metrics(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        sensitive_attr: pd.Series,
        y_pred_proba: Optional[np.ndarray] = None,
    ) -> dict[str, Any]:
        """
        Calculate all post-training metrics (model-dependent).

        Args:
            y_true: True labels
            y_pred: Model predictions (binary)
            sensitive_attr: Sensitive attribute
            y_pred_proba: Predicted probabilities (optional, for calibration)

        Returns:
            Dictionary with all post-training metrics

        Example:
            >>> calculator = FairnessCalculator()
            >>> metrics = calculator.calculate_posttrain_metrics(
            ...     y_true, y_pred, sensitive, y_pred_proba
            ... )
            >>> print(metrics['statistical_parity'])
        """
        self._validate_inputs(
            y_true=y_true,
            y_pred=y_pred,
            y_pred_proba=y_pred_proba,
            sensitive_attr=sensitive_attr,
        )

        cache_key = "posttrain"
        if self.cache_results and cache_key in self.cache:
            return self.cache[cache_key]

        results = {
            # Basic metrics
            "statistical_parity": statistical_parity(y_pred, sensitive_attr),
            "disparate_impact": disparate_impact(y_pred, sensitive_attr),
            "equal_opportunity": equal_opportunity(y_true, y_pred, sensitive_attr),
            "equalized_odds": equalized_odds(y_true, y_pred, sensitive_attr),
            "confusion_matrix": confusion_matrix_by_group(
                y_true, y_pred, sensitive_attr
            ),
            # Advanced metrics
            "false_negative_rate_diff": false_negative_rate_difference(
                y_true, y_pred, sensitive_attr
            ),
            "predictive_parity": predictive_parity(y_true, y_pred, sensitive_attr),
            "negative_predictive_parity": negative_predictive_parity(
                y_true, y_pred, sensitive_attr
            ),
            "accuracy_difference": accuracy_difference(y_true, y_pred, sensitive_attr),
            "treatment_equality": treatment_equality(y_true, y_pred, sensitive_attr),
        }

        # Add calibration if probabilities provided
        if y_pred_proba is not None:
            results["calibration"] = calibration_by_group(
                y_true, y_pred_proba, sensitive_attr
            )

        if self.cache_results:
            self.cache[cache_key] = results

        return results

    def calculate_all(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        sensitive_attr: pd.Series,
        X: Optional[pd.DataFrame] = None,
        y_pred_proba: Optional[np.ndarray] = None,
    ) -> dict[str, Any]:
        """
        Calculate all fairness metrics (pre and post-training).

        Args:
            y_true: True labels
            y_pred: Model predictions
            sensitive_attr: Sensitive attribute
            X: Feature matrix (optional, for pre-training metrics)
            y_pred_proba: Predicted probabilities (optional, for calibration)

        Returns:
            Dictionary with all metrics organized by category:
            {
                'pretrain': {...},  # If X provided
                'posttrain': {...},
                'summary': {...}
            }

        Example:
            >>> calculator = FairnessCalculator()
            >>> all_metrics = calculator.calculate_all(
            ...     y_true=y,
            ...     y_pred=predictions,
            ...     sensitive_attr=sensitive,
            ...     X=features,
            ...     y_pred_proba=probabilities
            ... )
            >>> print(all_metrics['summary']['overall_fairness_score'])
        """
        self._validate_inputs(
            y_true=y_true,
            y_pred=y_pred,
            y_pred_proba=y_pred_proba,
            sensitive_attr=sensitive_attr,
            X=X,
        )

        results: dict[str, Any] = {}

        # Calculate pre-training metrics if X provided
        if X is not None:
            results["pretrain"] = self.calculate_pretrain_metrics(
                X=X,
                y=pd.Series(y_true),
                sensitive_attr=sensitive_attr,
            )

        # Calculate post-training metrics
        results["posttrain"] = self.calculate_posttrain_metrics(
            y_true=y_true,
            y_pred=y_pred,
            sensitive_attr=sensitive_attr,
            y_pred_proba=y_pred_proba,
        )

        # Calculate summary statistics
        results["summary"] = self._calculate_summary(results)

        return results

    def _calculate_summary(self, results: dict[str, Any]) -> dict[str, Any]:
        """
        Calculate summary statistics from all metrics.

        Args:
            results: Dictionary with pretrain and posttrain metrics

        Returns:
            Dictionary with summary statistics
        """
        posttrain = results.get("posttrain", {})

        # Count fairness violations
        violations = []
        if not posttrain.get("statistical_parity", {}).get("is_fair", True):
            violations.append("statistical_parity")
        if not posttrain.get("disparate_impact", {}).get("passes_80_rule", True):
            violations.append("disparate_impact")
        if not posttrain.get("equal_opportunity", {}).get("is_fair", True):
            violations.append("equal_opportunity")
        if not posttrain.get("equalized_odds", {}).get("is_fair", True):
            violations.append("equalized_odds")

        # Calculate overall fairness score (0-100)
        total_checks = 4  # Number of basic fairness checks
        violations_count = len(violations)
        overall_score = ((total_checks - violations_count) / total_checks) * 100

        # Get key metric values
        di_ratio = posttrain.get("disparate_impact", {}).get("ratio", 1.0)
        sp_diff = posttrain.get("statistical_parity", {}).get("difference", 0.0)

        return {
            "overall_fairness_score": float(overall_score),
            "fairness_violations": violations,
            "n_violations": len(violations),
            "disparate_impact_ratio": float(di_ratio),
            "statistical_parity_diff": float(sp_diff),
            "passes_basic_fairness": len(violations) == 0,
        }

    def get_recommendations(
        self, results: Optional[dict[str, Any]] = None
    ) -> list[str]:
        """
        Get actionable recommendations based on fairness violations.

        Args:
            results: Results from calculate_all() (uses cache if not provided)

        Returns:
            List of recommendation strings

        Example:
            >>> results = calculator.calculate_all(y_true, y_pred, sensitive)
            >>> recommendations = calculator.get_recommendations(results)
            >>> for rec in recommendations:
            ...     print(rec)
        """
        if results is None:
            if "posttrain" not in self.cache:
                raise ValueError("No cached results. Call calculate_all() first.")
            results = {"posttrain": self.cache["posttrain"]}

        recommendations = []
        posttrain = results.get("posttrain", {})

        # Statistical parity
        if not posttrain.get("statistical_parity", {}).get("is_fair", True):
            recommendations.append(
                "Statistical parity violation detected. "
                "Consider using threshold optimization or reweighing techniques."
            )

        # Disparate impact
        if not posttrain.get("disparate_impact", {}).get("passes_80_rule", True):
            di_ratio = posttrain.get("disparate_impact", {}).get("ratio", 1.0)
            recommendations.append(
                f"Disparate impact ratio ({di_ratio:.2f}) fails 80% rule. "
                "Review feature selection and consider fairness-aware training."
            )

        # Equal opportunity
        if not posttrain.get("equal_opportunity", {}).get("is_fair", True):
            recommendations.append(
                "Equal opportunity violation detected. "
                "Different groups have unequal true positive rates. "
                "Consider equalized odds post-processing."
            )

        # Equalized odds
        if not posttrain.get("equalized_odds", {}).get("is_fair", True):
            recommendations.append(
                "Equalized odds violation detected. "
                "Both TPR and FPR differ across groups. "
                "Consider using calibrated equalized odds."
            )

        if not recommendations:
            recommendations.append(
                "No major fairness violations detected! "
                "Model passes basic fairness checks."
            )

        return recommendations

    def clear_cache(self) -> None:
        """Clear cached results."""
        self.cache.clear()
