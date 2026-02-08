"""
Fairness Report Builder - Unified Interface (Facade).

This module provides the main interface for creating fairness reports
from model metrics.
"""

import webbrowser
from pathlib import Path
from typing import Any

import numpy as np
import pandas as pd

from justiceai.core.metrics.calculator import FairnessCalculator
from justiceai.reports.charts.chart_factory import ChartFactory
from justiceai.reports.renderers.html_renderer import HTMLRenderer
from justiceai.reports.transformers.data_transformer import FairnessDataTransformer


class FairnessReport:
    """
    Unified interface for creating fairness reports.

    This class provides a simple facade over the entire reporting pipeline:
    metrics calculation -> data transformation -> chart creation -> HTML rendering.

    Example:
        >>> from justiceai.reports import FairnessReport
        >>> import numpy as np
        >>> import pandas as pd
        >>>
        >>> # Prepare data
        >>> y_true = np.array([1, 0, 1, 0, 1, 0, 1, 0])
        >>> y_pred = np.array([1, 0, 1, 0, 0, 1, 1, 0])
        >>> sensitive = pd.Series(['A', 'A', 'A', 'A', 'B', 'B', 'B', 'B'])
        >>>
        >>> # Create report
        >>> report = FairnessReport.from_predictions(
        ...     y_true=y_true,
        ...     y_pred=y_pred,
        ...     sensitive_attr=sensitive
        ... )
        >>>
        >>> # Save and open
        >>> report.save_html('report.html')
        >>> report.show()  # Opens in browser
    """

    def __init__(
        self,
        metrics: dict[str, Any],
        transformed_data: dict[str, Any],
        charts: dict[str, str],
    ):
        """
        Initialize report from pre-computed components.

        Args:
            metrics: Raw metrics from FairnessCalculator
            transformed_data: Transformed data from FairnessDataTransformer
            charts: Chart JSON strings from ChartFactory
        """
        self.metrics = metrics
        self.transformed_data = transformed_data
        self.charts = charts
        self._html: str | None = None

    @classmethod
    def from_predictions(
        cls,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        sensitive_attr: pd.Series,
        X: pd.DataFrame | None = None,
        y_pred_proba: np.ndarray | None = None,
        fairness_threshold: float = 0.05,
    ) -> "FairnessReport":
        """
        Create report from model predictions.

        Args:
            y_true: True labels
            y_pred: Model predictions
            sensitive_attr: Sensitive attribute (e.g., gender, race)
            X: Feature matrix (optional, for pre-training metrics)
            y_pred_proba: Predicted probabilities (optional, for calibration)
            fairness_threshold: Threshold for fairness violations (default: 0.05)

        Returns:
            FairnessReport instance

        Example:
            >>> report = FairnessReport.from_predictions(
            ...     y_true=y_test,
            ...     y_pred=y_pred,
            ...     sensitive_attr=sensitive_test
            ... )
        """
        # Calculate metrics
        calculator = FairnessCalculator(cache_results=True)
        metrics = calculator.calculate_all(
            y_true=y_true,
            y_pred=y_pred,
            sensitive_attr=sensitive_attr,
            X=X,
            y_pred_proba=y_pred_proba,
        )

        # Transform data
        transformer = FairnessDataTransformer(fairness_threshold=fairness_threshold)
        transformed_data = transformer.transform(metrics)

        # Create charts
        factory = ChartFactory()
        charts = factory.create_all_charts(transformed_data)

        return cls(
            metrics=metrics, transformed_data=transformed_data, charts=charts
        )

    @classmethod
    def from_metrics(
        cls, metrics: dict[str, Any], fairness_threshold: float = 0.05
    ) -> "FairnessReport":
        """
        Create report from pre-calculated metrics.

        Args:
            metrics: Metrics from FairnessCalculator.calculate_all()
            fairness_threshold: Threshold for fairness violations

        Returns:
            FairnessReport instance

        Example:
            >>> from justiceai.core.metrics.calculator import FairnessCalculator
            >>> calculator = FairnessCalculator()
            >>> metrics = calculator.calculate_all(y_true, y_pred, sensitive)
            >>>
            >>> report = FairnessReport.from_metrics(metrics)
        """
        # Transform data
        transformer = FairnessDataTransformer(fairness_threshold=fairness_threshold)
        transformed_data = transformer.transform(metrics)

        # Create charts
        factory = ChartFactory()
        charts = factory.create_all_charts(transformed_data)

        return cls(
            metrics=metrics, transformed_data=transformed_data, charts=charts
        )

    def render_html(self, template_name: str = "fairness_report.html") -> str:
        """
        Render report as HTML.

        Args:
            template_name: Name of template file to use

        Returns:
            HTML string

        Example:
            >>> html = report.render_html()
        """
        if self._html is None:
            renderer = HTMLRenderer()
            self._html = renderer.render(
                self.transformed_data, self.charts, template_name
            )
        return self._html

    def save_html(
        self, output_path: str | Path, template_name: str = "fairness_report.html"
    ) -> None:
        """
        Save report as HTML file.

        Args:
            output_path: Path to save HTML file
            template_name: Template file name

        Example:
            >>> report.save_html('fairness_report.html')
        """
        html = self.render_html(template_name)
        renderer = HTMLRenderer()
        renderer.save(html, output_path)

    def show(self, output_path: str | Path = "fairness_report.html") -> None:
        """
        Save report and open in default web browser.

        Args:
            output_path: Path to save HTML file (default: 'fairness_report.html')

        Example:
            >>> report.show()  # Opens in browser
        """
        # Save HTML
        self.save_html(output_path)

        # Open in browser
        output_path = Path(output_path).absolute()
        webbrowser.open(f"file://{output_path}")

    def get_summary(self) -> dict[str, Any]:
        """
        Get summary statistics from report.

        Returns:
            Dictionary with summary metrics

        Example:
            >>> summary = report.get_summary()
            >>> print(f"Overall Score: {summary['overall_score']}")
            >>> print(f"Violations: {summary['n_violations']}")
        """
        return self.transformed_data.get("summary", {})

    def get_issues(self) -> list[dict[str, str]]:
        """
        Get list of detected fairness issues.

        Returns:
            List of issue dictionaries

        Example:
            >>> issues = report.get_issues()
            >>> for issue in issues:
            ...     print(f"{issue['severity']}: {issue['message']}")
        """
        return self.transformed_data.get("issues", [])

    def get_recommendations(self) -> list[dict[str, str]]:
        """
        Get list of recommendations.

        Returns:
            List of recommendation dictionaries

        Example:
            >>> recs = report.get_recommendations()
            >>> for rec in recs:
            ...     print(f"[{rec['priority']}] {rec['action']}")
        """
        return self.transformed_data.get("recommendations", [])

    def passes_fairness(self) -> bool:
        """
        Check if model passes basic fairness criteria.

        Returns:
            True if model passes, False otherwise

        Example:
            >>> if report.passes_fairness():
            ...     print("Model is fair!")
            ... else:
            ...     print("Model has fairness violations")
        """
        summary = self.get_summary()
        return summary.get("passes_fairness", False)

    def get_overall_score(self) -> float:
        """
        Get overall fairness score (0-100).

        Returns:
            Fairness score

        Example:
            >>> score = report.get_overall_score()
            >>> print(f"Fairness Score: {score:.1f}/100")
        """
        summary = self.get_summary()
        return summary.get("overall_score", 0.0)
