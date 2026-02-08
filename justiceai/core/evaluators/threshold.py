"""
Threshold analysis for fairness-performance trade-offs.

This module provides tools to analyze how different decision thresholds
affect both model performance and fairness metrics.
"""

from typing import Any, Callable, Optional

import numpy as np
import pandas as pd
from sklearn.metrics import accuracy_score, f1_score, precision_score, recall_score

from justiceai.core.metrics.posttrain import (
    disparate_impact,
    equal_opportunity,
    equalized_odds,
    statistical_parity,
)


class ThresholdAnalyzer:
    """
    Analyze fairness metrics across different decision thresholds.

    This class helps identify optimal thresholds that balance fairness
    and performance objectives.

    Example:
        >>> from sklearn.ensemble import RandomForestClassifier
        >>> import numpy as np
        >>> import pandas as pd
        >>>
        >>> # Train model
        >>> model = RandomForestClassifier(random_state=42)
        >>> X_train = np.random.randn(100, 5)
        >>> y_train = np.random.randint(0, 2, 100)
        >>> model.fit(X_train, y_train)
        >>>
        >>> # Analyze thresholds
        >>> X_test = np.random.randn(50, 5)
        >>> y_test = np.random.randint(0, 2, 50)
        >>> sensitive = pd.Series(np.random.choice(['A', 'B'], 50))
        >>>
        >>> analyzer = ThresholdAnalyzer()
        >>> results = analyzer.analyze(
        ...     y_true=y_test,
        ...     y_pred_proba=model.predict_proba(X_test)[:, 1],
        ...     sensitive_attr=sensitive
        ... )
    """

    def __init__(
        self,
        thresholds: Optional[np.ndarray] = None,
        fairness_metrics: Optional[list[str]] = None,
        performance_metrics: Optional[list[str]] = None,
    ):
        """
        Initialize threshold analyzer.

        Args:
            thresholds: Array of thresholds to test (default: 0.01 to 0.99)
            fairness_metrics: List of fairness metrics to compute
            performance_metrics: List of performance metrics to compute
        """
        self.thresholds = (
            thresholds
            if thresholds is not None
            else np.linspace(0.01, 0.99, 99)
        )

        self.fairness_metrics = fairness_metrics or [
            "statistical_parity",
            "disparate_impact",
            "equal_opportunity",
            "equalized_odds",
        ]

        self.performance_metrics = performance_metrics or [
            "accuracy",
            "precision",
            "recall",
            "f1_score",
        ]

        self.results_: Optional[pd.DataFrame] = None
        self.optimal_threshold_: Optional[float] = None

    def analyze(
        self,
        y_true: np.ndarray,
        y_pred_proba: np.ndarray,
        sensitive_attr: pd.Series,
    ) -> pd.DataFrame:
        """
        Analyze metrics across all thresholds.

        Args:
            y_true: True labels
            y_pred_proba: Predicted probabilities (not binary predictions)
            sensitive_attr: Sensitive attribute

        Returns:
            DataFrame with metrics for each threshold

        Example:
            >>> analyzer = ThresholdAnalyzer()
            >>> results = analyzer.analyze(y_true, y_proba, sensitive)
            >>> print(results.head())
        """
        results = []

        for threshold in self.thresholds:
            # Convert probabilities to binary predictions
            y_pred = (y_pred_proba >= threshold).astype(int)

            metrics = {"threshold": threshold}

            # Calculate performance metrics
            if "accuracy" in self.performance_metrics:
                metrics["accuracy"] = accuracy_score(y_true, y_pred)

            if "precision" in self.performance_metrics:
                metrics["precision"] = precision_score(
                    y_true, y_pred, zero_division=0.0
                )

            if "recall" in self.performance_metrics:
                metrics["recall"] = recall_score(
                    y_true, y_pred, zero_division=0.0
                )

            if "f1_score" in self.performance_metrics:
                metrics["f1_score"] = f1_score(y_true, y_pred, zero_division=0.0)

            # Calculate fairness metrics
            if "statistical_parity" in self.fairness_metrics:
                sp_result = statistical_parity(y_pred, sensitive_attr)
                metrics["statistical_parity_diff"] = sp_result["difference"]
                metrics["statistical_parity_ratio"] = sp_result["ratio"]

            if "disparate_impact" in self.fairness_metrics:
                di_result = disparate_impact(y_pred, sensitive_attr)
                metrics["disparate_impact_ratio"] = di_result["ratio"]

            if "equal_opportunity" in self.fairness_metrics:
                eo_result = equal_opportunity(y_true, y_pred, sensitive_attr)
                metrics["equal_opportunity_diff"] = eo_result["difference"]

            if "equalized_odds" in self.fairness_metrics:
                eq_result = equalized_odds(y_true, y_pred, sensitive_attr)
                metrics["equalized_odds_tpr_diff"] = eq_result["tpr_difference"]
                metrics["equalized_odds_fpr_diff"] = eq_result["fpr_difference"]

            results.append(metrics)

        self.results_ = pd.DataFrame(results)
        return self.results_

    def find_optimal_threshold(
        self,
        fairness_metric: str = "disparate_impact_ratio",
        performance_metric: str = "f1_score",
        fairness_weight: float = 0.5,
        fairness_constraint: Optional[float] = None,
    ) -> dict[str, Any]:
        """
        Find optimal threshold balancing fairness and performance.

        Args:
            fairness_metric: Name of fairness metric to optimize
            performance_metric: Name of performance metric to optimize
            fairness_weight: Weight for fairness (0-1, default 0.5)
            fairness_constraint: Minimum fairness value required (optional)

        Returns:
            Dictionary with optimal threshold and metrics

        Example:
            >>> optimal = analyzer.find_optimal_threshold(
            ...     fairness_metric='disparate_impact_ratio',
            ...     performance_metric='f1_score',
            ...     fairness_weight=0.6
            ... )
            >>> print(f"Optimal threshold: {optimal['threshold']}")
        """
        if self.results_ is None:
            raise ValueError("Must call analyze() before finding optimal threshold")

        df = self.results_.copy()

        # Normalize metrics to [0, 1] range
        if performance_metric in df.columns:
            perf_normalized = df[performance_metric] / df[performance_metric].max()
        else:
            raise ValueError(f"Performance metric '{performance_metric}' not found")

        if fairness_metric in df.columns:
            # For metrics where higher is better (like disparate_impact_ratio)
            if "ratio" in fairness_metric:
                fair_normalized = df[fairness_metric] / df[fairness_metric].max()
            # For metrics where lower is better (like difference metrics)
            else:
                fair_normalized = 1 - (
                    df[fairness_metric] / df[fairness_metric].max()
                )
        else:
            raise ValueError(f"Fairness metric '{fairness_metric}' not found")

        # Apply fairness constraint if specified
        if fairness_constraint is not None:
            valid_mask = df[fairness_metric] >= fairness_constraint
            df = df[valid_mask]
            perf_normalized = perf_normalized[valid_mask]
            fair_normalized = fair_normalized[valid_mask]

            if len(df) == 0:
                return {
                    "threshold": None,
                    "message": "No threshold satisfies the fairness constraint",
                    "fairness_constraint": fairness_constraint,
                }

        # Calculate combined score
        combined_score = (
            fairness_weight * fair_normalized
            + (1 - fairness_weight) * perf_normalized
        )

        # Find optimal threshold
        optimal_idx = combined_score.idxmax()
        optimal_row = df.loc[optimal_idx]

        self.optimal_threshold_ = float(optimal_row["threshold"])

        return {
            "threshold": self.optimal_threshold_,
            "fairness_metric": fairness_metric,
            "fairness_value": float(optimal_row[fairness_metric]),
            "performance_metric": performance_metric,
            "performance_value": float(optimal_row[performance_metric]),
            "combined_score": float(combined_score.loc[optimal_idx]),
            "all_metrics": optimal_row.to_dict(),
        }

    def plot_tradeoff_curve(
        self,
        fairness_metric: str = "disparate_impact_ratio",
        performance_metric: str = "f1_score",
    ) -> dict[str, Any]:
        """
        Get data for plotting fairness-performance trade-off curve.

        Args:
            fairness_metric: Fairness metric for x-axis
            performance_metric: Performance metric for y-axis

        Returns:
            Dictionary with plot data

        Example:
            >>> plot_data = analyzer.plot_tradeoff_curve()
            >>> # Use with Plotly/Matplotlib to create visualization
        """
        if self.results_ is None:
            raise ValueError("Must call analyze() before plotting")

        return {
            "x": self.results_[fairness_metric].values,
            "y": self.results_[performance_metric].values,
            "thresholds": self.results_["threshold"].values,
            "x_label": fairness_metric,
            "y_label": performance_metric,
        }

    def get_threshold_recommendation(
        self, use_case: str = "balanced"
    ) -> dict[str, Any]:
        """
        Get threshold recommendation based on use case.

        Args:
            use_case: One of 'balanced', 'fairness_priority', 'performance_priority'

        Returns:
            Dictionary with recommended threshold and explanation

        Example:
            >>> recommendation = analyzer.get_threshold_recommendation('fairness_priority')
            >>> print(recommendation['explanation'])
        """
        if self.results_ is None:
            raise ValueError("Must call analyze() before getting recommendation")

        if use_case == "balanced":
            result = self.find_optimal_threshold(fairness_weight=0.5)
            explanation = (
                "Balanced approach: Equal weight to fairness and performance"
            )
        elif use_case == "fairness_priority":
            result = self.find_optimal_threshold(fairness_weight=0.7)
            explanation = (
                "Fairness priority: 70% weight on fairness, 30% on performance"
            )
        elif use_case == "performance_priority":
            result = self.find_optimal_threshold(fairness_weight=0.3)
            explanation = (
                "Performance priority: 30% weight on fairness, 70% on performance"
            )
        else:
            raise ValueError(
                f"Unknown use case: {use_case}. "
                "Choose: 'balanced', 'fairness_priority', 'performance_priority'"
            )

        result["use_case"] = use_case
        result["explanation"] = explanation

        return result
