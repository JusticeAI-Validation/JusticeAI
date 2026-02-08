"""
Chart factory for creating all fairness visualizations.

This module orchestrates the creation of all charts from transformed data.
"""

from typing import Any

from justiceai.reports.charts.fairness_charts import (
    ConfusionMatrixHeatmap,
    DisparateImpactGauge,
    MetricsOverviewBar,
    OverallFairnessGauge,
    StatisticalParityBar,
)
from justiceai.reports.charts.threshold_charts import (
    ThresholdMetricsLine,
    ThresholdTradeoffCurve,
)


class ChartFactory:
    """
    Factory for creating all fairness charts.

    This class takes transformed data and creates all relevant charts,
    handling errors gracefully to prevent cascading failures.

    Example:
        >>> from justiceai.reports.transformers.data_transformer import FairnessDataTransformer
        >>> transformer = FairnessDataTransformer()
        >>> report_data = transformer.transform(metrics)
        >>>
        >>> factory = ChartFactory()
        >>> charts = factory.create_all_charts(report_data)
        >>> print(charts.keys())
    """

    def __init__(self):
        """Initialize chart factory with all chart types."""
        self.fairness_charts = {
            "overall_gauge": OverallFairnessGauge(),
            "disparate_impact_gauge": DisparateImpactGauge(),
            "statistical_parity_bar": StatisticalParityBar(),
            "metrics_overview": MetricsOverviewBar(),
            "confusion_matrix": ConfusionMatrixHeatmap(),
        }

        self.threshold_charts = {
            "threshold_tradeoff": ThresholdTradeoffCurve(),
            "threshold_metrics": ThresholdMetricsLine(),
        }

    def create_all_charts(self, data: dict[str, Any]) -> dict[str, str]:
        """
        Create all charts from transformed data.

        Each chart is created independently with error handling to prevent
        cascading failures.

        Args:
            data: Transformed data dictionary from FairnessDataTransformer

        Returns:
            Dictionary mapping chart name to Plotly JSON string
        """
        charts = {}

        # Create fairness charts
        for name, chart in self.fairness_charts.items():
            try:
                chart_json = chart.create(data)
                if chart_json and chart_json != "{}":
                    charts[name] = chart_json
            except Exception as e:
                # Log error but continue with other charts
                print(f"Warning: Failed to create chart '{name}': {e}")
                continue

        # Create threshold charts if data available
        if "threshold_analysis" in data:
            for name, chart in self.threshold_charts.items():
                try:
                    chart_json = chart.create(data)
                    if chart_json and chart_json != "{}":
                        charts[name] = chart_json
                except Exception as e:
                    print(f"Warning: Failed to create chart '{name}': {e}")
                    continue

        return charts

    def create_chart(self, chart_name: str, data: dict[str, Any]) -> str:
        """
        Create a single chart by name.

        Args:
            chart_name: Name of the chart to create
            data: Transformed data dictionary

        Returns:
            Plotly JSON string or empty dict if chart not found/failed

        Raises:
            ValueError: If chart_name is not recognized
        """
        # Look in fairness charts
        if chart_name in self.fairness_charts:
            return self.fairness_charts[chart_name].create(data)

        # Look in threshold charts
        if chart_name in self.threshold_charts:
            return self.threshold_charts[chart_name].create(data)

        raise ValueError(
            f"Unknown chart name: {chart_name}. "
            f"Available charts: {list(self.fairness_charts.keys()) + list(self.threshold_charts.keys())}"
        )

    def get_available_charts(self) -> list[str]:
        """
        Get list of all available chart names.

        Returns:
            List of chart names
        """
        return list(self.fairness_charts.keys()) + list(self.threshold_charts.keys())
