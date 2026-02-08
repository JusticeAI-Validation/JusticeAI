"""Tests for FairnessReport builder."""

from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from justiceai.core.metrics.calculator import FairnessCalculator
from justiceai.reports import FairnessReport


class TestFairnessReport:
    """Tests for FairnessReport class."""

    @pytest.fixture
    def sample_data(self) -> dict:
        """Create sample prediction data."""
        np.random.seed(42)
        n_samples = 100

        return {
            "y_true": np.random.randint(0, 2, n_samples),
            "y_pred": np.random.randint(0, 2, n_samples),
            "sensitive": pd.Series(np.random.choice(["A", "B"], n_samples)),
            "X": pd.DataFrame(
                np.random.randn(n_samples, 5),
                columns=[f"feature_{i}" for i in range(5)],
            ),
        }

    def test_from_predictions(self, sample_data: dict) -> None:
        """Test creating report from predictions."""
        report = FairnessReport.from_predictions(
            y_true=sample_data["y_true"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
        )

        assert isinstance(report, FairnessReport)
        assert report.metrics is not None
        assert report.transformed_data is not None
        assert report.charts is not None

    def test_from_predictions_with_X(self, sample_data: dict) -> None:
        """Test creating report with features."""
        report = FairnessReport.from_predictions(
            y_true=sample_data["y_true"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
            X=sample_data["X"],
        )

        assert "pretrain" in report.metrics

    def test_from_metrics(self, sample_data: dict) -> None:
        """Test creating report from pre-calculated metrics."""
        calculator = FairnessCalculator()
        metrics = calculator.calculate_all(
            y_true=sample_data["y_true"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
        )

        report = FairnessReport.from_metrics(metrics)

        assert isinstance(report, FairnessReport)
        assert report.metrics == metrics

    def test_render_html(self, sample_data: dict) -> None:
        """Test rendering HTML."""
        report = FairnessReport.from_predictions(
            y_true=sample_data["y_true"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
        )

        html = report.render_html()

        assert isinstance(html, str)
        assert len(html) > 0
        assert "<html" in html.lower()
        assert "justiceai" in html.lower()

    def test_render_html_caching(self, sample_data: dict) -> None:
        """Test that HTML rendering is cached."""
        report = FairnessReport.from_predictions(
            y_true=sample_data["y_true"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
        )

        html1 = report.render_html()
        html2 = report.render_html()

        # Should return same object (cached)
        assert html1 is html2

    def test_save_html(self, sample_data: dict, tmp_path: Path) -> None:
        """Test saving HTML to file."""
        report = FairnessReport.from_predictions(
            y_true=sample_data["y_true"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
        )

        output_path = tmp_path / "report.html"
        report.save_html(output_path)

        assert output_path.exists()
        assert output_path.stat().st_size > 0

        # Verify content
        html = output_path.read_text(encoding="utf-8")
        assert "justiceai" in html.lower()

    def test_get_summary(self, sample_data: dict) -> None:
        """Test getting summary statistics."""
        report = FairnessReport.from_predictions(
            y_true=sample_data["y_true"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
        )

        summary = report.get_summary()

        assert isinstance(summary, dict)
        assert "overall_score" in summary
        assert "n_violations" in summary
        assert "passes_fairness" in summary

    def test_get_issues(self, sample_data: dict) -> None:
        """Test getting issues list."""
        report = FairnessReport.from_predictions(
            y_true=sample_data["y_true"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
        )

        issues = report.get_issues()

        assert isinstance(issues, list)
        # Issues may or may not exist depending on data

    def test_get_recommendations(self, sample_data: dict) -> None:
        """Test getting recommendations."""
        report = FairnessReport.from_predictions(
            y_true=sample_data["y_true"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
        )

        recs = report.get_recommendations()

        assert isinstance(recs, list)
        assert len(recs) > 0  # Should always have at least one recommendation

    def test_passes_fairness(self, sample_data: dict) -> None:
        """Test checking fairness pass/fail."""
        report = FairnessReport.from_predictions(
            y_true=sample_data["y_true"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
        )

        result = report.passes_fairness()

        assert isinstance(result, bool)

    def test_passes_fairness_perfect_data(self) -> None:
        """Test fairness check with perfect fairness."""
        # Create perfectly fair data
        y_true = np.array([1, 0, 1, 0])
        y_pred = np.array([1, 0, 1, 0])
        sensitive = pd.Series(["A", "A", "B", "B"])

        report = FairnessReport.from_predictions(
            y_true=y_true, y_pred=y_pred, sensitive_attr=sensitive
        )

        assert report.passes_fairness() is True

    def test_get_overall_score(self, sample_data: dict) -> None:
        """Test getting overall fairness score."""
        report = FairnessReport.from_predictions(
            y_true=sample_data["y_true"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
        )

        score = report.get_overall_score()

        assert isinstance(score, float)
        assert 0 <= score <= 100

    def test_custom_fairness_threshold(self, sample_data: dict) -> None:
        """Test creating report with custom fairness threshold."""
        report = FairnessReport.from_predictions(
            y_true=sample_data["y_true"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
            fairness_threshold=0.1,
        )

        assert isinstance(report, FairnessReport)

    def test_with_probabilities(self, sample_data: dict) -> None:
        """Test creating report with predicted probabilities."""
        y_pred_proba = np.random.rand(len(sample_data["y_true"]))

        report = FairnessReport.from_predictions(
            y_true=sample_data["y_true"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
            y_pred_proba=y_pred_proba,
        )

        # Should include calibration metrics
        assert "calibration" in report.metrics.get("posttrain", {})

    def test_show_creates_file(self, sample_data: dict, tmp_path: Path) -> None:
        """Test that show() creates HTML file."""
        report = FairnessReport.from_predictions(
            y_true=sample_data["y_true"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
        )

        output_path = tmp_path / "test_show.html"

        # Note: This won't actually open the browser in tests
        # We just verify file creation
        try:
            report.show(output_path)
        except Exception:
            # Browser opening may fail in test environment
            pass

        # File should be created regardless
        assert output_path.exists()

    def test_integration_full_pipeline(self, sample_data: dict, tmp_path: Path) -> None:
        """Test full pipeline from predictions to HTML."""
        # Create report
        report = FairnessReport.from_predictions(
            y_true=sample_data["y_true"],
            y_pred=sample_data["y_pred"],
            sensitive_attr=sample_data["sensitive"],
            X=sample_data["X"],
        )

        # Get summary
        summary = report.get_summary()
        assert "overall_score" in summary

        # Get issues and recommendations
        issues = report.get_issues()
        recs = report.get_recommendations()
        assert isinstance(issues, list)
        assert isinstance(recs, list)

        # Render HTML
        html = report.render_html()
        assert len(html) > 1000  # Should be substantial

        # Save
        output_path = tmp_path / "integration_report.html"
        report.save_html(output_path)
        assert output_path.exists()
