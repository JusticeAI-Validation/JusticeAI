"""Tests for HTML renderer."""

import json
from pathlib import Path

import numpy as np
import pandas as pd
import pytest

from justiceai.core.metrics.calculator import FairnessCalculator
from justiceai.reports.charts.chart_factory import ChartFactory
from justiceai.reports.renderers.html_renderer import HTMLRenderer
from justiceai.reports.transformers.data_transformer import FairnessDataTransformer


class TestHTMLRenderer:
    """Tests for HTMLRenderer class."""

    @pytest.fixture
    def sample_data_and_charts(self) -> tuple[dict, dict]:
        """Create sample data and charts for testing."""
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
        data = transformer.transform(metrics)

        factory = ChartFactory()
        charts = factory.create_all_charts(data)

        return data, charts

    def test_initialization_default(self) -> None:
        """Test renderer initialization with default template path."""
        renderer = HTMLRenderer()

        assert renderer.env is not None
        assert len(renderer.env.loader.searchpath) > 0

    def test_initialization_custom_path(self, tmp_path: Path) -> None:
        """Test renderer initialization with custom template path."""
        # Create a temporary template directory
        template_dir = tmp_path / "templates"
        template_dir.mkdir()

        # Create a simple template
        (template_dir / "test.html").write_text("<html>{{ test }}</html>")

        renderer = HTMLRenderer(template_path=str(template_dir))

        assert renderer.env is not None
        assert str(template_dir) in renderer.env.loader.searchpath

    def test_initialization_invalid_path(self) -> None:
        """Test that initialization fails with invalid path."""
        with pytest.raises(ValueError, match="Template directory not found"):
            HTMLRenderer(template_path="/nonexistent/path")

    def test_render(self, sample_data_and_charts: tuple) -> None:
        """Test rendering HTML from data and charts."""
        data, charts = sample_data_and_charts
        renderer = HTMLRenderer()

        html = renderer.render(data, charts)

        assert isinstance(html, str)
        assert len(html) > 0
        assert "<html" in html.lower()
        assert "</html>" in html.lower()
        assert "JusticeAI" in html

    def test_render_contains_summary(self, sample_data_and_charts: tuple) -> None:
        """Test that rendered HTML contains summary data."""
        data, charts = sample_data_and_charts
        renderer = HTMLRenderer()

        html = renderer.render(data, charts)

        # Should contain overall score
        assert "Overall Score" in html or "overall" in html.lower()

    def test_render_contains_charts(self, sample_data_and_charts: tuple) -> None:
        """Test that rendered HTML includes chart scripts."""
        data, charts = sample_data_and_charts
        renderer = HTMLRenderer()

        html = renderer.render(data, charts)

        # Should include Plotly script
        assert "plotly" in html.lower() or "Plotly" in html

        # Should include chart data
        if charts:
            assert "chart" in html.lower()

    def test_render_string(self, sample_data_and_charts: tuple) -> None:
        """Test rendering from template string."""
        data, charts = sample_data_and_charts
        renderer = HTMLRenderer()

        template_string = "<html><body>Score: {{ summary.overall_score }}</body></html>"
        html = renderer.render_string(template_string, data, charts)

        assert isinstance(html, str)
        assert "<html>" in html
        assert "Score:" in html

    def test_save(self, sample_data_and_charts: tuple, tmp_path: Path) -> None:
        """Test saving HTML to file."""
        data, charts = sample_data_and_charts
        renderer = HTMLRenderer()

        html = renderer.render(data, charts)
        output_path = tmp_path / "test_report.html"

        renderer.save(html, output_path)

        assert output_path.exists()
        assert output_path.stat().st_size > 0

        # Verify content
        saved_html = output_path.read_text(encoding="utf-8")
        assert saved_html == html

    def test_save_creates_parent_directories(
        self, sample_data_and_charts: tuple, tmp_path: Path
    ) -> None:
        """Test that save creates parent directories if needed."""
        data, charts = sample_data_and_charts
        renderer = HTMLRenderer()

        html = renderer.render(data, charts)
        output_path = tmp_path / "subdir" / "nested" / "report.html"

        renderer.save(html, output_path)

        assert output_path.exists()
        assert output_path.parent.exists()

    def test_render_and_save(
        self, sample_data_and_charts: tuple, tmp_path: Path
    ) -> None:
        """Test rendering and saving in one step."""
        data, charts = sample_data_and_charts
        renderer = HTMLRenderer()

        output_path = tmp_path / "combined_report.html"
        html = renderer.render_and_save(data, charts, output_path)

        assert isinstance(html, str)
        assert len(html) > 0
        assert output_path.exists()

        # Verify saved content matches returned HTML
        saved_html = output_path.read_text(encoding="utf-8")
        assert saved_html == html

    def test_get_available_templates(self) -> None:
        """Test getting list of available templates."""
        renderer = HTMLRenderer()

        templates = renderer.get_available_templates()

        assert isinstance(templates, list)
        assert len(templates) > 0
        assert "fairness_report.html" in templates

    def test_render_with_empty_data(self) -> None:
        """Test rendering with minimal/empty data."""
        renderer = HTMLRenderer()

        minimal_data = {
            "summary": {"overall_score": 0.0, "n_violations": 0, "passes_fairness": False},
            "issues": [],
            "recommendations": [],
        }
        empty_charts = {}

        # Should not crash
        html = renderer.render(minimal_data, empty_charts)

        assert isinstance(html, str)
        assert len(html) > 0
        assert "<html" in html.lower()

    def test_render_with_issues(self) -> None:
        """Test rendering with issues."""
        renderer = HTMLRenderer()

        data = {
            "summary": {"overall_score": 50.0, "n_violations": 2, "passes_fairness": False},
            "issues": [
                {
                    "severity": "critical",
                    "metric": "Statistical Parity",
                    "message": "Test issue",
                    "impact": "Test impact",
                }
            ],
            "recommendations": [],
        }
        charts = {}

        html = renderer.render(data, charts)

        assert "Statistical Parity" in html
        assert "Test issue" in html

    def test_render_with_recommendations(self) -> None:
        """Test rendering with recommendations."""
        renderer = HTMLRenderer()

        data = {
            "summary": {"overall_score": 50.0, "n_violations": 0, "passes_fairness": False},
            "issues": [],
            "recommendations": [
                {
                    "priority": "high",
                    "action": "Test action",
                    "description": "Test description",
                }
            ],
        }
        charts = {}

        html = renderer.render(data, charts)

        assert "Test action" in html
        assert "Test description" in html

    def test_format_filter(self) -> None:
        """Test custom format filter."""
        renderer = HTMLRenderer()

        # Test with % format spec
        result = renderer._format_filter("%.2f", 3.14159)
        assert result == "3.14"

        # Test with Python format spec
        result = renderer._format_filter(".2f", 3.14159)
        assert result == "3.14"

        # Test without format spec
        result = renderer._format_filter("", 42)
        assert result == "42"

    def test_render_includes_timestamp(self, sample_data_and_charts: tuple) -> None:
        """Test that rendered HTML includes timestamp."""
        data, charts = sample_data_and_charts
        renderer = HTMLRenderer()

        html = renderer.render(data, charts)

        # Should include a timestamp (year pattern)
        assert "202" in html  # Matches 2020s

    def test_charts_json_in_context(self, sample_data_and_charts: tuple) -> None:
        """Test that charts are properly JSON-encoded in context."""
        data, charts = sample_data_and_charts
        renderer = HTMLRenderer()

        html = renderer.render(data, charts)

        # Should include JSON-encoded charts
        if charts:
            # At least one chart name should appear
            for chart_name in charts.keys():
                # The chart name might appear in the HTML
                assert chart_name in html or "chart" in html.lower()
