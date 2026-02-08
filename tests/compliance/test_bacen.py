"""Tests for BACEN compliance module."""

import pytest
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier

from justiceai import audit
from justiceai.compliance import BACENComplianceReporter


class TestBACENComplianceReporter:
    """Tests for BACENComplianceReporter class."""

    @pytest.fixture
    def fairness_report(self):
        """Create a fairness report for testing."""
        import pandas as pd

        # Create sample data
        X, y = make_classification(n_samples=200, n_features=5, random_state=42)
        protected_attr = [0] * 100 + [1] * 100

        # Train model
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)

        # Create DataFrame
        data = pd.DataFrame(X)
        data["gender"] = protected_attr
        data["target"] = y

        # Run audit
        report = audit(model, X, y, sensitive_attrs=data["gender"])

        return report

    def test_initialization(self, fairness_report):
        """Test reporter initialization."""
        reporter = BACENComplianceReporter(fairness_report)

        assert reporter.fairness_report is fairness_report
        assert len(reporter.compliance_data) == 0

    def test_generate_report(self, fairness_report):
        """Test generating compliance report."""
        reporter = BACENComplianceReporter(fairness_report)

        compliance_data = reporter.generate_report()

        assert "identificacao_modelo" in compliance_data
        assert "validacao_modelo" in compliance_data
        assert "governanca" in compliance_data
        assert "risco_modelo" in compliance_data
        assert "monitoramento" in compliance_data
        assert "fairness_assessment" in compliance_data
        assert "recomendacoes" in compliance_data

    def test_risk_assessment(self, fairness_report):
        """Test risk assessment functionality."""
        reporter = BACENComplianceReporter(fairness_report)
        compliance_data = reporter.generate_report()

        risk_assessment = compliance_data["risco_modelo"]

        assert "nivel_risco" in risk_assessment
        assert risk_assessment["nivel_risco"] in ["BAIXO", "MÉDIO", "ALTO"]
        assert "total_disparidades" in risk_assessment

    def test_to_dict(self, fairness_report):
        """Test exporting compliance data as dict."""
        reporter = BACENComplianceReporter(fairness_report)

        compliance_dict = reporter.to_dict()

        assert isinstance(compliance_dict, dict)
        assert len(compliance_dict) > 0

    def test_save_html(self, fairness_report, tmp_path):
        """Test saving HTML report."""
        reporter = BACENComplianceReporter(fairness_report)

        output_file = tmp_path / "bacen_report.html"
        reporter.save_html(str(output_file))

        assert output_file.exists()
        content = output_file.read_text()
        assert "BACEN" in content
        assert "Resolução" in content
