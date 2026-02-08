"""
Threshold analysis charts.

This module provides charts for visualizing threshold analysis results
from the ThresholdAnalyzer.
"""

from typing import Any

import plotly.graph_objects as go

from justiceai.reports.charts.base_chart import COLOR_INFO, BaseChart


class ThresholdTradeoffCurve(BaseChart):
    """
    Scatter plot showing fairness-performance trade-off across thresholds.

    This chart helps identify the optimal decision threshold that balances
    fairness and performance objectives.
    """

    def create(self, data: dict[str, Any]) -> str:
        """
        Create threshold trade-off curve.

        Args:
            data: Dictionary with 'threshold_analysis' containing:
                - thresholds: List of threshold values
                - fairness_values: List of fairness metric values
                - performance_values: List of performance metric values
                - optimal_threshold: Optimal threshold value (optional)
                - fairness_metric_name: Name of fairness metric
                - performance_metric_name: Name of performance metric

        Returns:
            Plotly JSON string
        """
        threshold_data = data.get("threshold_analysis", {})

        if not threshold_data:
            return "{}"

        thresholds = threshold_data.get("thresholds", [])
        fairness_values = threshold_data.get("fairness_values", [])
        performance_values = threshold_data.get("performance_values", [])

        if not thresholds or not fairness_values or not performance_values:
            return "{}"

        fairness_metric = threshold_data.get("fairness_metric_name", "Fairness")
        performance_metric = threshold_data.get(
            "performance_metric_name", "Performance"
        )
        optimal_threshold = threshold_data.get("optimal_threshold")

        # Create trace for all thresholds
        fig = go.Figure()

        fig.add_trace(
            go.Scatter(
                x=fairness_values,
                y=performance_values,
                mode="markers+lines",
                marker={
                    "size": 8,
                    "color": thresholds,
                    "colorscale": "Viridis",
                    "showscale": True,
                    "colorbar": {"title": "Threshold"},
                },
                line={"color": COLOR_INFO, "width": 2},
                text=[f"Threshold: {t:.2f}" for t in thresholds],
                hovertemplate="<b>%{text}</b><br>"
                + f"{fairness_metric}: %{{x:.4f}}<br>"
                + f"{performance_metric}: %{{y:.4f}}<extra></extra>",
                name="Trade-off Curve",
            )
        )

        # Highlight optimal threshold if provided
        if optimal_threshold is not None and optimal_threshold in thresholds:
            idx = thresholds.index(optimal_threshold)
            fig.add_trace(
                go.Scatter(
                    x=[fairness_values[idx]],
                    y=[performance_values[idx]],
                    mode="markers",
                    marker={
                        "size": 15,
                        "color": "red",
                        "symbol": "star",
                        "line": {"width": 2, "color": "darkred"},
                    },
                    text=[f"Optimal: {optimal_threshold:.2f}"],
                    hovertemplate="<b>%{text}</b><br>"
                    + f"{fairness_metric}: %{{x:.4f}}<br>"
                    + f"{performance_metric}: %{{y:.4f}}<extra></extra>",
                    name="Optimal",
                )
            )

        fig.update_xaxes(title=fairness_metric)
        fig.update_yaxes(title=performance_metric)

        self._apply_common_layout(
            fig,
            title=f"{fairness_metric} vs {performance_metric} Trade-off",
            height=500,
            show_legend=True,
        )

        return self._to_json(fig)


class ThresholdMetricsLine(BaseChart):
    """Line plot showing how metrics change across thresholds."""

    def create(self, data: dict[str, Any]) -> str:
        """
        Create threshold metrics line chart.

        Args:
            data: Dictionary with 'threshold_analysis' containing:
                - thresholds: List of threshold values
                - metrics: Dict of metric_name -> list of values

        Returns:
            Plotly JSON string
        """
        threshold_data = data.get("threshold_analysis", {})

        if not threshold_data:
            return "{}"

        thresholds = threshold_data.get("thresholds", [])
        metrics = threshold_data.get("metrics", {})

        if not thresholds or not metrics:
            return "{}"

        fig = go.Figure()

        # Add trace for each metric
        for metric_name, values in metrics.items():
            if len(values) != len(thresholds):
                continue

            fig.add_trace(
                go.Scatter(
                    x=thresholds,
                    y=values,
                    mode="lines+markers",
                    name=metric_name,
                    hovertemplate=f"<b>{metric_name}</b><br>"
                    + "Threshold: %{x:.2f}<br>"
                    + "Value: %{y:.4f}<extra></extra>",
                )
            )

        fig.update_xaxes(title="Decision Threshold", range=[0, 1])
        fig.update_yaxes(title="Metric Value")

        self._apply_common_layout(
            fig,
            title="Metrics Across Thresholds",
            height=450,
            show_legend=True,
        )

        return self._to_json(fig)
