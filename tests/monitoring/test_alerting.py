"""Tests for alerting module."""

import pytest

from justiceai.monitoring import (
    AlertConfig,
    ConsoleAlertChannel,
    FairnessAlerting,
    FairnessDriftDetector,
)


class TestAlertConfig:
    """Tests for AlertConfig class."""

    def test_initialization_defaults(self):
        """Test default configuration."""
        config = AlertConfig()

        assert config.enabled is True
        assert config.severity_threshold == "low"
        assert config.rate_limit_seconds == 300

    def test_initialization_custom(self):
        """Test custom configuration."""
        config = AlertConfig(
            enabled=False, severity_threshold="high", rate_limit_seconds=600
        )

        assert config.enabled is False
        assert config.severity_threshold == "high"
        assert config.rate_limit_seconds == 600


class TestConsoleAlertChannel:
    """Tests for ConsoleAlertChannel class."""

    def test_send_alert(self, capsys):
        """Test sending console alert."""
        channel = ConsoleAlertChannel()

        alert_data = {"severity": "high", "message": "Test drift detected"}

        result = channel.send(alert_data)

        assert result is True

        # Check console output
        captured = capsys.readouterr()
        assert "FAIRNESS ALERT" in captured.out
        assert "high" in captured.out
        assert "Test drift detected" in captured.out


class TestFairnessAlerting:
    """Tests for FairnessAlerting class."""

    def test_initialization(self):
        """Test alerting system initialization."""
        alerting = FairnessAlerting()

        assert len(alerting.channels) == 0
        assert alerting.config.enabled is True

    def test_add_channel(self):
        """Test adding alert channel."""
        alerting = FairnessAlerting()
        channel = ConsoleAlertChannel()

        alerting.add_channel("console", channel)

        assert "console" in alerting.channels
        assert alerting.channels["console"] is channel

    def test_remove_channel(self):
        """Test removing alert channel."""
        alerting = FairnessAlerting()
        channel = ConsoleAlertChannel()

        alerting.add_channel("console", channel)
        alerting.remove_channel("console")

        assert "console" not in alerting.channels

    def test_send_drift_alert(self):
        """Test sending drift alert."""
        alerting = FairnessAlerting()
        alerting.add_channel("console", ConsoleAlertChannel())

        # Create drift result
        baseline_metrics = {"statistical_parity": 0.95}
        detector = FairnessDriftDetector(baseline_metrics, threshold=0.1)
        new_metrics = {"statistical_parity": 0.70}  # Drift!

        result = detector.detect(new_metrics)

        # Send alert
        alert_results = alerting.send_drift_alert(result, detector)

        assert "console" in alert_results
        assert alert_results["console"] is True

    def test_no_alert_when_disabled(self):
        """Test that no alerts sent when disabled."""
        config = AlertConfig(enabled=False)
        alerting = FairnessAlerting(config)
        alerting.add_channel("console", ConsoleAlertChannel())

        baseline_metrics = {"statistical_parity": 0.95}
        detector = FairnessDriftDetector(baseline_metrics)
        new_metrics = {"statistical_parity": 0.70}

        result = detector.detect(new_metrics)
        alert_results = alerting.send_drift_alert(result, detector)

        # No alerts should be sent
        assert len(alert_results) == 0

    def test_no_alert_when_no_drift(self):
        """Test that no alerts sent when no drift detected."""
        alerting = FairnessAlerting()
        alerting.add_channel("console", ConsoleAlertChannel())

        baseline_metrics = {"statistical_parity": 0.95}
        detector = FairnessDriftDetector(baseline_metrics)
        new_metrics = {"statistical_parity": 0.94}  # No drift

        result = detector.detect(new_metrics)
        alert_results = alerting.send_drift_alert(result, detector)

        # No alerts should be sent
        assert len(alert_results) == 0
