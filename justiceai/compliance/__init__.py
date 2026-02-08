"""
Compliance module for Brazilian regulations.

This module provides compliance reporters for:
- LGPD (Lei Geral de Proteção de Dados) - Art. 20
- BACEN (Banco Central) - Resolution 4.658/2018

Example:
    >>> from justiceai import audit
    >>> from justiceai.compliance import LGPDComplianceReporter, BACENComplianceReporter
    >>>
    >>> # Run fairness audit
    >>> report = audit(model, data, protected_attrs=['gender'])
    >>>
    >>> # Generate LGPD compliance report
    >>> lgpd_reporter = LGPDComplianceReporter(report)
    >>> lgpd_reporter.save_html("lgpd_compliance.html")
    >>>
    >>> # Generate BACEN compliance report
    >>> bacen_reporter = BACENComplianceReporter(report)
    >>> bacen_reporter.save_html("bacen_compliance.html")
"""

from justiceai.compliance.bacen import BACENComplianceReporter
from justiceai.compliance.lgpd import LGPDComplianceReporter

__all__ = ["LGPDComplianceReporter", "BACENComplianceReporter"]
