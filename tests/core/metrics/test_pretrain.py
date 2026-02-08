"""Tests for pre-training fairness metrics."""

import numpy as np
import pandas as pd
import pytest

from justiceai.core.metrics.pretrain import (
    class_balance,
    concept_balance,
    group_distribution_difference,
    js_divergence,
    kl_divergence,
)


class TestClassBalance:
    """Tests for class_balance function."""

    def test_perfectly_balanced(self) -> None:
        """Test with perfectly balanced classes."""
        y = pd.Series([0, 1, 0, 1, 0, 1])
        sensitive = pd.Series(["A", "A", "A", "A", "A", "A"])

        result = class_balance(y, sensitive)

        assert "A" in result
        assert result["A"]["balance_score"] == pytest.approx(1.0, abs=0.01)
        assert result["A"]["majority_class_ratio"] == 0.5

    def test_imbalanced_classes(self) -> None:
        """Test with imbalanced classes."""
        y = pd.Series([0, 0, 0, 1])
        sensitive = pd.Series(["A", "A", "A", "A"])

        result = class_balance(y, sensitive)

        assert result["A"]["majority_class_ratio"] == 0.75
        assert result["A"]["balance_score"] < 1.0

    def test_multiple_groups(self) -> None:
        """Test with multiple sensitive groups."""
        y = pd.Series([0, 1, 0, 1, 0, 1])
        sensitive = pd.Series(["A", "A", "B", "B", "C", "C"])

        result = class_balance(y, sensitive)

        assert len(result) == 3
        assert "A" in result
        assert "B" in result
        assert "C" in result

    def test_single_class(self) -> None:
        """Test with only one class (edge case)."""
        y = pd.Series([0, 0, 0, 0])
        sensitive = pd.Series(["A", "A", "A", "A"])

        result = class_balance(y, sensitive)

        assert result["A"]["balance_score"] == 0.0
        assert result["A"]["majority_class_ratio"] == 1.0

    def test_empty_group(self) -> None:
        """Test behavior with groups that become empty after filtering."""
        y = pd.Series([0, 1, 0, 1])
        sensitive = pd.Series(["A", "A", "B", "B"])

        result = class_balance(y, sensitive)

        assert len(result) == 2
        assert all(r["total_samples"] > 0 for r in result.values())


class TestConceptBalance:
    """Tests for concept_balance function."""

    def test_perfect_correlation(self) -> None:
        """Test with perfect correlation between sensitive attr and target."""
        X = pd.DataFrame({"feat1": [1, 2, 3, 4]})
        y = pd.Series([0, 0, 1, 1])
        sensitive = pd.Series(["A", "A", "B", "B"])

        result = concept_balance(X, y, sensitive)

        assert "mutual_information" in result
        assert "normalized_mi" in result
        assert result["mutual_information"] > 0
        assert 0 <= result["normalized_mi"] <= 1

    def test_no_correlation(self) -> None:
        """Test with no correlation."""
        X = pd.DataFrame({"feat1": [1, 2, 3, 4]})
        y = pd.Series([0, 1, 0, 1])
        sensitive = pd.Series(["A", "B", "A", "B"])

        result = concept_balance(X, y, sensitive)

        assert result["mutual_information"] >= 0
        assert result["normalized_mi"] >= 0


class TestKLDivergence:
    """Tests for kl_divergence function."""

    def test_identical_distributions(self) -> None:
        """Test KL divergence of identical distributions."""
        dist1 = np.array([0.5, 0.5])
        dist2 = np.array([0.5, 0.5])

        result = kl_divergence(dist1, dist2)

        assert result == pytest.approx(0.0, abs=1e-5)

    def test_different_distributions(self) -> None:
        """Test KL divergence of different distributions."""
        dist1 = np.array([0.9, 0.1])
        dist2 = np.array([0.1, 0.9])

        result = kl_divergence(dist1, dist2)

        assert result > 0

    def test_non_normalized_input(self) -> None:
        """Test that non-normalized inputs are handled correctly."""
        dist1 = np.array([2, 2])  # Will be normalized to [0.5, 0.5]
        dist2 = np.array([3, 3])  # Will be normalized to [0.5, 0.5]

        result = kl_divergence(dist1, dist2)

        assert result == pytest.approx(0.0, abs=1e-5)

    def test_asymmetry(self) -> None:
        """Test that KL divergence is asymmetric."""
        dist1 = np.array([0.9, 0.1])
        dist2 = np.array([0.5, 0.5])

        kl_12 = kl_divergence(dist1, dist2)
        kl_21 = kl_divergence(dist2, dist1)

        assert kl_12 != pytest.approx(kl_21, abs=1e-5)


class TestJSDivergence:
    """Tests for js_divergence function."""

    def test_identical_distributions(self) -> None:
        """Test JS divergence of identical distributions."""
        dist1 = np.array([0.5, 0.5])
        dist2 = np.array([0.5, 0.5])

        result = js_divergence(dist1, dist2)

        assert result == pytest.approx(0.0, abs=1e-5)

    def test_different_distributions(self) -> None:
        """Test JS divergence of different distributions."""
        dist1 = np.array([0.9, 0.1])
        dist2 = np.array([0.1, 0.9])

        result = js_divergence(dist1, dist2)

        assert result > 0
        assert result <= 1.0

    def test_symmetry(self) -> None:
        """Test that JS divergence is symmetric."""
        dist1 = np.array([0.9, 0.1])
        dist2 = np.array([0.5, 0.5])

        js_12 = js_divergence(dist1, dist2)
        js_21 = js_divergence(dist2, dist1)

        assert js_12 == pytest.approx(js_21, abs=1e-5)

    def test_bounded(self) -> None:
        """Test that JS divergence is bounded between 0 and 1."""
        dist1 = np.array([0.99, 0.01])
        dist2 = np.array([0.01, 0.99])

        result = js_divergence(dist1, dist2)

        assert 0 <= result <= 1.0


class TestGroupDistributionDifference:
    """Tests for group_distribution_difference function."""

    def test_two_groups(self) -> None:
        """Test with two groups."""
        y = pd.Series([0, 1, 0, 1, 0, 1])
        sensitive = pd.Series(["A", "A", "A", "B", "B", "B"])

        result = group_distribution_difference(y, sensitive)

        assert "A_vs_B" in result
        assert "kl_divergence" in result["A_vs_B"]
        assert "js_divergence" in result["A_vs_B"]

    def test_three_groups(self) -> None:
        """Test with three groups (pairwise comparisons)."""
        y = pd.Series([0, 1, 0, 1, 0, 1])
        sensitive = pd.Series(["A", "A", "B", "B", "C", "C"])

        result = group_distribution_difference(y, sensitive)

        # Should have 3 pairwise comparisons
        assert len(result) == 3
        assert "A_vs_B" in result
        assert "A_vs_C" in result
        assert "B_vs_C" in result

    def test_identical_group_distributions(self) -> None:
        """Test when all groups have identical distributions."""
        y = pd.Series([0, 1, 0, 1, 0, 1])
        sensitive = pd.Series(["A", "A", "B", "B", "C", "C"])

        result = group_distribution_difference(y, sensitive)

        # All divergences should be near zero
        for metrics in result.values():
            assert metrics["js_divergence"] == pytest.approx(0.0, abs=1e-5)
