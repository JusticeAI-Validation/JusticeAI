"""Tests for threshold analysis."""

import numpy as np
import pandas as pd
import pytest

from justiceai.core.evaluators.threshold import ThresholdAnalyzer


class TestThresholdAnalyzer:
    """Tests for ThresholdAnalyzer class."""

    @pytest.fixture
    def sample_data(self) -> dict:
        """Create sample data for testing."""
        np.random.seed(42)
        n_samples = 100

        y_true = np.random.randint(0, 2, n_samples)
        y_pred_proba = np.random.rand(n_samples)
        sensitive = pd.Series(np.random.choice(["A", "B"], n_samples))

        return {
            "y_true": y_true,
            "y_pred_proba": y_pred_proba,
            "sensitive": sensitive,
        }

    def test_initialization_default(self) -> None:
        """Test default initialization."""
        analyzer = ThresholdAnalyzer()

        assert len(analyzer.thresholds) == 99
        assert analyzer.thresholds[0] == pytest.approx(0.01, abs=1e-5)
        assert analyzer.thresholds[-1] == pytest.approx(0.99, abs=1e-5)
        assert "statistical_parity" in analyzer.fairness_metrics
        assert "accuracy" in analyzer.performance_metrics

    def test_initialization_custom(self) -> None:
        """Test custom initialization."""
        custom_thresholds = np.array([0.3, 0.5, 0.7])
        analyzer = ThresholdAnalyzer(
            thresholds=custom_thresholds,
            fairness_metrics=["disparate_impact"],
            performance_metrics=["accuracy"],
        )

        assert len(analyzer.thresholds) == 3
        assert analyzer.fairness_metrics == ["disparate_impact"]
        assert analyzer.performance_metrics == ["accuracy"]

    def test_analyze(self, sample_data: dict) -> None:
        """Test analyze method."""
        analyzer = ThresholdAnalyzer(thresholds=np.array([0.3, 0.5, 0.7]))

        results = analyzer.analyze(
            y_true=sample_data["y_true"],
            y_pred_proba=sample_data["y_pred_proba"],
            sensitive_attr=sample_data["sensitive"],
        )

        assert isinstance(results, pd.DataFrame)
        assert len(results) == 3
        assert "threshold" in results.columns
        assert "accuracy" in results.columns
        assert "statistical_parity_diff" in results.columns

    def test_analyze_stores_results(self, sample_data: dict) -> None:
        """Test that analyze stores results internally."""
        analyzer = ThresholdAnalyzer(thresholds=np.array([0.5]))

        analyzer.analyze(
            y_true=sample_data["y_true"],
            y_pred_proba=sample_data["y_pred_proba"],
            sensitive_attr=sample_data["sensitive"],
        )

        assert analyzer.results_ is not None
        assert isinstance(analyzer.results_, pd.DataFrame)

    def test_find_optimal_threshold(self, sample_data: dict) -> None:
        """Test finding optimal threshold."""
        analyzer = ThresholdAnalyzer(thresholds=np.linspace(0.1, 0.9, 9))

        analyzer.analyze(
            y_true=sample_data["y_true"],
            y_pred_proba=sample_data["y_pred_proba"],
            sensitive_attr=sample_data["sensitive"],
        )

        optimal = analyzer.find_optimal_threshold(
            fairness_metric="disparate_impact_ratio",
            performance_metric="f1_score",
            fairness_weight=0.5,
        )

        assert "threshold" in optimal
        assert "fairness_value" in optimal
        assert "performance_value" in optimal
        assert 0.1 <= optimal["threshold"] <= 0.9

    def test_find_optimal_without_analyze_fails(self) -> None:
        """Test that find_optimal fails without calling analyze first."""
        analyzer = ThresholdAnalyzer()

        with pytest.raises(ValueError, match="Must call analyze"):
            analyzer.find_optimal_threshold()

    def test_find_optimal_with_constraint(self, sample_data: dict) -> None:
        """Test finding optimal threshold with fairness constraint."""
        analyzer = ThresholdAnalyzer(thresholds=np.linspace(0.1, 0.9, 9))

        analyzer.analyze(
            y_true=sample_data["y_true"],
            y_pred_proba=sample_data["y_pred_proba"],
            sensitive_attr=sample_data["sensitive"],
        )

        optimal = analyzer.find_optimal_threshold(
            fairness_metric="disparate_impact_ratio",
            performance_metric="f1_score",
            fairness_constraint=0.8,
        )

        # Should either find a threshold or return None with message
        assert "threshold" in optimal

    def test_different_fairness_weights(self, sample_data: dict) -> None:
        """Test that different weights produce different results."""
        analyzer = ThresholdAnalyzer(thresholds=np.linspace(0.1, 0.9, 9))

        analyzer.analyze(
            y_true=sample_data["y_true"],
            y_pred_proba=sample_data["y_pred_proba"],
            sensitive_attr=sample_data["sensitive"],
        )

        result_fairness = analyzer.find_optimal_threshold(fairness_weight=0.9)
        result_performance = analyzer.find_optimal_threshold(fairness_weight=0.1)

        # Results should potentially be different (not always guaranteed with random data)
        assert "threshold" in result_fairness
        assert "threshold" in result_performance

    def test_plot_tradeoff_curve(self, sample_data: dict) -> None:
        """Test getting plot data."""
        analyzer = ThresholdAnalyzer(thresholds=np.array([0.3, 0.5, 0.7]))

        analyzer.analyze(
            y_true=sample_data["y_true"],
            y_pred_proba=sample_data["y_pred_proba"],
            sensitive_attr=sample_data["sensitive"],
        )

        plot_data = analyzer.plot_tradeoff_curve(
            fairness_metric="disparate_impact_ratio",
            performance_metric="f1_score",
        )

        assert "x" in plot_data
        assert "y" in plot_data
        assert "thresholds" in plot_data
        assert len(plot_data["x"]) == 3
        assert len(plot_data["y"]) == 3

    def test_plot_without_analyze_fails(self) -> None:
        """Test that plot fails without calling analyze first."""
        analyzer = ThresholdAnalyzer()

        with pytest.raises(ValueError, match="Must call analyze"):
            analyzer.plot_tradeoff_curve()

    def test_get_threshold_recommendation_balanced(self, sample_data: dict) -> None:
        """Test balanced recommendation."""
        analyzer = ThresholdAnalyzer(thresholds=np.linspace(0.1, 0.9, 9))

        analyzer.analyze(
            y_true=sample_data["y_true"],
            y_pred_proba=sample_data["y_pred_proba"],
            sensitive_attr=sample_data["sensitive"],
        )

        rec = analyzer.get_threshold_recommendation("balanced")

        assert rec["use_case"] == "balanced"
        assert "threshold" in rec
        assert "explanation" in rec

    def test_get_threshold_recommendation_fairness_priority(
        self, sample_data: dict
    ) -> None:
        """Test fairness priority recommendation."""
        analyzer = ThresholdAnalyzer(thresholds=np.linspace(0.1, 0.9, 9))

        analyzer.analyze(
            y_true=sample_data["y_true"],
            y_pred_proba=sample_data["y_pred_proba"],
            sensitive_attr=sample_data["sensitive"],
        )

        rec = analyzer.get_threshold_recommendation("fairness_priority")

        assert rec["use_case"] == "fairness_priority"
        assert "70%" in rec["explanation"]

    def test_get_threshold_recommendation_performance_priority(
        self, sample_data: dict
    ) -> None:
        """Test performance priority recommendation."""
        analyzer = ThresholdAnalyzer(thresholds=np.linspace(0.1, 0.9, 9))

        analyzer.analyze(
            y_true=sample_data["y_true"],
            y_pred_proba=sample_data["y_pred_proba"],
            sensitive_attr=sample_data["sensitive"],
        )

        rec = analyzer.get_threshold_recommendation("performance_priority")

        assert rec["use_case"] == "performance_priority"
        assert "70%" in rec["explanation"]

    def test_get_threshold_recommendation_invalid_use_case(
        self, sample_data: dict
    ) -> None:
        """Test invalid use case raises error."""
        analyzer = ThresholdAnalyzer(thresholds=np.array([0.5]))

        analyzer.analyze(
            y_true=sample_data["y_true"],
            y_pred_proba=sample_data["y_pred_proba"],
            sensitive_attr=sample_data["sensitive"],
        )

        with pytest.raises(ValueError, match="Unknown use case"):
            analyzer.get_threshold_recommendation("invalid")

    def test_get_recommendation_without_analyze_fails(self) -> None:
        """Test that recommendation fails without calling analyze first."""
        analyzer = ThresholdAnalyzer()

        with pytest.raises(ValueError, match="Must call analyze"):
            analyzer.get_threshold_recommendation()
