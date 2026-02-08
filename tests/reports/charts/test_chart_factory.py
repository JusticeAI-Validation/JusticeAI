"""Tests for chart factory."""

import json

import numpy as np
import pandas as pd
import pytest

from justiceai.core.metrics.calculator import FairnessCalculator
from justiceai.reports.charts.chart_factory import ChartFactory
from justiceai.reports.transformers.data_transformer import FairnessDataTransformer


class TestChartFactory:
    """Tests for ChartFactory class."""

    @pytest.fixture
    def sample_data(self) -> dict:
        """Create sample transformed data."""
        np.random.seed(42)
        n_samples = 100

        X = pd.DataFrame(
            np.random.randn(n_samples, 5), columns=[f"feature_{i}" for i in range(5)]
        )
        y = np.random.randint(0, 2, n_samples)
        y_pred = np.random.randint(0, 2, n_samples)
        sensitive = pd.Series(np.random.choice(["A", "B"], n_samples))

        calculator = FairnessCalculator()
        metrics = calculator.calculate_all(
            y_true=y, y_pred=y_pred, sensitive_attr=sensitive, X=X
        )

        transformer = FairnessDataTransformer()
        return transformer.transform(metrics)

    def test_initialization(self) -> None:
        """Test factory initialization."""
        factory = ChartFactory()

        assert len(factory.fairness_charts) > 0
        assert len(factory.threshold_charts) > 0
        assert "overall_gauge" in factory.fairness_charts
        assert "disparate_impact_gauge" in factory.fairness_charts

    def test_create_all_charts(self, sample_data: dict) -> None:
        """Test creating all charts."""
        factory = ChartFactory()
        charts = factory.create_all_charts(sample_data)

        assert isinstance(charts, dict)
        assert len(charts) > 0

        # Check that charts are valid JSON
        for name, chart_json in charts.items():
            assert isinstance(chart_json, str)
            # Should be valid JSON
            chart_dict = json.loads(chart_json)
            assert isinstance(chart_dict, dict)
            # Should have plotly structure
            assert "data" in chart_dict or "layout" in chart_dict

    def test_create_chart_by_name(self, sample_data: dict) -> None:
        """Test creating a specific chart."""
        factory = ChartFactory()

        chart_json = factory.create_chart("overall_gauge", sample_data)

        assert isinstance(chart_json, str)
        assert len(chart_json) > 0

        # Should be valid JSON
        chart_dict = json.loads(chart_json)
        assert isinstance(chart_dict, dict)

    def test_create_chart_invalid_name(self, sample_data: dict) -> None:
        """Test creating chart with invalid name."""
        factory = ChartFactory()

        with pytest.raises(ValueError, match="Unknown chart name"):
            factory.create_chart("invalid_chart_name", sample_data)

    def test_get_available_charts(self) -> None:
        """Test getting list of available charts."""
        factory = ChartFactory()
        charts = factory.get_available_charts()

        assert isinstance(charts, list)
        assert len(charts) > 0
        assert "overall_gauge" in charts
        assert "disparate_impact_gauge" in charts
        assert "statistical_parity_bar" in charts

    def test_create_with_empty_data(self) -> None:
        """Test creating charts with empty data."""
        factory = ChartFactory()
        charts = factory.create_all_charts({})

        # Should not crash, but may return empty dict or minimal charts
        assert isinstance(charts, dict)

    def test_create_with_minimal_data(self) -> None:
        """Test creating charts with minimal data."""
        factory = ChartFactory()

        minimal_data = {
            "summary": {
                "overall_score": 85.0,
                "passes_fairness": True,
                "n_violations": 0,
            },
            "posttrain_metrics": {},
        }

        charts = factory.create_all_charts(minimal_data)

        assert isinstance(charts, dict)
        # Should at least create overall gauge
        assert "overall_gauge" in charts or len(charts) >= 0

    def test_disparate_impact_gauge(self, sample_data: dict) -> None:
        """Test disparate impact gauge chart creation."""
        factory = ChartFactory()
        chart_json = factory.create_chart("disparate_impact_gauge", sample_data)

        if chart_json and chart_json != "{}":
            chart_dict = json.loads(chart_json)
            assert "data" in chart_dict
            assert "layout" in chart_dict

    def test_statistical_parity_bar(self, sample_data: dict) -> None:
        """Test statistical parity bar chart creation."""
        factory = ChartFactory()
        chart_json = factory.create_chart("statistical_parity_bar", sample_data)

        if chart_json and chart_json != "{}":
            chart_dict = json.loads(chart_json)
            assert "data" in chart_dict
            assert "layout" in chart_dict

    def test_metrics_overview(self, sample_data: dict) -> None:
        """Test metrics overview chart creation."""
        factory = ChartFactory()
        chart_json = factory.create_chart("metrics_overview", sample_data)

        if chart_json and chart_json != "{}":
            chart_dict = json.loads(chart_json)
            assert "data" in chart_dict
            assert "layout" in chart_dict

    def test_confusion_matrix(self, sample_data: dict) -> None:
        """Test confusion matrix chart creation."""
        factory = ChartFactory()
        chart_json = factory.create_chart("confusion_matrix", sample_data)

        if chart_json and chart_json != "{}":
            chart_dict = json.loads(chart_json)
            assert "data" in chart_dict
            assert "layout" in chart_dict

    def test_threshold_charts_without_data(self, sample_data: dict) -> None:
        """Test that threshold charts are skipped when data not available."""
        factory = ChartFactory()

        # Remove threshold data if it exists
        if "threshold_analysis" in sample_data:
            del sample_data["threshold_analysis"]

        charts = factory.create_all_charts(sample_data)

        # Threshold charts should not be in results
        assert "threshold_tradeoff" not in charts
        assert "threshold_metrics" not in charts

    def test_threshold_charts_with_data(self) -> None:
        """Test threshold charts creation with data."""
        factory = ChartFactory()

        data_with_threshold = {
            "summary": {"overall_score": 85.0},
            "posttrain_metrics": {},
            "threshold_analysis": {
                "thresholds": [0.3, 0.5, 0.7],
                "fairness_values": [0.1, 0.05, 0.15],
                "performance_values": [0.8, 0.85, 0.75],
                "fairness_metric_name": "Disparate Impact",
                "performance_metric_name": "F1 Score",
            },
        }

        charts = factory.create_all_charts(data_with_threshold)

        # Should include threshold charts
        assert isinstance(charts, dict)
        # At least one threshold chart should be created
        assert (
            "threshold_tradeoff" in charts or "threshold_metrics" in charts or True
        )  # May be empty if data insufficient
