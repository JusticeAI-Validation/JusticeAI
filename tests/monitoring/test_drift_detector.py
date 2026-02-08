"""Tests for drift detection module."""

import pytest

from justiceai.monitoring import DriftResult, FairnessDriftDetector, MetricsDriftMonitor


class TestFairnessDriftDetector:
    """Tests for FairnessDriftDetector class."""

    @pytest.fixture
    def baseline_metrics(self) -> dict[str, float]:
        """Create baseline metrics."""
        return {
            "statistical_parity": 0.95,
            "equal_opportunity": 0.92,
            "predictive_parity": 0.88,
        }

    def test_initialization(self, baseline_metrics: dict[str, float]):
        """Test detector initialization."""
        detector = FairnessDriftDetector(baseline_metrics)

        assert detector.baseline_metrics == baseline_metrics
        assert detector.method == "threshold"
        assert detector.threshold == 0.1

    def test_initialization_custom_params(self, baseline_metrics: dict[str, float]):
        """Test detector initialization with custom parameters."""
        detector = FairnessDriftDetector(
            baseline_metrics, method="psi", threshold=0.15
        )

        assert detector.method == "psi"
        assert detector.threshold == 0.15

    def test_initialization_invalid_method(self, baseline_metrics: dict[str, float]):
        """Test that invalid method raises error."""
        with pytest.raises(ValueError, match="Unsupported method"):
            FairnessDriftDetector(baseline_metrics, method="invalid")

    def test_detect_no_drift(self, baseline_metrics: dict[str, float]):
        """Test drift detection when no drift present."""
        detector = FairnessDriftDetector(baseline_metrics, threshold=0.1)

        # New metrics very similar to baseline
        new_metrics = {
            "statistical_parity": 0.94,  # 0.01 diff
            "equal_opportunity": 0.93,  # 0.01 diff
            "predictive_parity": 0.87,  # 0.01 diff
        }

        result = detector.detect(new_metrics)

        assert isinstance(result, DriftResult)
        assert result.has_drift is False
        assert len(result.drifted_metrics) == 0

    def test_detect_with_drift(self, baseline_metrics: dict[str, float]):
        """Test drift detection when drift present."""
        detector = FairnessDriftDetector(baseline_metrics, threshold=0.1)

        # New metrics with significant drift
        new_metrics = {
            "statistical_parity": 0.75,  # 0.20 diff - DRIFT!
            "equal_opportunity": 0.91,  # 0.01 diff
            "predictive_parity": 0.87,  # 0.01 diff
        }

        result = detector.detect(new_metrics)

        assert result.has_drift is True
        assert "statistical_parity" in result.drifted_metrics
        assert "equal_opportunity" not in result.drifted_metrics

    def test_detect_multiple_drifts(self, baseline_metrics: dict[str, float]):
        """Test detection of multiple drifted metrics."""
        detector = FairnessDriftDetector(baseline_metrics, threshold=0.1)

        # Multiple metrics with drift
        new_metrics = {
            "statistical_parity": 0.70,  # 0.25 diff - DRIFT!
            "equal_opportunity": 0.75,  # 0.17 diff - DRIFT!
            "predictive_parity": 0.87,  # 0.01 diff
        }

        result = detector.detect(new_metrics)

        assert result.has_drift is True
        assert len(result.drifted_metrics) == 2
        assert "statistical_parity" in result.drifted_metrics
        assert "equal_opportunity" in result.drifted_metrics

    def test_update_baseline(self, baseline_metrics: dict[str, float]):
        """Test updating baseline metrics."""
        detector = FairnessDriftDetector(baseline_metrics)

        new_baseline = {
            "statistical_parity": 0.90,
            "equal_opportunity": 0.85,
            "predictive_parity": 0.80,
        }

        detector.update_baseline(new_baseline)

        assert detector.baseline_metrics == new_baseline

    def test_get_drift_summary(self, baseline_metrics: dict[str, float]):
        """Test getting drift summary."""
        detector = FairnessDriftDetector(baseline_metrics)

        new_metrics = {
            "statistical_parity": 0.70,
            "equal_opportunity": 0.91,
            "predictive_parity": 0.87,
        }

        result = detector.detect(new_metrics)
        summary = detector.get_drift_summary(result)

        assert "drift_detected" in summary
        assert summary["drift_detected"] is True
        assert "severity" in summary
        assert "message" in summary

    def test_detect_psi_method(self, baseline_metrics: dict[str, float]):
        """Test drift detection using PSI method."""
        detector = FairnessDriftDetector(baseline_metrics, method="psi", threshold=0.1)

        # New metrics with moderate change
        new_metrics = {
            "statistical_parity": 0.75,
            "equal_opportunity": 0.92,
            "predictive_parity": 0.88,
        }

        result = detector.detect(new_metrics)

        assert result.method == "psi"
        assert isinstance(result, DriftResult)
        # PSI should detect drift for large changes
        assert "drift_scores" in result.__dict__

    def test_detect_psi_with_drift(self, baseline_metrics: dict[str, float]):
        """Test PSI drift detection with significant change."""
        detector = FairnessDriftDetector(baseline_metrics, method="psi", threshold=0.05)

        # Significant change in metrics
        new_metrics = {
            "statistical_parity": 0.50,  # Large change
            "equal_opportunity": 0.92,
            "predictive_parity": 0.88,
        }

        result = detector.detect(new_metrics)

        assert result.has_drift is True
        assert len(result.drifted_metrics) > 0

    def test_detect_ks_method(self, baseline_metrics: dict[str, float]):
        """Test drift detection using KS method."""
        detector = FairnessDriftDetector(baseline_metrics, method="ks", threshold=0.1)

        new_metrics = {
            "statistical_parity": 0.75,
            "equal_opportunity": 0.92,
            "predictive_parity": 0.88,
        }

        result = detector.detect(new_metrics)

        assert result.method == "ks"
        assert isinstance(result, DriftResult)

    def test_detect_ks_with_drift(self, baseline_metrics: dict[str, float]):
        """Test KS drift detection with significant change."""
        detector = FairnessDriftDetector(baseline_metrics, method="ks", threshold=0.1)

        # Large change
        new_metrics = {
            "statistical_parity": 0.50,
            "equal_opportunity": 0.50,
            "predictive_parity": 0.50,
        }

        result = detector.detect(new_metrics)

        assert result.has_drift is True
        assert len(result.drifted_metrics) > 0

    def test_drift_severity_high(self, baseline_metrics: dict[str, float]):
        """Test high severity drift classification."""
        detector = FairnessDriftDetector(baseline_metrics, threshold=0.1)

        # Very large drift
        new_metrics = {
            "statistical_parity": 0.50,
            "equal_opportunity": 0.50,
            "predictive_parity": 0.50,
        }

        result = detector.detect(new_metrics)
        summary = detector.get_drift_summary(result)

        assert summary["severity"] == "high"

    def test_drift_severity_medium(self, baseline_metrics: dict[str, float]):
        """Test medium severity drift classification."""
        detector = FairnessDriftDetector(baseline_metrics, threshold=0.1)

        # Moderate drift
        new_metrics = {
            "statistical_parity": 0.80,
            "equal_opportunity": 0.92,
            "predictive_parity": 0.88,
        }

        result = detector.detect(new_metrics)
        summary = detector.get_drift_summary(result)

        assert summary["severity"] in ["medium", "high"]

    def test_drift_severity_low(self, baseline_metrics: dict[str, float]):
        """Test low severity drift classification."""
        detector = FairnessDriftDetector(baseline_metrics, threshold=0.05)

        # Small drift
        new_metrics = {
            "statistical_parity": 0.89,
            "equal_opportunity": 0.92,
            "predictive_parity": 0.88,
        }

        result = detector.detect(new_metrics)
        summary = detector.get_drift_summary(result)

        assert summary["severity"] in ["low", "medium", "none"]


class TestMetricsDriftMonitor:
    """Tests for MetricsDriftMonitor class."""

    @pytest.fixture
    def baseline_metrics(self) -> dict[str, float]:
        """Create baseline metrics."""
        return {
            "statistical_parity": 0.95,
            "equal_opportunity": 0.92,
        }

    def test_initialization(self, baseline_metrics: dict[str, float]):
        """Test monitor initialization."""
        monitor = MetricsDriftMonitor(baseline_metrics, window_size=5)

        assert monitor.baseline_metrics == baseline_metrics
        assert monitor.window_size == 5
        assert len(monitor.history) == 0

    def test_add_observation(self, baseline_metrics: dict[str, float]):
        """Test adding observations."""
        monitor = MetricsDriftMonitor(baseline_metrics)

        metrics = {"statistical_parity": 0.94, "equal_opportunity": 0.91}

        result = monitor.add_observation(metrics, timestamp="2024-01-01")

        assert len(monitor.history) == 1
        assert monitor.history[0]["timestamp"] == "2024-01-01"
        assert isinstance(result, DriftResult)

    def test_window_size_limit(self, baseline_metrics: dict[str, float]):
        """Test that history respects window size."""
        monitor = MetricsDriftMonitor(baseline_metrics, window_size=3)

        # Add more observations than window size
        for i in range(5):
            metrics = {"statistical_parity": 0.90 + i * 0.01, "equal_opportunity": 0.90}
            monitor.add_observation(metrics)

        # Should only keep last 3
        assert len(monitor.history) == 3

    def test_check_drift(self, baseline_metrics: dict[str, float]):
        """Test checking drift across observations."""
        monitor = MetricsDriftMonitor(baseline_metrics, threshold=0.1)

        # Add observations with no drift
        for i in range(3):
            metrics = {"statistical_parity": 0.94, "equal_opportunity": 0.91}
            monitor.add_observation(metrics)

        report = monitor.check_drift()

        assert "has_drift" in report
        assert "num_observations" in report
        assert report["num_observations"] == 3

    def test_get_drift_trend(self, baseline_metrics: dict[str, float]):
        """Test getting drift trends."""
        monitor = MetricsDriftMonitor(baseline_metrics)

        # Add observations with increasing drift
        for i in range(3):
            metrics = {
                "statistical_parity": 0.95 - i * 0.05,
                "equal_opportunity": 0.92,
            }
            monitor.add_observation(metrics)

        trends = monitor.get_drift_trend()

        assert "statistical_parity" in trends
        assert "equal_opportunity" in trends
        assert len(trends["statistical_parity"]) == 3

    def test_monitor_with_psi_method(self, baseline_metrics: dict[str, float]):
        """Test monitor using PSI detection method."""
        monitor = MetricsDriftMonitor(baseline_metrics, method="psi", threshold=0.1)

        metrics = {"statistical_parity": 0.75, "equal_opportunity": 0.92}
        result = monitor.add_observation(metrics)

        assert result.method == "psi"

    def test_monitor_with_ks_method(self, baseline_metrics: dict[str, float]):
        """Test monitor using KS detection method."""
        monitor = MetricsDriftMonitor(baseline_metrics, method="ks", threshold=0.1)

        metrics = {"statistical_parity": 0.75, "equal_opportunity": 0.92}
        result = monitor.add_observation(metrics)

        assert result.method == "ks"
