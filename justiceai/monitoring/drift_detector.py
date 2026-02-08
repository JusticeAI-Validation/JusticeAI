"""
Fairness Drift Detection.

This module provides drift detection for fairness metrics over time,
helping identify when model fairness characteristics change in production.

Drift detection methods:
- Statistical tests (Kolmogorov-Smirnov, Chi-square)
- PSI (Population Stability Index)
- Threshold-based alerts
"""

from dataclasses import dataclass
from typing import Any

import numpy as np
from scipy import stats


@dataclass
class DriftResult:
    """
    Result of drift detection analysis.

    Attributes:
        has_drift: Whether drift was detected
        drifted_metrics: Dictionary of metrics that drifted with their scores
        drift_scores: Dictionary of all drift scores calculated
        method: Detection method used
        threshold: Threshold used for detection
        details: Additional details about the drift
    """

    has_drift: bool
    drifted_metrics: dict[str, float]
    drift_scores: dict[str, float]
    method: str
    threshold: float
    details: dict[str, Any]


class FairnessDriftDetector:
    """
    Detector for fairness metric drift.

    This detector compares baseline fairness metrics with new metrics
    to identify significant changes that may indicate model degradation
    or changing data distributions.

    Supported detection methods:
        - 'psi': Population Stability Index
        - 'ks': Kolmogorov-Smirnov test
        - 'threshold': Simple threshold-based comparison

    Example:
        >>> from justiceai.monitoring import FairnessDriftDetector
        >>>
        >>> # Baseline metrics from training/validation
        >>> baseline_metrics = {
        ...     'statistical_parity': 0.95,
        ...     'equal_opportunity': 0.92,
        ...     'predictive_parity': 0.88
        ... }
        >>>
        >>> # Create detector
        >>> detector = FairnessDriftDetector(baseline_metrics, method='threshold')
        >>>
        >>> # New metrics from production
        >>> new_metrics = {
        ...     'statistical_parity': 0.75,  # Drifted!
        ...     'equal_opportunity': 0.91,
        ...     'predictive_parity': 0.87
        ... }
        >>>
        >>> # Detect drift
        >>> result = detector.detect(new_metrics)
        >>> if result.has_drift:
        ...     print(f"Drift detected in: {list(result.drifted_metrics.keys())}")
        Drift detected in: ['statistical_parity']
    """

    def __init__(
        self,
        baseline_metrics: dict[str, float],
        method: str = "threshold",
        threshold: float = 0.1,
        significance_level: float = 0.05,
    ):
        """
        Initialize Fairness Drift Detector.

        Args:
            baseline_metrics: Dictionary of baseline fairness metrics
            method: Detection method ('threshold', 'psi', 'ks')
            threshold: Threshold for drift detection (default: 0.1)
            significance_level: Significance level for statistical tests (default: 0.05)

        Raises:
            ValueError: If method is not supported
        """
        self.baseline_metrics = baseline_metrics
        self.method = method
        self.threshold = threshold
        self.significance_level = significance_level

        if method not in ["threshold", "psi", "ks"]:
            raise ValueError(
                f"Unsupported method: {method}. "
                f"Supported methods: 'threshold', 'psi', 'ks'"
            )

    def detect(self, new_metrics: dict[str, float]) -> DriftResult:
        """
        Detect drift in fairness metrics.

        Args:
            new_metrics: Dictionary of new fairness metrics to compare

        Returns:
            DriftResult with detection results

        Example:
            >>> result = detector.detect(new_metrics)
            >>> print(f"Drift detected: {result.has_drift}")
            >>> print(f"Drifted metrics: {result.drifted_metrics}")
        """
        if self.method == "threshold":
            return self._detect_threshold(new_metrics)
        elif self.method == "psi":
            return self._detect_psi(new_metrics)
        elif self.method == "ks":
            return self._detect_ks(new_metrics)
        else:
            raise ValueError(f"Unknown method: {self.method}")

    def _detect_threshold(self, new_metrics: dict[str, float]) -> DriftResult:
        """Detect drift using simple threshold comparison."""
        drift_scores = {}
        drifted_metrics = {}

        for metric_name, baseline_value in self.baseline_metrics.items():
            if metric_name in new_metrics:
                new_value = new_metrics[metric_name]
                # Calculate absolute difference
                diff = abs(new_value - baseline_value)
                drift_scores[metric_name] = diff

                # Check if drift exceeds threshold
                if diff > self.threshold:
                    drifted_metrics[metric_name] = diff

        has_drift = len(drifted_metrics) > 0

        return DriftResult(
            has_drift=has_drift,
            drifted_metrics=drifted_metrics,
            drift_scores=drift_scores,
            method="threshold",
            threshold=self.threshold,
            details={
                "baseline_metrics": self.baseline_metrics,
                "new_metrics": new_metrics,
                "num_drifted": len(drifted_metrics),
            },
        )

    def _detect_psi(self, new_metrics: dict[str, float]) -> DriftResult:
        """
        Detect drift using Population Stability Index (PSI).

        PSI is calculated as: sum((new - baseline) * ln(new / baseline))
        PSI < 0.1: No significant change
        PSI 0.1-0.25: Small change
        PSI > 0.25: Significant change (drift)
        """
        drift_scores = {}
        drifted_metrics = {}

        for metric_name, baseline_value in self.baseline_metrics.items():
            if metric_name in new_metrics:
                new_value = new_metrics[metric_name]

                # Avoid log(0) by adding small epsilon
                epsilon = 1e-10
                baseline_adj = max(baseline_value, epsilon)
                new_adj = max(new_value, epsilon)

                # Calculate PSI
                psi = (new_adj - baseline_adj) * np.log(new_adj / baseline_adj)
                drift_scores[metric_name] = abs(psi)

                # Check if PSI exceeds threshold (default 0.1 maps to 0.25 for PSI)
                psi_threshold = self.threshold * 2.5  # Convert to PSI scale
                if abs(psi) > psi_threshold:
                    drifted_metrics[metric_name] = abs(psi)

        has_drift = len(drifted_metrics) > 0

        return DriftResult(
            has_drift=has_drift,
            drifted_metrics=drifted_metrics,
            drift_scores=drift_scores,
            method="psi",
            threshold=self.threshold,
            details={
                "baseline_metrics": self.baseline_metrics,
                "new_metrics": new_metrics,
                "num_drifted": len(drifted_metrics),
                "psi_threshold": self.threshold * 2.5,
            },
        )

    def _detect_ks(self, new_metrics: dict[str, float]) -> DriftResult:
        """
        Detect drift using Kolmogorov-Smirnov test.

        Note: This is a simplified version that uses the difference
        between metric values as a proxy for distribution difference.
        For full KS test, you would need distribution data.
        """
        drift_scores = {}
        drifted_metrics = {}

        for metric_name, baseline_value in self.baseline_metrics.items():
            if metric_name in new_metrics:
                new_value = new_metrics[metric_name]

                # Calculate KS-like statistic (simplified)
                # In full implementation, this would be KS test on distributions
                ks_stat = abs(new_value - baseline_value)
                drift_scores[metric_name] = ks_stat

                # Use threshold for detection
                if ks_stat > self.threshold:
                    drifted_metrics[metric_name] = ks_stat

        has_drift = len(drifted_metrics) > 0

        return DriftResult(
            has_drift=has_drift,
            drifted_metrics=drifted_metrics,
            drift_scores=drift_scores,
            method="ks",
            threshold=self.threshold,
            details={
                "baseline_metrics": self.baseline_metrics,
                "new_metrics": new_metrics,
                "num_drifted": len(drifted_metrics),
                "note": "Simplified KS test - for full test, provide distribution data",
            },
        )

    def update_baseline(self, new_baseline: dict[str, float]) -> None:
        """
        Update baseline metrics.

        Use this when you want to establish a new baseline
        (e.g., after model retraining).

        Args:
            new_baseline: New baseline metrics dictionary

        Example:
            >>> detector.update_baseline(new_metrics)
        """
        self.baseline_metrics = new_baseline

    def get_drift_summary(self, result: DriftResult) -> dict[str, Any]:
        """
        Get human-readable drift summary.

        Args:
            result: DriftResult from detect() method

        Returns:
            Dictionary with summary information

        Example:
            >>> summary = detector.get_drift_summary(result)
            >>> print(summary['message'])
            'Drift detected in 1 metric(s)'
        """
        summary = {
            "drift_detected": result.has_drift,
            "method": result.method,
            "threshold": result.threshold,
            "num_metrics_checked": len(self.baseline_metrics),
            "num_drifted": len(result.drifted_metrics),
        }

        if result.has_drift:
            summary["message"] = (
                f"Drift detected in {len(result.drifted_metrics)} metric(s)"
            )
            summary["drifted_metrics"] = list(result.drifted_metrics.keys())
            summary["severity"] = self._assess_drift_severity(result)
        else:
            summary["message"] = "No drift detected"
            summary["severity"] = "none"

        return summary

    def _assess_drift_severity(self, result: DriftResult) -> str:
        """Assess drift severity based on number and magnitude of drifted metrics."""
        num_drifted = len(result.drifted_metrics)
        total_metrics = len(self.baseline_metrics)

        # Calculate average drift magnitude
        if num_drifted > 0:
            avg_drift = np.mean(list(result.drifted_metrics.values()))
        else:
            return "none"

        # Assess severity
        drift_ratio = num_drifted / total_metrics

        if drift_ratio >= 0.5 or avg_drift > self.threshold * 3:
            return "high"
        elif drift_ratio >= 0.25 or avg_drift > self.threshold * 2:
            return "medium"
        else:
            return "low"


class MetricsDriftMonitor:
    """
    Monitor for continuous drift detection across multiple time periods.

    This class maintains a history of metrics and detects drift trends.

    Example:
        >>> from justiceai.monitoring import MetricsDriftMonitor
        >>>
        >>> # Create monitor
        >>> monitor = MetricsDriftMonitor(baseline_metrics, window_size=5)
        >>>
        >>> # Add new observations over time
        >>> monitor.add_observation(metrics_t1, timestamp="2024-01-01")
        >>> monitor.add_observation(metrics_t2, timestamp="2024-01-02")
        >>> monitor.add_observation(metrics_t3, timestamp="2024-01-03")
        >>>
        >>> # Check drift
        >>> drift_report = monitor.check_drift()
        >>> print(drift_report['has_drift'])
    """

    def __init__(
        self,
        baseline_metrics: dict[str, float],
        window_size: int = 10,
        method: str = "threshold",
        threshold: float = 0.1,
    ):
        """
        Initialize Metrics Drift Monitor.

        Args:
            baseline_metrics: Baseline fairness metrics
            window_size: Number of recent observations to consider
            method: Drift detection method
            threshold: Threshold for drift detection
        """
        self.baseline_metrics = baseline_metrics
        self.window_size = window_size
        self.detector = FairnessDriftDetector(baseline_metrics, method, threshold)
        self.history: list[dict[str, Any]] = []

    def add_observation(
        self, metrics: dict[str, float], timestamp: str | None = None
    ) -> DriftResult:
        """
        Add new metrics observation and detect drift.

        Args:
            metrics: New metrics to add
            timestamp: Optional timestamp for the observation

        Returns:
            DriftResult for this observation
        """
        result = self.detector.detect(metrics)

        # Add to history
        self.history.append(
            {"timestamp": timestamp, "metrics": metrics, "drift_result": result}
        )

        # Keep only recent observations
        if len(self.history) > self.window_size:
            self.history = self.history[-self.window_size :]

        return result

    def check_drift(self) -> dict[str, Any]:
        """
        Check for drift across recent observations.

        Returns:
            Dictionary with drift analysis across time window
        """
        if not self.history:
            return {
                "has_drift": False,
                "message": "No observations yet",
                "num_observations": 0,
            }

        # Count how many recent observations show drift
        drift_count = sum(1 for obs in self.history if obs["drift_result"].has_drift)

        drift_ratio = drift_count / len(self.history)

        return {
            "has_drift": drift_ratio > 0.3,  # Alert if >30% of observations drift
            "drift_ratio": drift_ratio,
            "num_observations": len(self.history),
            "num_with_drift": drift_count,
            "message": f"Drift detected in {drift_count}/{len(self.history)} recent observations",
            "latest_result": self.history[-1]["drift_result"],
        }

    def get_drift_trend(self) -> dict[str, list[float]]:
        """
        Get trend of drift scores over time for each metric.

        Returns:
            Dictionary mapping metric names to lists of drift scores
        """
        trends: dict[str, list[float]] = {}

        for obs in self.history:
            for metric_name, score in obs["drift_result"].drift_scores.items():
                if metric_name not in trends:
                    trends[metric_name] = []
                trends[metric_name].append(score)

        return trends
