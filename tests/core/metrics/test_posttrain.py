"""Tests for post-training fairness metrics."""

import numpy as np
import pandas as pd
import pytest

from justiceai.core.metrics.posttrain import (
    confusion_matrix_by_group,
    disparate_impact,
    equal_opportunity,
    equalized_odds,
    statistical_parity,
)


class TestStatisticalParity:
    """Tests for statistical_parity function."""

    def test_perfect_parity(self) -> None:
        """Test with perfect statistical parity."""
        y_pred = np.array([1, 1, 1, 1])
        sensitive = pd.Series(["A", "A", "B", "B"])

        result = statistical_parity(y_pred, sensitive)

        assert result["difference"] == pytest.approx(0.0, abs=1e-5)
        assert result["ratio"] == pytest.approx(1.0, abs=1e-5)
        assert result["is_fair"]

    def test_imperfect_parity(self) -> None:
        """Test with imperfect parity."""
        y_pred = np.array([1, 1, 0, 0])
        sensitive = pd.Series(["A", "A", "B", "B"])

        result = statistical_parity(y_pred, sensitive)

        assert result["difference"] == pytest.approx(1.0, abs=1e-5)
        assert result["ratio"] == pytest.approx(0.0, abs=1e-5)
        assert not result["is_fair"]

    def test_multiple_groups(self) -> None:
        """Test with multiple groups."""
        y_pred = np.array([1, 1, 1, 0, 0, 0])
        sensitive = pd.Series(["A", "A", "B", "B", "C", "C"])

        result = statistical_parity(y_pred, sensitive)

        assert len(result["by_group"]) == 3
        assert "A" in result["by_group"]
        assert "B" in result["by_group"]
        assert "C" in result["by_group"]


class TestDisparateImpact:
    """Tests for disparate_impact function."""

    def test_passes_80_rule(self) -> None:
        """Test case that passes 80% rule."""
        y_pred = np.array([1, 1, 1, 1, 1, 0, 0, 0])
        sensitive = pd.Series(["A", "A", "A", "A", "B", "B", "B", "B"])

        result = disparate_impact(y_pred, sensitive)

        # Group A: 4/4 = 1.0, Group B: 1/4 = 0.25
        # Ratio: 0.25 / 1.0 = 0.25
        assert result["ratio"] == pytest.approx(0.25, abs=1e-2)
        assert not result["passes_80_rule"]

    def test_perfect_impact(self) -> None:
        """Test with no disparate impact."""
        y_pred = np.array([1, 0, 1, 0])
        sensitive = pd.Series(["A", "A", "B", "B"])

        result = disparate_impact(y_pred, sensitive)

        assert result["ratio"] == pytest.approx(1.0, abs=1e-5)
        assert result["passes_80_rule"]

    def test_identifies_advantaged_group(self) -> None:
        """Test that advantaged/disadvantaged groups are identified."""
        y_pred = np.array([1, 1, 0, 0])
        sensitive = pd.Series(["A", "A", "B", "B"])

        result = disparate_impact(y_pred, sensitive)

        assert result["advantaged_group"] == "A"
        assert result["disadvantaged_group"] == "B"


class TestEqualOpportunity:
    """Tests for equal_opportunity function."""

    def test_perfect_equal_opportunity(self) -> None:
        """Test with perfect equal opportunity (equal TPR)."""
        y_true = np.array([1, 1, 1, 1])
        y_pred = np.array([1, 1, 1, 1])
        sensitive = pd.Series(["A", "A", "B", "B"])

        result = equal_opportunity(y_true, y_pred, sensitive)

        assert result["difference"] == pytest.approx(0.0, abs=1e-5)
        assert result["is_fair"]

    def test_different_tpr(self) -> None:
        """Test with different TPRs across groups."""
        y_true = np.array([1, 1, 1, 1])
        y_pred = np.array([1, 1, 0, 0])
        sensitive = pd.Series(["A", "A", "B", "B"])

        result = equal_opportunity(y_true, y_pred, sensitive)

        # Group A: TPR = 2/2 = 1.0
        # Group B: TPR = 0/2 = 0.0
        assert result["difference"] == pytest.approx(1.0, abs=1e-5)
        assert not result["is_fair"]

    def test_no_positive_labels(self) -> None:
        """Test when group has no positive labels."""
        y_true = np.array([0, 0, 1, 1])
        y_pred = np.array([0, 0, 1, 0])
        sensitive = pd.Series(["A", "A", "B", "B"])

        result = equal_opportunity(y_true, y_pred, sensitive)

        # Group A has no positives, TPR = 0
        # Group B: TPR = 1/2 = 0.5
        assert "A" in result["by_group"]
        assert "B" in result["by_group"]


class TestEqualizedOdds:
    """Tests for equalized_odds function."""

    def test_perfect_equalized_odds(self) -> None:
        """Test with perfect equalized odds."""
        y_true = np.array([1, 1, 0, 0, 1, 1, 0, 0])
        y_pred = np.array([1, 0, 0, 1, 1, 0, 0, 1])
        sensitive = pd.Series(["A", "A", "A", "A", "B", "B", "B", "B"])

        result = equalized_odds(y_true, y_pred, sensitive)

        # Both groups should have same TPR and FPR
        assert result["tpr_difference"] == pytest.approx(0.0, abs=1e-5)
        assert result["fpr_difference"] == pytest.approx(0.0, abs=1e-5)
        assert result["is_fair"]

    def test_different_tpr_fpr(self) -> None:
        """Test with different TPR and FPR."""
        y_true = np.array([1, 1, 0, 0])
        y_pred = np.array([1, 1, 0, 0])
        sensitive = pd.Series(["A", "A", "A", "A"])

        result = equalized_odds(y_true, y_pred, sensitive)

        # Only one group, differences should be 0
        assert result["tpr_difference"] == 0.0
        assert result["fpr_difference"] == 0.0

    def test_confusion_matrix_components(self) -> None:
        """Test that confusion matrix components are correct."""
        y_true = np.array([1, 0])
        y_pred = np.array([1, 1])
        sensitive = pd.Series(["A", "A"])

        result = equalized_odds(y_true, y_pred, sensitive)

        assert result["by_group"]["A"]["tp"] == 1
        assert result["by_group"]["A"]["fp"] == 1
        assert result["by_group"]["A"]["tn"] == 0
        assert result["by_group"]["A"]["fn"] == 0


class TestConfusionMatrixByGroup:
    """Tests for confusion_matrix_by_group function."""

    def test_basic_confusion_matrix(self) -> None:
        """Test basic confusion matrix calculation."""
        y_true = np.array([1, 1, 0, 0])
        y_pred = np.array([1, 0, 0, 1])
        sensitive = pd.Series(["A", "A", "B", "B"])

        result = confusion_matrix_by_group(y_true, y_pred, sensitive)

        assert result["A"]["TP"] == 1
        assert result["A"]["FN"] == 1
        assert result["B"]["TN"] == 1
        assert result["B"]["FP"] == 1

    def test_perfect_predictions(self) -> None:
        """Test with perfect predictions."""
        y_true = np.array([1, 1, 0, 0])
        y_pred = np.array([1, 1, 0, 0])
        sensitive = pd.Series(["A", "A", "B", "B"])

        result = confusion_matrix_by_group(y_true, y_pred, sensitive)

        assert result["A"]["TP"] == 2
        assert result["A"]["FN"] == 0
        assert result["B"]["TN"] == 2
        assert result["B"]["FP"] == 0

    def test_all_wrong_predictions(self) -> None:
        """Test with all wrong predictions."""
        y_true = np.array([1, 1, 0, 0])
        y_pred = np.array([0, 0, 1, 1])
        sensitive = pd.Series(["A", "A", "B", "B"])

        result = confusion_matrix_by_group(y_true, y_pred, sensitive)

        assert result["A"]["TP"] == 0
        assert result["A"]["FN"] == 2
        assert result["B"]["TN"] == 0
        assert result["B"]["FP"] == 2

    def test_total_count(self) -> None:
        """Test that total count is correct."""
        y_true = np.array([1, 1, 0, 0, 1, 0])
        y_pred = np.array([1, 0, 0, 1, 1, 0])
        sensitive = pd.Series(["A", "A", "A", "B", "B", "B"])

        result = confusion_matrix_by_group(y_true, y_pred, sensitive)

        assert result["A"]["total"] == 3
        assert result["B"]["total"] == 3
        assert (
            result["A"]["TP"]
            + result["A"]["TN"]
            + result["A"]["FP"]
            + result["A"]["FN"]
            == 3
        )


class TestAdvancedMetrics:
    """Tests for advanced post-training metrics."""

    def test_false_negative_rate_difference(self) -> None:
        """Test FNR difference calculation."""
        from justiceai.core.metrics.posttrain import false_negative_rate_difference

        y_true = np.array([1, 1, 1, 1])
        y_pred = np.array([1, 0, 1, 1])
        sensitive = pd.Series(["A", "A", "B", "B"])

        result = false_negative_rate_difference(y_true, y_pred, sensitive)

        # Group A: FNR = 1/2 = 0.5
        # Group B: FNR = 0/2 = 0.0
        assert result["by_group"]["A"]["fnr"] == pytest.approx(0.5, abs=1e-5)
        assert result["by_group"]["B"]["fnr"] == pytest.approx(0.0, abs=1e-5)
        assert result["difference"] == pytest.approx(0.5, abs=1e-5)

    def test_predictive_parity(self) -> None:
        """Test predictive parity (PPV equality)."""
        from justiceai.core.metrics.posttrain import predictive_parity

        y_true = np.array([1, 1, 0, 0])
        y_pred = np.array([1, 1, 1, 0])
        sensitive = pd.Series(["A", "A", "B", "B"])

        result = predictive_parity(y_true, y_pred, sensitive)

        # Group A: PPV = 2/2 = 1.0
        # Group B: PPV = 0/1 = 0.0
        assert result["by_group"]["A"]["ppv"] == pytest.approx(1.0, abs=1e-5)
        assert result["by_group"]["B"]["ppv"] == pytest.approx(0.0, abs=1e-5)

    def test_negative_predictive_parity(self) -> None:
        """Test negative predictive parity (NPV equality)."""
        from justiceai.core.metrics.posttrain import negative_predictive_parity

        y_true = np.array([1, 1, 0, 0])
        y_pred = np.array([0, 1, 0, 0])
        sensitive = pd.Series(["A", "A", "B", "B"])

        result = negative_predictive_parity(y_true, y_pred, sensitive)

        # Group A: NPV = 0/1 = 0.0 (TN=0, FN=1)
        # Group B: NPV = 2/2 = 1.0 (TN=2, FN=0)
        assert result["by_group"]["A"]["npv"] == pytest.approx(0.0, abs=1e-5)
        assert result["by_group"]["B"]["npv"] == pytest.approx(1.0, abs=1e-5)

    def test_accuracy_difference(self) -> None:
        """Test accuracy difference across groups."""
        from justiceai.core.metrics.posttrain import accuracy_difference

        y_true = np.array([1, 1, 0, 0])
        y_pred = np.array([1, 1, 0, 0])
        sensitive = pd.Series(["A", "A", "B", "B"])

        result = accuracy_difference(y_true, y_pred, sensitive)

        # Both groups: 100% accuracy
        assert result["by_group"]["A"]["accuracy"] == pytest.approx(1.0, abs=1e-5)
        assert result["by_group"]["B"]["accuracy"] == pytest.approx(1.0, abs=1e-5)
        assert result["difference"] == pytest.approx(0.0, abs=1e-5)
        assert result["is_fair"]

    def test_treatment_equality(self) -> None:
        """Test treatment equality (FN/FP ratio)."""
        from justiceai.core.metrics.posttrain import treatment_equality

        y_true = np.array([1, 1, 0, 0])
        y_pred = np.array([0, 1, 1, 0])
        sensitive = pd.Series(["A", "A", "B", "B"])

        result = treatment_equality(y_true, y_pred, sensitive)

        # Group A: FN=1, FP=1, ratio=1.0
        # Group B: FN=0, FP=0, ratio=1.0
        assert "A" in result["by_group"]
        assert "B" in result["by_group"]

    def test_calibration_by_group(self) -> None:
        """Test calibration calculation."""
        from justiceai.core.metrics.posttrain import calibration_by_group

        y_true = np.array([1, 0, 1, 0, 1, 0, 1, 0])
        y_proba = np.array([0.9, 0.1, 0.8, 0.2, 0.7, 0.3, 0.6, 0.4])
        sensitive = pd.Series(["A", "A", "A", "A", "B", "B", "B", "B"])

        result = calibration_by_group(y_true, y_proba, sensitive, n_bins=5)

        assert "A" in result["by_group"]
        assert "B" in result["by_group"]
        assert "expected_calibration_error" in result["by_group"]["A"]
        assert result["by_group"]["A"]["expected_calibration_error"] >= 0
