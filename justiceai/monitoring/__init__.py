"""
Monitoring module for continuous fairness evaluation.

This module provides:
- Drift detection for fairness metrics
- Alerting system with multiple channels
- Continuous monitoring utilities

Example:
    >>> from justiceai.monitoring import (
    ...     FairnessDriftDetector,
    ...     MetricsDriftMonitor,
    ...     FairnessAlerting,
    ...     ConsoleAlertChannel
    ... )
    >>>
    >>> # Setup drift detector
    >>> detector = FairnessDriftDetector(baseline_metrics)
    >>>
    >>> # Setup alerting
    >>> alerting = FairnessAlerting()
    >>> alerting.add_channel('console', ConsoleAlertChannel())
    >>>
    >>> # Detect and alert
    >>> result = detector.detect(new_metrics)
    >>> if result.has_drift:
    ...     alerting.send_drift_alert(result, detector)
"""

from justiceai.monitoring.alerting import (
    AlertChannel,
    AlertConfig,
    ConsoleAlertChannel,
    EmailAlertChannel,
    FairnessAlerting,
    SlackAlertChannel,
    WebhookAlertChannel,
)
from justiceai.monitoring.drift_detector import (
    DriftResult,
    FairnessDriftDetector,
    MetricsDriftMonitor,
)

__all__ = [
    "FairnessDriftDetector",
    "MetricsDriftMonitor",
    "DriftResult",
    "FairnessAlerting",
    "AlertConfig",
    "AlertChannel",
    "ConsoleAlertChannel",
    "EmailAlertChannel",
    "SlackAlertChannel",
    "WebhookAlertChannel",
]
