"""
Fairness-specific charts for reports.

This module provides Plotly charts for visualizing fairness metrics:
- Disparate Impact Gauge
- Statistical Parity Comparison
- Confusion Matrix Heatmap
- Metrics Overview Bar Chart
"""

from typing import Any

import plotly.graph_objects as go
from plotly.subplots import make_subplots

from justiceai.reports.charts.base_chart import (
    COLOR_CRITICAL,
    COLOR_SUCCESS,
    COLOR_WARNING,
    BaseChart,
)


class DisparateImpactGauge(BaseChart):
    """
    Gauge chart showing disparate impact ratio vs 80% rule.

    The 80% rule (EEOC guideline) states that the selection rate for any group
    should be at least 80% of the selection rate for the highest group.
    """

    def create(self, data: dict[str, Any]) -> str:
        """
        Create disparate impact gauge chart.

        Args:
            data: Dictionary with 'posttrain_metrics' containing 'disparate_impact'

        Returns:
            Plotly JSON string
        """
        metrics = data.get("posttrain_metrics", {})
        di_data = metrics.get("disparate_impact", {})

        if not di_data:
            return "{}"

        ratio = di_data.get("ratio", 1.0)
        passes = di_data.get("passes_80_rule", True)

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number+delta",
                value=ratio,
                delta={"reference": 0.8, "increasing": {"color": COLOR_SUCCESS}},
                title={
                    "text": "Disparate Impact Ratio<br><span style='font-size:0.8em;color:gray'>80% Rule (EEOC)</span>"
                },
                gauge={
                    "axis": {"range": [0, 1.2], "tickwidth": 1},
                    "bar": {"color": COLOR_SUCCESS if passes else COLOR_CRITICAL},
                    "steps": [
                        {"range": [0, 0.7], "color": "rgba(239, 68, 68, 0.2)"},
                        {"range": [0.7, 0.8], "color": "rgba(245, 158, 11, 0.2)"},
                        {"range": [0.8, 1.2], "color": "rgba(16, 185, 129, 0.2)"},
                    ],
                    "threshold": {
                        "line": {"color": COLOR_WARNING, "width": 4},
                        "thickness": 0.75,
                        "value": 0.8,
                    },
                },
            )
        )

        self._apply_common_layout(fig, height=300, show_legend=False)
        return self._to_json(fig)


class StatisticalParityBar(BaseChart):
    """Bar chart comparing selection rates across groups."""

    def create(self, data: dict[str, Any]) -> str:
        """
        Create statistical parity comparison chart.

        Args:
            data: Dictionary with 'posttrain_metrics' containing 'statistical_parity'

        Returns:
            Plotly JSON string
        """
        metrics = data.get("posttrain_metrics", {})
        sp_data = metrics.get("statistical_parity", {})

        if not sp_data:
            return "{}"

        groups = sp_data.get("groups", {})
        if not groups:
            return "{}"

        group_names = list(groups.keys())
        selection_rates = [groups[g].get("selection_rate", 0.0) for g in group_names]

        # Get status for coloring
        status = sp_data.get("status", "ok")
        bar_color = self._get_color_for_status(status)

        fig = go.Figure(
            go.Bar(
                x=group_names,
                y=selection_rates,
                text=[self._format_percentage(sr) for sr in selection_rates],
                textposition="outside",
                marker={"color": bar_color},
                hovertemplate="<b>%{x}</b><br>Selection Rate: %{text}<extra></extra>",
            )
        )

        fig.update_yaxes(title="Selection Rate", tickformat=".0%", range=[0, 1.1])
        fig.update_xaxes(title="Group")

        self._apply_common_layout(
            fig,
            title="Statistical Parity: Selection Rates by Group",
            height=400,
            show_legend=False,
        )

        return self._to_json(fig)


class ConfusionMatrixHeatmap(BaseChart):
    """Heatmap showing confusion matrices for each group."""

    def create(self, data: dict[str, Any]) -> str:
        """
        Create confusion matrix heatmap.

        Args:
            data: Dictionary with 'posttrain_metrics' containing 'confusion_matrix'

        Returns:
            Plotly JSON string
        """
        metrics = data.get("posttrain_metrics", {})
        cm_data = metrics.get("confusion_matrix", {})

        if not cm_data:
            return "{}"

        groups_data = cm_data.get("groups", {})
        if not groups_data:
            return "{}"

        group_names = list(groups_data.keys())
        n_groups = len(group_names)

        # Create subplots for each group
        fig = make_subplots(
            rows=1,
            cols=n_groups,
            subplot_titles=[f"Group: {g}" for g in group_names],
            specs=[[{"type": "heatmap"} for _ in range(n_groups)]],
        )

        for i, group in enumerate(group_names, 1):
            group_cm = groups_data[group]

            # Create 2x2 confusion matrix
            cm_values = [
                [group_cm.get("TN", 0), group_cm.get("FP", 0)],
                [group_cm.get("FN", 0), group_cm.get("TP", 0)],
            ]

            # Create text annotations
            cm_text = [
                [
                    f"TN<br>{group_cm.get('TN', 0)}",
                    f"FP<br>{group_cm.get('FP', 0)}",
                ],
                [
                    f"FN<br>{group_cm.get('FN', 0)}",
                    f"TP<br>{group_cm.get('TP', 0)}",
                ],
            ]

            heatmap = go.Heatmap(
                z=cm_values,
                x=["Predicted Negative", "Predicted Positive"],
                y=["Actual Negative", "Actual Positive"],
                text=cm_text,
                texttemplate="%{text}",
                textfont={"size": 12},
                colorscale="Blues",
                showscale=(i == n_groups),  # Show scale only on last subplot
                hovertemplate="<b>%{x}</b><br><b>%{y}</b><br>Count: %{z}<extra></extra>",
            )

            fig.add_trace(heatmap, row=1, col=i)

        fig.update_yaxes(autorange="reversed")

        self._apply_common_layout(
            fig,
            title="Confusion Matrices by Group",
            height=400,
            show_legend=False,
        )

        return self._to_json(fig)


class MetricsOverviewBar(BaseChart):
    """Bar chart showing key fairness metrics with color-coded status."""

    def create(self, data: dict[str, Any]) -> str:
        """
        Create metrics overview bar chart.

        Args:
            data: Dictionary with 'posttrain_metrics'

        Returns:
            Plotly JSON string
        """
        metrics = data.get("posttrain_metrics", {})

        if not metrics:
            return "{}"

        # Collect key metrics with their values and status
        metric_data = []

        # Statistical parity difference
        if "statistical_parity" in metrics:
            sp = metrics["statistical_parity"]
            metric_data.append(
                {
                    "name": "Statistical Parity",
                    "value": abs(sp.get("difference", 0.0)),
                    "status": sp.get("status", "ok"),
                }
            )

        # Equal opportunity difference
        if "equal_opportunity" in metrics:
            eo = metrics["equal_opportunity"]
            metric_data.append(
                {
                    "name": "Equal Opportunity",
                    "value": abs(eo.get("difference", 0.0)),
                    "status": eo.get("status", "ok"),
                }
            )

        # Equalized odds (use max of TPR and FPR differences)
        if "equalized_odds" in metrics:
            eq = metrics["equalized_odds"]
            tpr_diff = abs(eq.get("tpr_difference", 0.0))
            fpr_diff = abs(eq.get("fpr_difference", 0.0))
            metric_data.append(
                {
                    "name": "Equalized Odds",
                    "value": max(tpr_diff, fpr_diff),
                    "status": eq.get("status", "ok"),
                }
            )

        # Accuracy difference
        if "accuracy_difference" in metrics:
            ad = metrics["accuracy_difference"]
            metric_data.append(
                {
                    "name": "Accuracy Diff",
                    "value": abs(ad.get("difference", 0.0)),
                    "status": ad.get("status", "ok"),
                }
            )

        if not metric_data:
            return "{}"

        # Extract data for plotting
        names = [m["name"] for m in metric_data]
        values = [m["value"] for m in metric_data]
        colors = [self._get_color_for_status(m["status"]) for m in metric_data]
        symbols = [self._get_status_symbol(m["status"]) for m in metric_data]

        fig = go.Figure(
            go.Bar(
                y=names,
                x=values,
                orientation="h",
                marker={"color": colors},
                text=[f"{v:.3f} {s}" for v, s in zip(values, symbols)],
                textposition="outside",
                hovertemplate="<b>%{y}</b><br>Difference: %{x:.4f}<extra></extra>",
            )
        )

        fig.update_xaxes(title="Absolute Difference", range=[0, max(values) * 1.2])
        fig.update_yaxes(title="")

        # Add reference line at 0.05 (typical threshold)
        fig.add_vline(
            x=0.05,
            line_dash="dash",
            line_color="gray",
            annotation_text="Threshold (0.05)",
            annotation_position="top right",
        )

        self._apply_common_layout(
            fig,
            title="Key Fairness Metrics Overview",
            height=300 + len(metric_data) * 40,
            show_legend=False,
        )

        return self._to_json(fig)


class OverallFairnessGauge(BaseChart):
    """Gauge showing overall fairness score (0-100)."""

    def create(self, data: dict[str, Any]) -> str:
        """
        Create overall fairness gauge.

        Args:
            data: Dictionary with 'summary' containing 'overall_score'

        Returns:
            Plotly JSON string
        """
        summary = data.get("summary", {})

        if not summary:
            return "{}"

        score = summary.get("overall_score", 0.0)
        passes = summary.get("passes_fairness", False)

        # Determine color based on score
        if score >= 75:
            color = COLOR_SUCCESS
        elif score >= 50:
            color = COLOR_WARNING
        else:
            color = COLOR_CRITICAL

        fig = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=score,
                title={"text": "Overall Fairness Score"},
                gauge={
                    "axis": {"range": [0, 100]},
                    "bar": {"color": color},
                    "steps": [
                        {"range": [0, 50], "color": "rgba(239, 68, 68, 0.2)"},
                        {"range": [50, 75], "color": "rgba(245, 158, 11, 0.2)"},
                        {"range": [75, 100], "color": "rgba(16, 185, 129, 0.2)"},
                    ],
                    "threshold": {
                        "line": {"color": "gray", "width": 4},
                        "thickness": 0.75,
                        "value": 75,
                    },
                },
                number={"suffix": "/100", "font": {"size": 40}},
            )
        )

        self._apply_common_layout(fig, height=300, show_legend=False)

        # Add annotation about pass/fail
        status_text = "✓ Passes basic fairness" if passes else "✗ Fails basic fairness"
        status_color = COLOR_SUCCESS if passes else COLOR_CRITICAL

        fig.add_annotation(
            text=status_text,
            xref="paper",
            yref="paper",
            x=0.5,
            y=0.1,
            showarrow=False,
            font={"size": 14, "color": status_color},
        )

        return self._to_json(fig)
