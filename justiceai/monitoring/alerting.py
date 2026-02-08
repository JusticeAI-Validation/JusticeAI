"""
Alerting System for Fairness Monitoring.

This module provides configurable alerting for fairness drift detection
with support for multiple notification channels (email, Slack, webhooks).
"""

import json
import smtplib
from abc import ABC, abstractmethod
from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from typing import Any
from urllib import request as urllib_request

from justiceai.monitoring.drift_detector import DriftResult


@dataclass
class AlertConfig:
    """
    Configuration for alerts.

    Attributes:
        enabled: Whether alerting is enabled
        severity_threshold: Minimum severity to trigger alert ('low', 'medium', 'high')
        channels: List of notification channels to use
        rate_limit_seconds: Minimum seconds between alerts (0 = no limit)
    """

    enabled: bool = True
    severity_threshold: str = "low"
    channels: list[str] | None = None
    rate_limit_seconds: int = 300  # 5 minutes default


class AlertChannel(ABC):
    """
    Abstract base class for alert notification channels.

    Subclass this to implement custom notification channels.
    """

    @abstractmethod
    def send(self, alert_data: dict[str, Any]) -> bool:
        """
        Send alert through this channel.

        Args:
            alert_data: Dictionary containing alert information

        Returns:
            True if alert was sent successfully, False otherwise
        """
        pass


class ConsoleAlertChannel(AlertChannel):
    """
    Alert channel that prints to console.

    Useful for development and testing.

    Example:
        >>> channel = ConsoleAlertChannel()
        >>> channel.send({'message': 'Drift detected!', 'severity': 'high'})
        ===== FAIRNESS ALERT =====
        Severity: high
        Message: Drift detected!
        ==========================
        True
    """

    def send(self, alert_data: dict[str, Any]) -> bool:
        """Send alert to console."""
        print("\n" + "=" * 30)
        print("FAIRNESS ALERT")
        print("=" * 30)
        print(f"Severity: {alert_data.get('severity', 'unknown')}")
        print(f"Message: {alert_data.get('message', 'No message')}")

        if "drifted_metrics" in alert_data:
            print(f"Drifted Metrics: {', '.join(alert_data['drifted_metrics'])}")

        if "details" in alert_data:
            print(f"Details: {alert_data['details']}")

        print("=" * 30 + "\n")
        return True


class EmailAlertChannel(AlertChannel):
    """
    Alert channel that sends email notifications.

    Example:
        >>> config = {
        ...     'smtp_host': 'smtp.gmail.com',
        ...     'smtp_port': 587,
        ...     'username': 'your-email@gmail.com',
        ...     'password': 'your-app-password',
        ...     'from_email': 'your-email@gmail.com',
        ...     'to_emails': ['recipient@example.com']
        ... }
        >>> channel = EmailAlertChannel(config)
        >>> channel.send({'message': 'Drift detected!', 'severity': 'high'})
    """

    def __init__(self, config: dict[str, Any]):
        """
        Initialize Email alert channel.

        Args:
            config: Dictionary with email configuration:
                - smtp_host: SMTP server hostname
                - smtp_port: SMTP server port
                - username: SMTP username
                - password: SMTP password
                - from_email: Sender email address
                - to_emails: List of recipient email addresses
                - use_tls: Whether to use TLS (default: True)
        """
        self.smtp_host = config.get("smtp_host")
        self.smtp_port = config.get("smtp_port", 587)
        self.username = config.get("username")
        self.password = config.get("password")
        self.from_email = config.get("from_email")
        self.to_emails = config.get("to_emails", [])
        self.use_tls = config.get("use_tls", True)

    def send(self, alert_data: dict[str, Any]) -> bool:
        """Send alert via email."""
        if not all([self.smtp_host, self.username, self.password, self.from_email]):
            print("Email alert channel not properly configured")
            return False

        if not self.to_emails:
            print("No recipient emails configured")
            return False

        try:
            # Create message
            msg = MIMEMultipart("alternative")
            msg["Subject"] = (
                f"[JusticeAI] Fairness Alert - {alert_data.get('severity', 'unknown').upper()}"
            )
            msg["From"] = self.from_email
            msg["To"] = ", ".join(self.to_emails)

            # Create email body
            body = self._create_email_body(alert_data)
            msg.attach(MIMEText(body, "html"))

            # Send email
            with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
                if self.use_tls:
                    server.starttls()
                server.login(self.username, self.password)
                server.send_message(msg)

            return True

        except Exception as e:
            print(f"Failed to send email alert: {e}")
            return False

    def _create_email_body(self, alert_data: dict[str, Any]) -> str:
        """Create HTML email body."""
        severity_colors = {
            "high": "#dc3545",
            "medium": "#ffc107",
            "low": "#17a2b8",
        }
        severity = alert_data.get("severity", "unknown")
        color = severity_colors.get(severity, "#6c757d")

        html = f"""
        <html>
        <body style="font-family: Arial, sans-serif; padding: 20px;">
            <div style="background-color: #f8f9fa; padding: 20px; border-left: 4px solid {color};">
                <h2 style="color: {color}; margin-top: 0;">Fairness Alert - {severity.upper()}</h2>
                <p><strong>Message:</strong> {alert_data.get('message', 'No message')}</p>
        """

        if "drifted_metrics" in alert_data and alert_data["drifted_metrics"]:
            html += f"""
                <p><strong>Drifted Metrics:</strong> {', '.join(alert_data['drifted_metrics'])}</p>
            """

        if "timestamp" in alert_data:
            html += f"""
                <p><strong>Timestamp:</strong> {alert_data['timestamp']}</p>
            """

        html += """
            </div>
            <p style="color: #666; font-size: 0.9em; margin-top: 20px;">
                This is an automated alert from JusticeAI Fairness Monitoring System.
            </p>
        </body>
        </html>
        """

        return html


class SlackAlertChannel(AlertChannel):
    """
    Alert channel that sends notifications to Slack.

    Example:
        >>> config = {'webhook_url': 'https://hooks.slack.com/services/YOUR/WEBHOOK/URL'}
        >>> channel = SlackAlertChannel(config)
        >>> channel.send({'message': 'Drift detected!', 'severity': 'high'})
    """

    def __init__(self, config: dict[str, Any]):
        """
        Initialize Slack alert channel.

        Args:
            config: Dictionary with Slack configuration:
                - webhook_url: Slack webhook URL
        """
        self.webhook_url = config.get("webhook_url")

    def send(self, alert_data: dict[str, Any]) -> bool:
        """Send alert to Slack."""
        if not self.webhook_url:
            print("Slack webhook URL not configured")
            return False

        try:
            # Create Slack message payload
            severity_emojis = {"high": ":rotating_light:", "medium": ":warning:", "low": ":information_source:"}
            severity = alert_data.get("severity", "unknown")
            emoji = severity_emojis.get(severity, ":bell:")

            payload = {
                "text": f"{emoji} *Fairness Alert - {severity.upper()}*",
                "blocks": [
                    {
                        "type": "header",
                        "text": {
                            "type": "plain_text",
                            "text": f"{emoji} Fairness Alert - {severity.upper()}",
                        },
                    },
                    {
                        "type": "section",
                        "text": {
                            "type": "mrkdwn",
                            "text": f"*Message:* {alert_data.get('message', 'No message')}",
                        },
                    },
                ],
            }

            # Add drifted metrics if present
            if "drifted_metrics" in alert_data and alert_data["drifted_metrics"]:
                metrics_text = ", ".join(alert_data["drifted_metrics"])
                payload["blocks"].append(
                    {
                        "type": "section",
                        "text": {"type": "mrkdwn", "text": f"*Drifted Metrics:* {metrics_text}"},
                    }
                )

            # Send to Slack
            req = urllib_request.Request(
                self.webhook_url,
                data=json.dumps(payload).encode("utf-8"),
                headers={"Content-Type": "application/json"},
            )

            with urllib_request.urlopen(req) as response:
                return response.status == 200

        except Exception as e:
            print(f"Failed to send Slack alert: {e}")
            return False


class WebhookAlertChannel(AlertChannel):
    """
    Alert channel that sends to generic webhook.

    Example:
        >>> config = {
        ...     'webhook_url': 'https://your-api.com/alerts',
        ...     'headers': {'Authorization': 'Bearer YOUR_TOKEN'}
        ... }
        >>> channel = WebhookAlertChannel(config)
        >>> channel.send({'message': 'Drift detected!', 'severity': 'high'})
    """

    def __init__(self, config: dict[str, Any]):
        """
        Initialize Webhook alert channel.

        Args:
            config: Dictionary with webhook configuration:
                - webhook_url: Webhook URL
                - headers: Optional HTTP headers dictionary
                - method: HTTP method (default: 'POST')
        """
        self.webhook_url = config.get("webhook_url")
        self.headers = config.get("headers", {})
        self.method = config.get("method", "POST")

    def send(self, alert_data: dict[str, Any]) -> bool:
        """Send alert to webhook."""
        if not self.webhook_url:
            print("Webhook URL not configured")
            return False

        try:
            # Prepare request
            headers = {"Content-Type": "application/json", **self.headers}

            req = urllib_request.Request(
                self.webhook_url,
                data=json.dumps(alert_data).encode("utf-8"),
                headers=headers,
                method=self.method,
            )

            with urllib_request.urlopen(req) as response:
                return 200 <= response.status < 300

        except Exception as e:
            print(f"Failed to send webhook alert: {e}")
            return False


class FairnessAlerting:
    """
    Main alerting system for fairness monitoring.

    Manages multiple alert channels and handles drift detection alerts.

    Example:
        >>> from justiceai.monitoring import FairnessAlerting, FairnessDriftDetector
        >>>
        >>> # Configure alerting
        >>> alerting = FairnessAlerting()
        >>> alerting.add_channel('console', ConsoleAlertChannel())
        >>>
        >>> # Detect drift
        >>> detector = FairnessDriftDetector(baseline_metrics)
        >>> drift_result = detector.detect(new_metrics)
        >>>
        >>> # Send alert if drift detected
        >>> if drift_result.has_drift:
        ...     alerting.send_drift_alert(drift_result, detector)
    """

    def __init__(self, config: AlertConfig | None = None):
        """
        Initialize Fairness Alerting system.

        Args:
            config: Alert configuration (uses defaults if not provided)
        """
        self.config = config or AlertConfig()
        self.channels: dict[str, AlertChannel] = {}
        self.last_alert_time: dict[str, float] = {}

    def add_channel(self, name: str, channel: AlertChannel) -> None:
        """
        Add an alert channel.

        Args:
            name: Channel name (e.g., 'email', 'slack', 'console')
            channel: AlertChannel instance

        Example:
            >>> alerting.add_channel('console', ConsoleAlertChannel())
            >>> alerting.add_channel('email', EmailAlertChannel(email_config))
        """
        self.channels[name] = channel

    def remove_channel(self, name: str) -> None:
        """Remove an alert channel by name."""
        if name in self.channels:
            del self.channels[name]

    def send_drift_alert(
        self, drift_result: DriftResult, detector: Any, timestamp: str | None = None
    ) -> dict[str, bool]:
        """
        Send alert for drift detection result.

        Args:
            drift_result: DriftResult from drift detector
            detector: FairnessDriftDetector instance
            timestamp: Optional timestamp for the alert

        Returns:
            Dictionary mapping channel names to success status

        Example:
            >>> results = alerting.send_drift_alert(drift_result, detector)
            >>> print(f"Console: {results['console']}")
        """
        if not self.config.enabled:
            return {}

        if not drift_result.has_drift:
            return {}

        # Get drift summary
        summary = detector.get_drift_summary(drift_result)

        # Check severity threshold
        severity = summary.get("severity", "low")
        if not self._should_alert(severity):
            return {}

        # Prepare alert data
        alert_data = {
            "severity": severity,
            "message": summary.get("message", "Drift detected"),
            "drifted_metrics": list(drift_result.drifted_metrics.keys()),
            "drift_scores": drift_result.drift_scores,
            "method": drift_result.method,
            "threshold": drift_result.threshold,
            "timestamp": timestamp or "N/A",
            "num_drifted": len(drift_result.drifted_metrics),
            "num_total": summary.get("num_metrics_checked", 0),
        }

        # Send to all configured channels
        results = {}
        for name, channel in self.channels.items():
            try:
                success = channel.send(alert_data)
                results[name] = success
            except Exception as e:
                print(f"Error sending alert to {name}: {e}")
                results[name] = False

        return results

    def _should_alert(self, severity: str) -> bool:
        """Check if alert should be sent based on severity threshold."""
        severity_levels = {"low": 1, "medium": 2, "high": 3}
        threshold_level = severity_levels.get(self.config.severity_threshold, 1)
        alert_level = severity_levels.get(severity, 1)

        return alert_level >= threshold_level
