"""Tests for data transformer."""

import numpy as np
import pandas as pd
import pytest

from justiceai.core.metrics.calculator import FairnessCalculator
from justiceai.reports.transformers.data_transformer import (
    FairnessDataTransformer,
    format_metric_value,
    get_status_from_value,
)


class TestStatusFunctions:
    """Tests for status determination functions."""

    def test_get_status_ratio_success(self) -> None:
        """Test status for ratio metrics - success case."""
        status = get_status_from_value("disparate_impact_ratio", 0.85)
        assert status == "success"

    def test_get_status_ratio_warning(self) -> None:
        """Test status for ratio metrics - warning case."""
        status = get_status_from_value("disparate_impact_ratio", 0.75)
        assert status == "warning"

    def test_get_status_ratio_critical(self) -> None:
        """Test status for ratio metrics - critical case."""
        status = get_status_from_value("disparate_impact_ratio", 0.5)
        assert status == "critical"

    def test_get_status_difference_success(self) -> None:
        """Test status for difference metrics - success case."""
        status = get_status_from_value("statistical_parity_diff", 0.02)
        assert status == "success"

    def test_get_status_difference_warning(self) -> None:
        """Test status for difference metrics - warning case."""
        status = get_status_from_value("statistical_parity_diff", 0.08)
        assert status == "warning"

    def test_get_status_difference_critical(self) -> None:
        """Test status for difference metrics - critical case."""
        status = get_status_from_value("statistical_parity_diff", 0.15)
        assert status == "critical"

    def test_get_status_custom_threshold(self) -> None:
        """Test status with custom threshold."""
        status = get_status_from_value("difference", 0.15, threshold=0.1)
        assert status == "warning"


class TestFormatMetricValue:
    """Tests for metric value formatting."""

    def test_format_int(self) -> None:
        """Test formatting integer values."""
        assert format_metric_value(42) == "42"
        assert format_metric_value(np.int64(100)) == "100"

    def test_format_float(self) -> None:
        """Test formatting float values."""
        assert format_metric_value(0.12345) == "0.123"
        assert format_metric_value(0.001) == "0.0010"
        assert format_metric_value(np.float64(0.5)) == "0.500"

    def test_format_bool(self) -> None:
        """Test formatting boolean values."""
        assert format_metric_value(True) == "✓ Pass"
        assert format_metric_value(False) == "✗ Fail"

    def test_format_string(self) -> None:
        """Test formatting string values."""
        assert format_metric_value("test") == "test"


class TestFairnessDataTransformer:
    """Tests for FairnessDataTransformer class."""

    @pytest.fixture
    def sample_metrics(self) -> dict:
        """Create sample metrics from calculator."""
        np.random.seed(42)
        n_samples = 100

        X = pd.DataFrame(
            np.random.randn(n_samples, 5), columns=[f"feature_{i}" for i in range(5)]
        )
        y = np.random.randint(0, 2, n_samples)
        y_pred = np.random.randint(0, 2, n_samples)
        sensitive = pd.Series(np.random.choice(["A", "B"], n_samples))

        calculator = FairnessCalculator()
        return calculator.calculate_all(
            y_true=y, y_pred=y_pred, sensitive_attr=sensitive, X=X
        )

    @pytest.fixture
    def perfect_fairness_metrics(self) -> dict:
        """Create metrics with perfect fairness."""
        y_true = np.array([1, 0, 1, 0])
        y_pred = np.array([1, 0, 1, 0])
        sensitive = pd.Series(["A", "A", "B", "B"])

        calculator = FairnessCalculator()
        return calculator.calculate_all(
            y_true=y_true, y_pred=y_pred, sensitive_attr=sensitive
        )

    def test_initialization(self) -> None:
        """Test transformer initialization."""
        transformer = FairnessDataTransformer()
        assert transformer.fairness_threshold == 0.05

        transformer = FairnessDataTransformer(fairness_threshold=0.1)
        assert transformer.fairness_threshold == 0.1

    def test_transform_structure(self, sample_metrics: dict) -> None:
        """Test that transform returns correct structure."""
        transformer = FairnessDataTransformer()
        result = transformer.transform(sample_metrics)

        assert isinstance(result, dict)
        assert "summary" in result
        assert "posttrain_metrics" in result
        assert "issues" in result
        assert "recommendations" in result
        assert "pretrain_metrics" in result

    def test_transform_summary(self, sample_metrics: dict) -> None:
        """Test summary transformation."""
        transformer = FairnessDataTransformer()
        result = transformer.transform(sample_metrics)

        summary = result["summary"]
        assert "overall_score" in summary
        assert "n_violations" in summary
        assert "passes_fairness" in summary
        assert "violations" in summary
        assert "status" in summary

        assert isinstance(summary["overall_score"], float)
        assert 0 <= summary["overall_score"] <= 100
        assert isinstance(summary["n_violations"], int)
        assert isinstance(summary["passes_fairness"], bool)
        assert isinstance(summary["violations"], list)
        assert summary["status"] in ["success", "critical"]

    def test_transform_pretrain_metrics(self, sample_metrics: dict) -> None:
        """Test pre-training metrics transformation."""
        transformer = FairnessDataTransformer()
        result = transformer.transform(sample_metrics)

        pretrain = result.get("pretrain_metrics", {})
        assert isinstance(pretrain, dict)

        if "class_balance" in pretrain:
            assert "groups" in pretrain["class_balance"]
            assert "status" in pretrain["class_balance"]

    def test_transform_posttrain_metrics(self, sample_metrics: dict) -> None:
        """Test post-training metrics transformation."""
        transformer = FairnessDataTransformer()
        result = transformer.transform(sample_metrics)

        posttrain = result["posttrain_metrics"]
        assert isinstance(posttrain, dict)

        # Check key metrics are present
        if "statistical_parity" in posttrain:
            sp = posttrain["statistical_parity"]
            assert "difference" in sp
            assert "ratio" in sp
            assert "is_fair" in sp
            assert "status" in sp

        if "disparate_impact" in posttrain:
            di = posttrain["disparate_impact"]
            assert "ratio" in di
            assert "passes_80_rule" in di
            assert "status" in di

    def test_extract_issues_with_violations(self, sample_metrics: dict) -> None:
        """Test issues extraction with violations."""
        transformer = FairnessDataTransformer()
        result = transformer.transform(sample_metrics)

        issues = result["issues"]
        assert isinstance(issues, list)

        # Each issue should have required fields
        for issue in issues:
            assert "severity" in issue
            assert "metric" in issue
            assert "message" in issue
            assert "impact" in issue
            assert issue["severity"] in ["critical", "warning"]

    def test_extract_issues_no_violations(
        self, perfect_fairness_metrics: dict
    ) -> None:
        """Test issues extraction without violations."""
        transformer = FairnessDataTransformer()
        result = transformer.transform(perfect_fairness_metrics)

        issues = result["issues"]
        assert isinstance(issues, list)
        assert len(issues) == 0

    def test_extract_recommendations_with_violations(
        self, sample_metrics: dict
    ) -> None:
        """Test recommendations extraction with violations."""
        transformer = FairnessDataTransformer()
        result = transformer.transform(sample_metrics)

        recommendations = result["recommendations"]
        assert isinstance(recommendations, list)
        assert len(recommendations) > 0

        # Each recommendation should have required fields
        for rec in recommendations:
            assert "priority" in rec
            assert "action" in rec
            assert "description" in rec
            assert rec["priority"] in ["high", "medium", "low", "info"]

    def test_extract_recommendations_no_violations(
        self, perfect_fairness_metrics: dict
    ) -> None:
        """Test recommendations without violations."""
        transformer = FairnessDataTransformer()
        result = transformer.transform(perfect_fairness_metrics)

        recommendations = result["recommendations"]
        assert isinstance(recommendations, list)
        assert len(recommendations) >= 1
        assert any("Maintain current practices" in rec["action"] for rec in recommendations)

    def test_transform_without_pretrain(self) -> None:
        """Test transform without pre-training metrics."""
        # Create metrics without X (no pretrain)
        y_true = np.array([1, 0, 1, 0, 1, 0])
        y_pred = np.array([1, 0, 1, 0, 0, 1])
        sensitive = pd.Series(["A", "A", "A", "B", "B", "B"])

        calculator = FairnessCalculator()
        metrics = calculator.calculate_all(
            y_true=y_true, y_pred=y_pred, sensitive_attr=sensitive
        )

        transformer = FairnessDataTransformer()
        result = transformer.transform(metrics)

        assert "pretrain_metrics" not in result or result.get("pretrain_metrics") == {}

    def test_transform_statistical_parity_status(self) -> None:
        """Test status assignment for statistical parity."""
        # Create metrics with violation
        y_true = np.array([1, 1, 1, 1])
        y_pred = np.array([1, 1, 0, 0])
        sensitive = pd.Series(["A", "A", "B", "B"])

        calculator = FairnessCalculator()
        metrics = calculator.calculate_all(
            y_true=y_true, y_pred=y_pred, sensitive_attr=sensitive
        )

        transformer = FairnessDataTransformer()
        result = transformer.transform(metrics)

        sp = result["posttrain_metrics"].get("statistical_parity", {})
        assert sp.get("status") == "critical"

    def test_transform_disparate_impact_status(self) -> None:
        """Test status assignment for disparate impact."""
        # Create metrics with violation
        y_true = np.array([1, 1, 1, 1])
        y_pred = np.array([1, 1, 0, 0])
        sensitive = pd.Series(["A", "A", "B", "B"])

        calculator = FairnessCalculator()
        metrics = calculator.calculate_all(
            y_true=y_true, y_pred=y_pred, sensitive_attr=sensitive
        )

        transformer = FairnessDataTransformer()
        result = transformer.transform(metrics)

        di = result["posttrain_metrics"].get("disparate_impact", {})
        assert di.get("status") == "critical"

    def test_custom_threshold(self) -> None:
        """Test transformer with custom threshold."""
        transformer = FairnessDataTransformer(fairness_threshold=0.1)

        # Create metrics
        y_true = np.array([1, 0, 1, 0, 1, 0])
        y_pred = np.array([1, 0, 1, 0, 0, 1])
        sensitive = pd.Series(["A", "A", "A", "B", "B", "B"])

        calculator = FairnessCalculator()
        metrics = calculator.calculate_all(
            y_true=y_true, y_pred=y_pred, sensitive_attr=sensitive
        )

        result = transformer.transform(metrics)

        # Just verify it runs without error
        assert "summary" in result
        assert transformer.fairness_threshold == 0.1
