"""
HTML renderer for fairness reports.

This module provides functionality to render fairness reports as HTML
using Jinja2 templates.
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Any

from jinja2 import Environment, FileSystemLoader, Template


class HTMLRenderer:
    """
    Render fairness reports as HTML using Jinja2 templates.

    This class takes transformed data and charts, and renders them
    into a professional HTML report.

    Example:
        >>> from justiceai.reports.renderers.html_renderer import HTMLRenderer
        >>> renderer = HTMLRenderer()
        >>> html = renderer.render(data, charts)
        >>> renderer.save(html, 'report.html')
    """

    def __init__(self, template_path: str | None = None):
        """
        Initialize HTML renderer.

        Args:
            template_path: Path to custom template directory.
                          If None, uses default templates.
        """
        if template_path is None:
            # Use default template directory
            template_dir = Path(__file__).parent.parent / "templates"
        else:
            template_dir = Path(template_path)

        if not template_dir.exists():
            raise ValueError(f"Template directory not found: {template_dir}")

        self.env = Environment(
            loader=FileSystemLoader(str(template_dir)),
            autoescape=True,
            trim_blocks=True,
            lstrip_blocks=True,
        )

        # Add custom filters
        self.env.filters["format"] = self._format_filter

    def _format_filter(self, format_spec: str, value: Any) -> str:
        """
        Custom Jinja2 filter for formatting values.

        Note: In Jinja2, filter syntax is {{ format_spec|format(value) }}
        which translates to _format_filter(format_spec, value).

        Args:
            format_spec: Format specification (e.g., "%.2f")
            value: Value to format

        Returns:
            Formatted string
        """
        if format_spec and "%" in format_spec:
            # Python % formatting
            return format_spec % value
        elif format_spec:
            # Python format() function
            return format(value, format_spec)
        return str(value)

    def render(
        self,
        data: dict[str, Any],
        charts: dict[str, str],
        template_name: str = "fairness_report.html",
    ) -> str:
        """
        Render HTML report from data and charts.

        Args:
            data: Transformed data from FairnessDataTransformer
            charts: Dictionary of chart name -> Plotly JSON string
            template_name: Name of template file to use

        Returns:
            Rendered HTML string

        Example:
            >>> renderer = HTMLRenderer()
            >>> html = renderer.render(transformed_data, charts)
        """
        template = self.env.get_template(template_name)

        # Prepare context for template
        context = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": data.get("summary", {}),
            "pretrain_metrics": data.get("pretrain_metrics", {}),
            "posttrain_metrics": data.get("posttrain_metrics", {}),
            "issues": data.get("issues", []),
            "recommendations": data.get("recommendations", []),
            "charts": charts,
            "charts_json": json.dumps(charts),
        }

        return template.render(**context)

    def render_string(
        self, template_string: str, data: dict[str, Any], charts: dict[str, str]
    ) -> str:
        """
        Render HTML from a template string.

        Args:
            template_string: Jinja2 template as string
            data: Transformed data
            charts: Dictionary of charts

        Returns:
            Rendered HTML string
        """
        template = self.env.from_string(template_string)

        context = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "summary": data.get("summary", {}),
            "pretrain_metrics": data.get("pretrain_metrics", {}),
            "posttrain_metrics": data.get("posttrain_metrics", {}),
            "issues": data.get("issues", []),
            "recommendations": data.get("recommendations", []),
            "charts": charts,
            "charts_json": json.dumps(charts),
        }

        return template.render(**context)

    def save(self, html: str, output_path: str | Path) -> None:
        """
        Save rendered HTML to file.

        Args:
            html: Rendered HTML string
            output_path: Path to save HTML file

        Example:
            >>> renderer = HTMLRenderer()
            >>> html = renderer.render(data, charts)
            >>> renderer.save(html, 'fairness_report.html')
        """
        output_path = Path(output_path)

        # Create parent directory if it doesn't exist
        output_path.parent.mkdir(parents=True, exist_ok=True)

        # Write HTML to file
        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html)

    def render_and_save(
        self,
        data: dict[str, Any],
        charts: dict[str, str],
        output_path: str | Path,
        template_name: str = "fairness_report.html",
    ) -> str:
        """
        Render and save HTML report in one step.

        Args:
            data: Transformed data
            charts: Dictionary of charts
            output_path: Path to save HTML file
            template_name: Template file name

        Returns:
            Rendered HTML string (also saved to file)

        Example:
            >>> renderer = HTMLRenderer()
            >>> html = renderer.render_and_save(data, charts, 'report.html')
        """
        html = self.render(data, charts, template_name)
        self.save(html, output_path)
        return html

    def get_available_templates(self) -> list[str]:
        """
        Get list of available template files.

        Returns:
            List of template file names
        """
        template_dir = Path(self.env.loader.searchpath[0])
        return [
            f.name for f in template_dir.glob("*.html") if f.is_file()
        ]
