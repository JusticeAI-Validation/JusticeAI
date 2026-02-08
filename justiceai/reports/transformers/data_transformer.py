"""
Data transformer for fairness metrics reports.

This module transforms raw fairness metrics into a structured format
suitable for visualization and HTML report generation.
"""

from typing import Any

import numpy as np


def get_status_from_value(
    metric_name: str, value: float, threshold: float = 0.05
) -> str:
    """
    Determine status from metric value.

    Args:
        metric_name: Name of the metric
        value: Metric value
        threshold: Threshold for determining status

    Returns:
        Status string: 'success', 'warning', or 'critical'
    """
    # For ratio metrics (disparate_impact), higher is better
    if "ratio" in metric_name.lower():
        if value >= 0.8:
            return "success"
        elif value >= 0.7:
            return "warning"
        else:
            return "critical"

    # For difference metrics, closer to 0 is better
    if "diff" in metric_name.lower() or "difference" in metric_name.lower():
        abs_value = abs(value)
        if abs_value <= threshold:
            return "success"
        elif abs_value <= threshold * 2:
            return "warning"
        else:
            return "critical"

    # Default: treat as difference metric
    abs_value = abs(value)
    if abs_value <= threshold:
        return "success"
    elif abs_value <= threshold * 2:
        return "warning"
    else:
        return "critical"


def format_metric_value(value: Any) -> str:
    """
    Format metric value for display.

    Args:
        value: Value to format

    Returns:
        Formatted string
    """
    # Check bool first (before int, since bool is subclass of int in Python)
    if isinstance(value, bool):
        return "✓ Pass" if value else "✗ Fail"
    elif isinstance(value, (int, np.integer)):
        return str(value)
    elif isinstance(value, (float, np.floating)):
        if abs(value) < 0.01:
            return f"{value:.4f}"
        else:
            return f"{value:.3f}"
    else:
        return str(value)


class FairnessDataTransformer:
    """
    Transform fairness metrics into report-ready format.

    This class takes raw metrics from FairnessCalculator and transforms
    them into a structured format suitable for charts and HTML reports.

    Example:
        >>> from justiceai.core.metrics.calculator import FairnessCalculator
        >>> calculator = FairnessCalculator()
        >>> metrics = calculator.calculate_all(y_true, y_pred, sensitive_attr, X)
        >>>
        >>> transformer = FairnessDataTransformer()
        >>> report_data = transformer.transform(metrics)
        >>> print(report_data.keys())
    """

    def __init__(self, fairness_threshold: float = 0.05):
        """
        Initialize transformer.

        Args:
            fairness_threshold: Threshold for fairness metrics (default: 0.05)
        """
        self.fairness_threshold = fairness_threshold

    def transform(self, metrics: dict[str, Any]) -> dict[str, Any]:
        """
        Transform raw metrics into report format.

        Args:
            metrics: Dictionary with 'pretrain', 'posttrain', and 'summary' keys

        Returns:
            Structured dictionary for report generation with:
            - summary: Overall fairness information
            - pretrain_metrics: Pre-training metrics (if available)
            - posttrain_metrics: Post-training metrics
            - issues: List of detected issues
            - recommendations: List of recommendations
        """
        pretrain = metrics.get("pretrain", {})
        posttrain = metrics.get("posttrain", {})
        summary = metrics.get("summary", {})

        transformed = {
            "summary": self._transform_summary(summary),
            "posttrain_metrics": self._transform_posttrain(posttrain),
            "issues": self._extract_issues(summary, posttrain),
            "recommendations": self._extract_recommendations(summary),
        }

        # Add pretrain metrics if available
        if pretrain:
            transformed["pretrain_metrics"] = self._transform_pretrain(pretrain)

        return transformed

    def _transform_summary(self, summary: dict[str, Any]) -> dict[str, Any]:
        """Transform summary section."""
        return {
            "overall_score": summary.get("overall_fairness_score", 0.0),
            "n_violations": summary.get("n_violations", 0),
            "passes_fairness": summary.get("passes_basic_fairness", False),
            "violations": summary.get("fairness_violations", []),
            "disparate_impact_ratio": summary.get("disparate_impact_ratio", 1.0),
            "statistical_parity_diff": summary.get("statistical_parity_diff", 0.0),
            "status": "success"
            if summary.get("passes_basic_fairness", False)
            else "critical",
        }

    def _transform_pretrain(self, pretrain: dict[str, Any]) -> dict[str, Any]:
        """Transform pre-training metrics."""
        transformed = {}

        # Class balance
        if "class_balance" in pretrain:
            cb = pretrain["class_balance"]
            transformed["class_balance"] = {
                "groups": cb,
                "status": "ok",
            }

        # Concept balance
        if "concept_balance" in pretrain:
            cb_value = pretrain["concept_balance"]
            # Handle both dict and numeric values
            if isinstance(cb_value, dict):
                transformed["concept_balance"] = {
                    "value": cb_value,
                    "status": "ok",
                }
            else:
                transformed["concept_balance"] = {
                    "value": cb_value,
                    "status": get_status_from_value(
                        "concept_balance",
                        float(cb_value),
                        self.fairness_threshold,
                    ),
                }

        # Group distribution difference
        if "group_distribution_difference" in pretrain:
            gdd = pretrain["group_distribution_difference"]
            transformed["group_distribution"] = {
                "max_difference": gdd.get("max_difference", 0.0),
                "groups": gdd.get("by_group", {}),
                "status": get_status_from_value(
                    "difference",
                    gdd.get("max_difference", 0.0),
                    self.fairness_threshold,
                ),
            }

        return transformed

    def _transform_posttrain(self, posttrain: dict[str, Any]) -> dict[str, Any]:
        """Transform post-training metrics."""
        transformed = {}

        # Statistical parity
        if "statistical_parity" in posttrain:
            sp = posttrain["statistical_parity"]
            transformed["statistical_parity"] = {
                "difference": sp.get("difference", 0.0),
                "ratio": sp.get("ratio", 1.0),
                "is_fair": sp.get("is_fair", True),
                "groups": sp.get("by_group", {}),
                "status": "success" if sp.get("is_fair", True) else "critical",
            }

        # Disparate impact
        if "disparate_impact" in posttrain:
            di = posttrain["disparate_impact"]
            transformed["disparate_impact"] = {
                "ratio": di.get("ratio", 1.0),
                "passes_80_rule": di.get("passes_80_rule", True),
                "advantaged_group": di.get("advantaged_group", ""),
                "disadvantaged_group": di.get("disadvantaged_group", ""),
                "groups": di.get("by_group", {}),
                "status": "success" if di.get("passes_80_rule", True) else "critical",
            }

        # Equal opportunity
        if "equal_opportunity" in posttrain:
            eo = posttrain["equal_opportunity"]
            transformed["equal_opportunity"] = {
                "difference": eo.get("difference", 0.0),
                "is_fair": eo.get("is_fair", True),
                "groups": eo.get("by_group", {}),
                "status": "success" if eo.get("is_fair", True) else "warning",
            }

        # Equalized odds
        if "equalized_odds" in posttrain:
            eq = posttrain["equalized_odds"]
            transformed["equalized_odds"] = {
                "tpr_difference": eq.get("tpr_difference", 0.0),
                "fpr_difference": eq.get("fpr_difference", 0.0),
                "is_fair": eq.get("is_fair", True),
                "groups": eq.get("by_group", {}),
                "status": "success" if eq.get("is_fair", True) else "warning",
            }

        # Confusion matrix
        if "confusion_matrix" in posttrain:
            transformed["confusion_matrix"] = {
                "groups": posttrain["confusion_matrix"],
                "status": "ok",
            }

        # False negative rate difference
        if "false_negative_rate_diff" in posttrain:
            fnr = posttrain["false_negative_rate_diff"]
            transformed["false_negative_rate_diff"] = {
                "difference": fnr.get("difference", 0.0),
                "groups": fnr.get("by_group", {}),
                "status": get_status_from_value(
                    "difference",
                    fnr.get("difference", 0.0),
                    self.fairness_threshold,
                ),
            }

        # Predictive parity
        if "predictive_parity" in posttrain:
            pp = posttrain["predictive_parity"]
            transformed["predictive_parity"] = {
                "difference": pp.get("difference", 0.0),
                "is_fair": pp.get("is_fair", True),
                "groups": pp.get("by_group", {}),
                "status": "success" if pp.get("is_fair", True) else "warning",
            }

        # Negative predictive parity
        if "negative_predictive_parity" in posttrain:
            npp = posttrain["negative_predictive_parity"]
            transformed["negative_predictive_parity"] = {
                "difference": npp.get("difference", 0.0),
                "is_fair": npp.get("is_fair", True),
                "groups": npp.get("by_group", {}),
                "status": "success" if npp.get("is_fair", True) else "warning",
            }

        # Accuracy difference
        if "accuracy_difference" in posttrain:
            ad = posttrain["accuracy_difference"]
            transformed["accuracy_difference"] = {
                "difference": ad.get("difference", 0.0),
                "is_fair": ad.get("is_fair", True),
                "groups": ad.get("by_group", {}),
                "status": "success" if ad.get("is_fair", True) else "warning",
            }

        # Treatment equality
        if "treatment_equality" in posttrain:
            te = posttrain["treatment_equality"]
            transformed["treatment_equality"] = {
                "difference": te.get("difference", 0.0),
                "groups": te.get("by_group", {}),
                "status": get_status_from_value(
                    "difference",
                    te.get("difference", 0.0),
                    self.fairness_threshold,
                ),
            }

        # Calibration
        if "calibration" in posttrain:
            cal = posttrain["calibration"]
            transformed["calibration"] = {
                "ece_difference": cal.get("ece_difference", 0.0),
                "groups": cal.get("by_group", {}),
                "status": get_status_from_value(
                    "difference", cal.get("ece_difference", 0.0), 0.1
                ),
            }

        return transformed

    def _extract_issues(
        self, summary: dict[str, Any], posttrain: dict[str, Any]
    ) -> list[dict[str, Any]]:
        """Extract critical issues and warnings."""
        issues = []

        violations = summary.get("fairness_violations", [])

        for violation in violations:
            if violation == "statistical_parity":
                issues.append(
                    {
                        "severity": "critical",
                        "metric": "Statistical Parity",
                        "message": "Different selection rates across groups",
                        "impact": "May violate equal treatment requirements",
                    }
                )
            elif violation == "disparate_impact":
                di_ratio = summary.get("disparate_impact_ratio", 1.0)
                issues.append(
                    {
                        "severity": "critical",
                        "metric": "Disparate Impact",
                        "message": f"Ratio {di_ratio:.2f} fails 80% rule",
                        "impact": "May violate EEOC guidelines",
                    }
                )
            elif violation == "equal_opportunity":
                issues.append(
                    {
                        "severity": "warning",
                        "metric": "Equal Opportunity",
                        "message": "Unequal true positive rates across groups",
                        "impact": "Qualified individuals treated differently",
                    }
                )
            elif violation == "equalized_odds":
                issues.append(
                    {
                        "severity": "warning",
                        "metric": "Equalized Odds",
                        "message": "Both TPR and FPR differ across groups",
                        "impact": "Inconsistent error rates",
                    }
                )

        return issues

    def _extract_recommendations(
        self, summary: dict[str, Any]
    ) -> list[dict[str, str]]:
        """Extract recommendations based on violations."""
        recommendations = []

        violations = summary.get("fairness_violations", [])

        if not violations:
            recommendations.append(
                {
                    "priority": "info",
                    "action": "Maintain current practices",
                    "description": "Model passes basic fairness checks. "
                    "Continue monitoring for drift.",
                }
            )
            return recommendations

        if "statistical_parity" in violations:
            recommendations.append(
                {
                    "priority": "high",
                    "action": "Apply threshold optimization",
                    "description": "Use different decision thresholds per group to "
                    "balance selection rates. See ThresholdAnalyzer.",
                }
            )

        if "disparate_impact" in violations:
            recommendations.append(
                {
                    "priority": "high",
                    "action": "Review feature selection",
                    "description": "Examine features that may correlate with protected "
                    "attributes. Consider reweighing or removing biased features.",
                }
            )

        if "equal_opportunity" in violations or "equalized_odds" in violations:
            recommendations.append(
                {
                    "priority": "medium",
                    "action": "Apply post-processing correction",
                    "description": "Use equalized odds post-processing to adjust "
                    "predictions and balance TPR/FPR across groups.",
                }
            )

        # Always add monitoring recommendation
        recommendations.append(
            {
                "priority": "medium",
                "action": "Implement continuous monitoring",
                "description": "Track fairness metrics over time to detect drift. "
                "Set up alerts for threshold violations.",
            }
        )

        return recommendations
