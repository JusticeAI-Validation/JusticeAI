"""Tests for alerting module."""

from unittest.mock import MagicMock, Mock, patch

import pytest

from justiceai.monitoring import (
    AlertConfig,
    ConsoleAlertChannel,
    EmailAlertChannel,
    FairnessAlerting,
    FairnessDriftDetector,
    SlackAlertChannel,
    WebhookAlertChannel,
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

    def test_severity_filtering_high(self):
        """Test severity threshold filtering for high severity only."""
        config = AlertConfig(severity_threshold="high")
        alerting = FairnessAlerting(config)
        alerting.add_channel("console", ConsoleAlertChannel())

        baseline_metrics = {"statistical_parity": 0.95}
        detector = FairnessDriftDetector(baseline_metrics, threshold=0.05)
        new_metrics = {"statistical_parity": 0.70}  # High severity drift

        result = detector.detect(new_metrics)
        alert_results = alerting.send_drift_alert(result, detector)

        # Alert should be sent for high severity
        assert "console" in alert_results


class TestEmailAlertChannel:
    """Tests for EmailAlertChannel class."""

    def test_initialization(self):
        """Test email channel initialization."""
        config = {
            "smtp_host": "smtp.gmail.com",
            "smtp_port": 587,
            "username": "test@example.com",
            "password": "password",
            "from_email": "alerts@example.com",
            "to_emails": ["user@example.com"],
        }
        channel = EmailAlertChannel(config)

        assert channel.smtp_host == "smtp.gmail.com"
        assert channel.smtp_port == 587
        assert channel.username == "test@example.com"
        assert channel.from_email == "alerts@example.com"
        assert channel.to_emails == ["user@example.com"]

    def test_send_missing_config(self, capsys):
        """Test sending email with missing configuration."""
        config = {"smtp_host": "smtp.gmail.com"}  # Missing required fields
        channel = EmailAlertChannel(config)

        alert_data = {"severity": "high", "message": "Test alert"}
        result = channel.send(alert_data)

        assert result is False
        captured = capsys.readouterr()
        assert "not properly configured" in captured.out

    def test_send_missing_recipients(self, capsys):
        """Test sending email with no recipients."""
        config = {
            "smtp_host": "smtp.gmail.com",
            "username": "test@example.com",
            "password": "password",
            "from_email": "alerts@example.com",
            "to_emails": [],
        }
        channel = EmailAlertChannel(config)

        alert_data = {"severity": "high", "message": "Test alert"}
        result = channel.send(alert_data)

        assert result is False
        captured = capsys.readouterr()
        assert "No recipient emails configured" in captured.out

    @patch("smtplib.SMTP")
    def test_send_success(self, mock_smtp):
        """Test successful email sending."""
        config = {
            "smtp_host": "smtp.gmail.com",
            "smtp_port": 587,
            "username": "test@example.com",
            "password": "password",
            "from_email": "alerts@example.com",
            "to_emails": ["user@example.com"],
            "use_tls": True,
        }
        channel = EmailAlertChannel(config)

        # Mock SMTP server
        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        alert_data = {
            "severity": "high",
            "message": "Test drift detected",
            "drifted_metrics": ["statistical_parity"],
            "timestamp": "2024-02-08 10:00:00",
        }
        result = channel.send(alert_data)

        assert result is True
        mock_server.starttls.assert_called_once()
        mock_server.login.assert_called_once_with("test@example.com", "password")
        mock_server.send_message.assert_called_once()

    @patch("smtplib.SMTP")
    def test_send_without_tls(self, mock_smtp):
        """Test email sending without TLS."""
        config = {
            "smtp_host": "smtp.example.com",
            "username": "test@example.com",
            "password": "password",
            "from_email": "alerts@example.com",
            "to_emails": ["user@example.com"],
            "use_tls": False,
        }
        channel = EmailAlertChannel(config)

        mock_server = MagicMock()
        mock_smtp.return_value.__enter__.return_value = mock_server

        alert_data = {"severity": "low", "message": "Test"}
        result = channel.send(alert_data)

        assert result is True
        mock_server.starttls.assert_not_called()

    @patch("smtplib.SMTP")
    def test_send_failure(self, mock_smtp, capsys):
        """Test email sending failure."""
        config = {
            "smtp_host": "smtp.gmail.com",
            "username": "test@example.com",
            "password": "password",
            "from_email": "alerts@example.com",
            "to_emails": ["user@example.com"],
        }
        channel = EmailAlertChannel(config)

        # Mock SMTP to raise exception
        mock_smtp.side_effect = Exception("Connection failed")

        alert_data = {"severity": "high", "message": "Test"}
        result = channel.send(alert_data)

        assert result is False
        captured = capsys.readouterr()
        assert "Failed to send email alert" in captured.out


class TestSlackAlertChannel:
    """Tests for SlackAlertChannel class."""

    def test_initialization(self):
        """Test Slack channel initialization."""
        config = {"webhook_url": "https://hooks.slack.com/services/TEST"}
        channel = SlackAlertChannel(config)

        assert channel.webhook_url == "https://hooks.slack.com/services/TEST"

    def test_send_missing_webhook(self, capsys):
        """Test sending Slack alert with missing webhook URL."""
        config = {}
        channel = SlackAlertChannel(config)

        alert_data = {"severity": "high", "message": "Test alert"}
        result = channel.send(alert_data)

        assert result is False
        captured = capsys.readouterr()
        assert "webhook URL not configured" in captured.out

    @patch("urllib.request.urlopen")
    def test_send_success(self, mock_urlopen):
        """Test successful Slack alert sending."""
        config = {"webhook_url": "https://hooks.slack.com/services/TEST"}
        channel = SlackAlertChannel(config)

        mock_response = MagicMock()
        mock_response.status = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        alert_data = {
            "severity": "high",
            "message": "Test drift detected",
            "drifted_metrics": ["statistical_parity", "equal_opportunity"],
            "timestamp": "2024-02-08 10:00:00",
        }
        result = channel.send(alert_data)

        assert result is True
        mock_urlopen.assert_called_once()

    @patch("urllib.request.urlopen")
    def test_send_failure(self, mock_urlopen, capsys):
        """Test Slack alert sending failure."""
        config = {"webhook_url": "https://hooks.slack.com/services/TEST"}
        channel = SlackAlertChannel(config)

        mock_urlopen.side_effect = Exception("Network error")

        alert_data = {"severity": "high", "message": "Test"}
        result = channel.send(alert_data)

        assert result is False
        captured = capsys.readouterr()
        assert "Failed to send Slack alert" in captured.out


class TestWebhookAlertChannel:
    """Tests for WebhookAlertChannel class."""

    def test_initialization(self):
        """Test webhook channel initialization."""
        config = {
            "webhook_url": "https://example.com/webhook",
            "method": "POST",
            "headers": {"Authorization": "Bearer token"},
        }
        channel = WebhookAlertChannel(config)

        assert channel.webhook_url == "https://example.com/webhook"
        assert channel.method == "POST"
        assert channel.headers == {"Authorization": "Bearer token"}

    def test_initialization_defaults(self):
        """Test webhook channel with default values."""
        config = {"webhook_url": "https://example.com/webhook"}
        channel = WebhookAlertChannel(config)

        assert channel.method == "POST"
        assert channel.headers == {}

    def test_send_missing_url(self, capsys):
        """Test sending webhook alert with missing URL."""
        config = {}
        channel = WebhookAlertChannel(config)

        alert_data = {"severity": "high", "message": "Test"}
        result = channel.send(alert_data)

        assert result is False
        captured = capsys.readouterr()
        assert "Webhook URL not configured" in captured.out

    @patch("urllib.request.urlopen")
    def test_send_success(self, mock_urlopen):
        """Test successful webhook alert sending."""
        config = {"webhook_url": "https://example.com/webhook"}
        channel = WebhookAlertChannel(config)

        mock_response = MagicMock()
        mock_response.status = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        alert_data = {"severity": "high", "message": "Test"}
        result = channel.send(alert_data)

        assert result is True

    @patch("urllib.request.urlopen")
    def test_send_failure(self, mock_urlopen, capsys):
        """Test webhook alert sending failure."""
        config = {"webhook_url": "https://example.com/webhook"}
        channel = WebhookAlertChannel(config)

        mock_urlopen.side_effect = Exception("Connection error")

        alert_data = {"severity": "high", "message": "Test"}
        result = channel.send(alert_data)

        assert result is False
        captured = capsys.readouterr()
        assert "Failed to send webhook alert" in captured.out
