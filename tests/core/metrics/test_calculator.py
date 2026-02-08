"""Tests for unified fairness calculator."""

import numpy as np
import pandas as pd
import pytest

from justiceai.core.metrics.calculator import FairnessCalculator


class TestFairnessCalculator:
    """Tests for FairnessCalculator class."""

    @pytest.fixture
    def sample_data(self) -> dict:
        """Create sample data for testing."""
        np.random.seed(42)
        n_samples = 100

        X = pd.DataFrame(
            np.random.randn(n_samples, 5), columns=[f"feature_{i}" for i in range(5)]
        )
        y = np.random.randint(0, 2, n_samples)
        y_pred = np.random.randint(0, 2, n_samples)
        y_pred_proba = np.random.rand(n_samples)
        sensitive = pd.Series(np.random.choice(["A", "B"], n_samples))

        return {
            "X": X,
            "y": y,
            "y_pred": y_pred,
            "y_pred_proba": y_pred_proba,
            "sensitive": sensitive,
        }

    def test_initialization_with_cache(self) -> None:
        """Test initialization with cache enabled."""
        calculator = FairnessCalculator(cache_results=True)

        assert calculator.cache_results
        assert isinstance(calculator.cache, dict)
        assert len(calculator.cache) == 0
        assert not calculator._validated

    def test_initialization_without_cache(self) -> None:
        """Test initialization with cache disabled."""
        calculator = FairnessCalculator(cache_results=False)

        assert not calculator.cache_results
        assert isinstance(calculator.cache, dict)

    def test_validate_inputs_success(self, sample_data: dict) -> None:
        """Test input validation with valid inputs."""
        calculator = FairnessCalculator()

        # Should not raise any errors
        calculator._validate_inputs(
            y_true=sample_data["y"],
            y_pred=sample_data["y_pred"],
            y_pred_proba=sample_data["y_pred_proba"],
            sensitive_attr=sample_data["sensitive"],
            X=sample_data["X"],
        )

        assert calculator._validated

    def test_validate_inputs_length_mismatch_y(self) -> None:
        """Test validation fails with mismatched lengths."""
        calculator = FairnessCalculator()

        with pytest.raises(ValueError, match="y_true and y_pred must have same length"):
            calculator._validate_inputs(
                y_true=np.array([1, 2, 3]), y_pred=np.array([1, 2])
            )

    def test_validate_inputs_length_mismatch_sensitive(self) -> None:
        """Test validation fails with mismatched sensitive attribute."""
        calculator = FairnessCalculator()

        with pytest.raises(
            ValueError, match="y_pred and sensitive_attr must have same length"
        ):
            calculator._validate_inputs(
                y_pred=np.array([1, 2, 3]), sensitive_attr=pd.Series(["A", "B"])
            )

    def test_calculate_pretrain_metrics(self, sample_data: dict) -> None:
        """Test pre-training metrics calculation."""
        calculator = FairnessCalculator()

        results = calculator.calculate_pretrain_metrics(
            X=sample_data["X"], y=pd.Series(sample_data["y"]), sensitive_attr=sample_data["sensitive"]
        )

        assert isinstance(results, dict)
        assert "class_balance" in results
        assert "concept_balance" in results
        assert "group_distribution_difference" in results

    def test_calculate_pretrain_metrics_caching(self, sample_data: dict) -> None:
        """Test that pre-training metrics are cached."""
        calculator = FairnessCalculator(cache_results=True)

        results1 = calculator.calculate_pretrain_metrics(
            X=sample_data["X"], y=pd.Series(sample_data["y"]), sensitive_attr=sample_data["sensitive"]
        )

        # Second call should return cached results
        results2 = calculator.calculate_pretrain_metrics(
            X=sample_data["X"], y=pd.Series(sample_data["y"]), sensitive_attr=sample_data["sensitive"]
        )

        assert results1 is results2  # Same object reference
        assert "pretrain" in calculator.cache

    def test_calculate_posttrain_metrics(self, sample_data: dict) -> None:
        """Test post-training metrics calculation."""
        calculator = FairnessCalculator()

        results = calculator.calculate_posttrain_metrics(
            y_true=sample_data["y"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
        )

        assert isinstance(results, dict)
        assert "statistical_parity" in results
        assert "disparate_impact" in results
        assert "equal_opportunity" in results
        assert "equalized_odds" in results
        assert "confusion_matrix" in results
        assert "false_negative_rate_diff" in results
        assert "predictive_parity" in results
        assert "negative_predictive_parity" in results
        assert "accuracy_difference" in results
        assert "treatment_equality" in results

    def test_calculate_posttrain_metrics_with_proba(self, sample_data: dict) -> None:
        """Test post-training metrics with probabilities."""
        calculator = FairnessCalculator()

        results = calculator.calculate_posttrain_metrics(
            y_true=sample_data["y"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
            y_pred_proba=sample_data["y_pred_proba"],
        )

        assert "calibration" in results

    def test_calculate_posttrain_metrics_caching(self, sample_data: dict) -> None:
        """Test that post-training metrics are cached."""
        calculator = FairnessCalculator(cache_results=True)

        results1 = calculator.calculate_posttrain_metrics(
            y_true=sample_data["y"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
        )

        results2 = calculator.calculate_posttrain_metrics(
            y_true=sample_data["y"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
        )

        assert results1 is results2
        assert "posttrain" in calculator.cache

    def test_calculate_all_with_X(self, sample_data: dict) -> None:
        """Test calculating all metrics with features."""
        calculator = FairnessCalculator()

        results = calculator.calculate_all(
            y_true=sample_data["y"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
            X=sample_data["X"],
            y_pred_proba=sample_data["y_pred_proba"],
        )

        assert isinstance(results, dict)
        assert "pretrain" in results
        assert "posttrain" in results
        assert "summary" in results

    def test_calculate_all_without_X(self, sample_data: dict) -> None:
        """Test calculating all metrics without features."""
        calculator = FairnessCalculator()

        results = calculator.calculate_all(
            y_true=sample_data["y"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
        )

        assert isinstance(results, dict)
        assert "pretrain" not in results
        assert "posttrain" in results
        assert "summary" in results

    def test_calculate_summary_structure(self, sample_data: dict) -> None:
        """Test summary statistics structure."""
        calculator = FairnessCalculator()

        results = calculator.calculate_all(
            y_true=sample_data["y"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
        )

        summary = results["summary"]
        assert "overall_fairness_score" in summary
        assert "fairness_violations" in summary
        assert "n_violations" in summary
        assert "disparate_impact_ratio" in summary
        assert "statistical_parity_diff" in summary
        assert "passes_basic_fairness" in summary

        assert isinstance(summary["overall_fairness_score"], float)
        assert 0 <= summary["overall_fairness_score"] <= 100
        assert isinstance(summary["fairness_violations"], list)
        assert isinstance(summary["n_violations"], int)
        assert isinstance(summary["passes_basic_fairness"], bool)

    def test_calculate_summary_perfect_fairness(self) -> None:
        """Test summary with perfect fairness."""
        calculator = FairnessCalculator()

        # Create perfectly fair data (same distribution across groups)
        y_true = np.array([1, 0, 1, 0])
        y_pred = np.array([1, 0, 1, 0])
        sensitive = pd.Series(["A", "A", "B", "B"])

        results = calculator.calculate_all(
            y_true=y_true, y_pred=y_pred, sensitive_attr=sensitive
        )

        summary = results["summary"]
        assert summary["overall_fairness_score"] == 100.0
        assert summary["n_violations"] == 0
        assert summary["passes_basic_fairness"]

    def test_calculate_summary_with_violations(self) -> None:
        """Test summary with fairness violations."""
        calculator = FairnessCalculator()

        # Create unfair data
        y_true = np.array([1, 1, 1, 1])
        y_pred = np.array([1, 1, 0, 0])
        sensitive = pd.Series(["A", "A", "B", "B"])

        results = calculator.calculate_all(
            y_true=y_true, y_pred=y_pred, sensitive_attr=sensitive
        )

        summary = results["summary"]
        assert summary["overall_fairness_score"] < 100.0
        assert summary["n_violations"] > 0
        assert not summary["passes_basic_fairness"]

    def test_get_recommendations_with_results(self, sample_data: dict) -> None:
        """Test getting recommendations with provided results."""
        calculator = FairnessCalculator()

        results = calculator.calculate_all(
            y_true=sample_data["y"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
        )

        recommendations = calculator.get_recommendations(results)

        assert isinstance(recommendations, list)
        assert len(recommendations) > 0
        assert all(isinstance(rec, str) for rec in recommendations)

    def test_get_recommendations_from_cache(self, sample_data: dict) -> None:
        """Test getting recommendations from cache."""
        calculator = FairnessCalculator(cache_results=True)

        calculator.calculate_all(
            y_true=sample_data["y"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
        )

        # Should use cached results
        recommendations = calculator.get_recommendations()

        assert isinstance(recommendations, list)
        assert len(recommendations) > 0

    def test_get_recommendations_without_cache_fails(self) -> None:
        """Test that recommendations fail without cached results."""
        calculator = FairnessCalculator(cache_results=True)

        with pytest.raises(ValueError, match="No cached results"):
            calculator.get_recommendations()

    def test_get_recommendations_no_violations(self) -> None:
        """Test recommendations when no violations detected."""
        calculator = FairnessCalculator()

        # Create perfectly fair data (same distribution across groups)
        y_true = np.array([1, 0, 1, 0])
        y_pred = np.array([1, 0, 1, 0])
        sensitive = pd.Series(["A", "A", "B", "B"])

        results = calculator.calculate_all(
            y_true=y_true, y_pred=y_pred, sensitive_attr=sensitive
        )

        recommendations = calculator.get_recommendations(results)

        assert len(recommendations) == 1
        assert "No major fairness violations" in recommendations[0]

    def test_get_recommendations_statistical_parity_violation(self) -> None:
        """Test recommendations for statistical parity violation."""
        calculator = FairnessCalculator()

        # Create data with statistical parity violation
        y_true = np.array([1, 1, 1, 1])
        y_pred = np.array([1, 1, 0, 0])
        sensitive = pd.Series(["A", "A", "B", "B"])

        results = calculator.calculate_all(
            y_true=y_true, y_pred=y_pred, sensitive_attr=sensitive
        )

        recommendations = calculator.get_recommendations(results)

        # Should have recommendations about violations
        assert any("Statistical parity" in rec for rec in recommendations)

    def test_clear_cache(self, sample_data: dict) -> None:
        """Test clearing cache."""
        calculator = FairnessCalculator(cache_results=True)

        calculator.calculate_all(
            y_true=sample_data["y"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
        )

        assert len(calculator.cache) > 0

        calculator.clear_cache()

        assert len(calculator.cache) == 0

    def test_multiple_calculations_with_cache(self, sample_data: dict) -> None:
        """Test multiple calculations with caching enabled."""
        calculator = FairnessCalculator(cache_results=True)

        # First calculation
        results1 = calculator.calculate_all(
            y_true=sample_data["y"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
        )

        # Second calculation should use cache
        results2 = calculator.calculate_all(
            y_true=sample_data["y"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
        )

        # Verify cache was used (same object references)
        assert results1["posttrain"] is results2["posttrain"]

    def test_multiple_calculations_without_cache(self, sample_data: dict) -> None:
        """Test multiple calculations without caching."""
        calculator = FairnessCalculator(cache_results=False)

        # First calculation
        results1 = calculator.calculate_all(
            y_true=sample_data["y"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
        )

        # Second calculation should recalculate
        results2 = calculator.calculate_all(
            y_true=sample_data["y"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
        )

        # Should be different objects (not cached)
        assert results1 is not results2
