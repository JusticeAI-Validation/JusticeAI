"""Integration tests for public API (audit function)."""

import tempfile
from pathlib import Path
from unittest.mock import patch

import numpy as np
import pandas as pd
import pytest
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier

from justiceai import audit
from justiceai.reports import FairnessReport


class TestAuditAPI:
    """Integration tests for audit() convenience function."""

    @pytest.fixture
    def sample_data(self) -> tuple:
        """Create sample classification data."""
        X, y = make_classification(
            n_samples=150,
            n_features=5,
            n_classes=2,
            random_state=42,
            flip_y=0.1,
        )

        # Create sensitive attribute
        gender = pd.Series(
            np.random.choice(["Male", "Female"], size=150, p=[0.55, 0.45]),
            name="gender",
        )

        return X, y, gender

    @pytest.fixture
    def trained_model(self, sample_data: tuple) -> RandomForestClassifier:
        """Create and train a model."""
        X, y, _ = sample_data
        model = RandomForestClassifier(n_estimators=30, random_state=42)
        model.fit(X, y)
        return model

    def test_audit_basic(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test basic audit() call."""
        X, y, gender = sample_data

        report = audit(
            model=trained_model,
            X=X,
            y_true=y,
            sensitive_attrs=gender,
        )

        assert isinstance(report, FairnessReport)
        assert report.get_overall_score() >= 0
        assert isinstance(report.get_summary(), dict)

    def test_audit_with_dataframe(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test audit() with pandas DataFrame."""
        X, y, gender = sample_data

        X_df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(X.shape[1])])
        y_series = pd.Series(y, name="target")

        report = audit(
            model=trained_model,
            X=X_df,
            y_true=y_series,
            sensitive_attrs=gender,
        )

        assert isinstance(report, FairnessReport)

    def test_audit_with_dict_sensitive_attrs(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test audit() with dictionary of sensitive attributes."""
        X, y, gender = sample_data

        report = audit(
            model=trained_model,
            X=X,
            y_true=y,
            sensitive_attrs={"gender": gender},
        )

        assert isinstance(report, FairnessReport)

    def test_audit_custom_threshold(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test audit() with custom fairness threshold."""
        X, y, gender = sample_data

        report = audit(
            model=trained_model,
            X=X,
            y_true=y,
            sensitive_attrs=gender,
            fairness_threshold=0.10,
        )

        assert isinstance(report, FairnessReport)

    def test_audit_save_html(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test audit() with HTML output."""
        X, y, gender = sample_data

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "fairness_report.html"

            report = audit(
                model=trained_model,
                X=X,
                y_true=y,
                sensitive_attrs=gender,
                output_path=str(output_path),
            )

            assert isinstance(report, FairnessReport)
            assert output_path.exists()
            assert output_path.stat().st_size > 0

            # Verify it's valid HTML
            content = output_path.read_text()
            assert "<!DOCTYPE html>" in content or "<html" in content
            assert "Fairness" in content

    def test_audit_without_save(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test audit() without saving report."""
        X, y, gender = sample_data

        report = audit(
            model=trained_model,
            X=X,
            y_true=y,
            sensitive_attrs=gender,
            output_path=None,
        )

        assert isinstance(report, FairnessReport)

    def test_audit_show_false(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test audit() with show=False (default)."""
        X, y, gender = sample_data

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "report.html"

            report = audit(
                model=trained_model,
                X=X,
                y_true=y,
                sensitive_attrs=gender,
                output_path=str(output_path),
                show=False,
            )

            assert isinstance(report, FairnessReport)
            assert output_path.exists()

    def test_audit_multiple_calls(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test multiple audit() calls."""
        X, y, gender = sample_data

        report1 = audit(
            model=trained_model,
            X=X,
            y_true=y,
            sensitive_attrs=gender,
        )

        report2 = audit(
            model=trained_model,
            X=X,
            y_true=y,
            sensitive_attrs=gender,
            fairness_threshold=0.10,
        )

        assert isinstance(report1, FairnessReport)
        assert isinstance(report2, FairnessReport)

        # Scores might differ due to different thresholds
        score1 = report1.get_overall_score()
        score2 = report2.get_overall_score()

        assert isinstance(score1, (int, float))
        assert isinstance(score2, (int, float))

    def test_audit_report_methods(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test that returned report has all expected methods."""
        X, y, gender = sample_data

        report = audit(
            model=trained_model,
            X=X,
            y_true=y,
            sensitive_attrs=gender,
        )

        # Test all report methods
        assert hasattr(report, "get_overall_score")
        assert hasattr(report, "passes_fairness")
        assert hasattr(report, "get_issues")
        assert hasattr(report, "get_summary")
        assert hasattr(report, "save_html")
        assert hasattr(report, "show")

        # Test methods work
        assert isinstance(report.get_overall_score(), (int, float))
        assert isinstance(report.passes_fairness(), bool)
        assert isinstance(report.get_issues(), list)
        assert isinstance(report.get_summary(), dict)

    def test_audit_with_numpy_arrays(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test audit() with all numpy arrays."""
        X, y, gender = sample_data

        report = audit(
            model=trained_model,
            X=np.array(X),
            y_true=np.array(y),
            sensitive_attrs=gender,
        )

        assert isinstance(report, FairnessReport)

    def test_audit_end_to_end_workflow(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test complete end-to-end audit workflow."""
        X, y, gender = sample_data

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "complete_audit.html"

            # Perform complete audit
            report = audit(
                model=trained_model,
                X=X,
                y_true=y,
                sensitive_attrs=gender,
                fairness_threshold=0.05,
                output_path=str(output_path),
                show=False,
            )

            # Verify report
            assert isinstance(report, FairnessReport)
            assert output_path.exists()

            # Verify score is valid
            score = report.get_overall_score()
            assert 0 <= score <= 100

            # Verify summary contains expected keys
            summary = report.get_summary()
            assert isinstance(summary, dict)
            assert "overall_score" in summary
            assert "n_violations" in summary
            assert "passes_fairness" in summary

            # Verify issues list
            issues = report.get_issues()
            assert isinstance(issues, list)

            # Verify HTML content
            html_content = output_path.read_text()
            assert len(html_content) > 0
            assert "Fairness" in html_content

    def test_audit_quick_iteration(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test audit() for quick iteration scenario."""
        X, y, gender = sample_data

        # Quick check without saving
        report = audit(model=trained_model, X=X, y_true=y, sensitive_attrs=gender)

        # Check basic metrics
        score = report.get_overall_score()
        passes = report.passes_fairness()

        assert isinstance(score, (int, float))
        assert isinstance(passes, bool)

        # If issues found, get details
        if not passes:
            issues = report.get_issues()
            assert len(issues) > 0

    @patch("webbrowser.open")
    def test_audit_with_show_and_path(
        self, mock_browser: any, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test audit() with show=True and output_path."""
        X, y, gender = sample_data

        with tempfile.TemporaryDirectory() as tmpdir:
            output_path = Path(tmpdir) / "report_to_show.html"

            report = audit(
                model=trained_model,
                X=X,
                y_true=y,
                sensitive_attrs=gender,
                output_path=str(output_path),
                show=True,
            )

            assert isinstance(report, FairnessReport)
            assert output_path.exists()
            # Verify browser was called with the path
            mock_browser.assert_called_once()

    @patch("webbrowser.open")
    def test_audit_with_show_no_path(
        self, mock_browser: any, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test audit() with show=True but no output_path."""
        X, y, gender = sample_data

        report = audit(
            model=trained_model,
            X=X,
            y_true=y,
            sensitive_attrs=gender,
            show=True,
        )

        assert isinstance(report, FairnessReport)
        # Verify browser was called
        mock_browser.assert_called_once()
