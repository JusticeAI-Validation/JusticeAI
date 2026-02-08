"""
Base chart class for Plotly visualizations.

This module provides the foundation for all fairness charts with
common styling, colors, and utilities.
"""

import json
from typing import Any

import numpy as np
import plotly.graph_objects as go
from plotly.utils import PlotlyJSONEncoder


# Color constants for status-based coloring
COLOR_SUCCESS = "#10b981"  # Green
COLOR_WARNING = "#f59e0b"  # Amber
COLOR_CRITICAL = "#ef4444"  # Red
COLOR_INFO = "#3b82f6"  # Blue
COLOR_NEUTRAL = "#6b7280"  # Gray

# Status to color mapping
COLOR_MAP_STATUS = {
    "success": COLOR_SUCCESS,
    "warning": COLOR_WARNING,
    "critical": COLOR_CRITICAL,
    "ok": COLOR_INFO,
    "info": COLOR_INFO,
}


class BaseChart:
    """
    Base class for all fairness charts.

    Provides common utilities for Plotly chart creation including:
    - Consistent color schemes
    - Layout styling
    - JSON serialization
    - Value formatting

    Example:
        >>> class MyChart(BaseChart):
        ...     def create(self, data: dict) -> str:
        ...         fig = go.Figure(...)
        ...         self._apply_common_layout(fig, title='My Chart')
        ...         return self._to_json(fig)
    """

    def __init__(self):
        """Initialize base chart with common configuration."""
        self.default_height = 400
        self.default_width = None  # Auto-width
        self.font_family = "Inter, system-ui, sans-serif"

    def create(self, data: dict[str, Any]) -> str:
        """
        Create chart from data.

        Args:
            data: Dictionary with chart data

        Returns:
            Plotly JSON string

        Raises:
            NotImplementedError: Must be implemented by subclasses
        """
        raise NotImplementedError("Subclasses must implement create()")

    def _apply_common_layout(
        self,
        fig: go.Figure,
        title: str = "",
        height: int | None = None,
        show_legend: bool = True,
    ) -> None:
        """
        Apply common layout styling to figure.

        Args:
            fig: Plotly figure
            title: Chart title
            height: Chart height in pixels
            show_legend: Whether to show legend
        """
        fig.update_layout(
            title={"text": title, "font": {"size": 18, "family": self.font_family}},
            height=height or self.default_height,
            template="plotly_white",
            font={"family": self.font_family},
            showlegend=show_legend,
            margin={"l": 50, "r": 50, "t": 80, "b": 50},
            plot_bgcolor="white",
            paper_bgcolor="white",
        )

    def _to_json(self, fig: go.Figure) -> str:
        """
        Convert Plotly figure to JSON string.

        Args:
            fig: Plotly figure

        Returns:
            JSON string representation
        """
        # Use PlotlyJSONEncoder to handle numpy arrays and other types
        return json.dumps(fig.to_dict(), cls=PlotlyJSONEncoder)

    def _get_color_for_status(self, status: str) -> str:
        """
        Get color for status.

        Args:
            status: Status string ('success', 'warning', 'critical', etc.)

        Returns:
            Hex color code
        """
        return COLOR_MAP_STATUS.get(status.lower(), COLOR_NEUTRAL)

    def _format_percentage(self, value: float) -> str:
        """
        Format value as percentage.

        Args:
            value: Value to format (0-1 range)

        Returns:
            Formatted percentage string
        """
        return f"{value * 100:.1f}%"

    def _format_decimal(self, value: float, decimals: int = 3) -> str:
        """
        Format decimal value.

        Args:
            value: Value to format
            decimals: Number of decimal places

        Returns:
            Formatted string
        """
        return f"{value:.{decimals}f}"

    def _safe_division(self, numerator: float, denominator: float) -> float:
        """
        Safely divide two numbers, returning 0 if denominator is 0.

        Args:
            numerator: Numerator
            denominator: Denominator

        Returns:
            Division result or 0 if denominator is 0
        """
        if denominator == 0 or np.isnan(denominator):
            return 0.0
        return numerator / denominator

    def _get_status_symbol(self, status: str) -> str:
        """
        Get symbol for status.

        Args:
            status: Status string

        Returns:
            Symbol (✓, ⚠, ✗)
        """
        status_symbols = {
            "success": "✓",
            "warning": "⚠",
            "critical": "✗",
            "ok": "✓",
        }
        return status_symbols.get(status.lower(), "●")
