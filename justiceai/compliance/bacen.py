"""
BACEN Compliance Reporter.

This module provides compliance reporting according to Brazilian Central Bank
Resolution 4.658/2018 for model risk management in financial institutions.

BACEN Resolution 4.658/2018 requires:
- Model validation and testing
- Performance monitoring
- Risk assessment and governance
- Documentation and auditability
"""

from typing import Any

import pandas as pd

from justiceai.reports.fairness_report import FairnessReport


class BACENComplianceReporter:
    """
    BACEN Compliance Reporter for model risk management.

    This reporter generates documentation according to BACEN Resolution 4.658/2018,
    which mandates governance and risk management for models used in financial
    institutions.

    Key requirements addressed:
        - Model validation (validação de modelos)
        - Performance monitoring (monitoramento de desempenho)
        - Risk assessment (avaliação de riscos)
        - Model governance (governança de modelos)
        - Documentation in Portuguese (BR)

    Example:
        >>> from justiceai import audit
        >>> from justiceai.compliance import BACENComplianceReporter
        >>>
        >>> # Run fairness audit
        >>> report = audit(model, data, protected_attrs=['gender'])
        >>>
        >>> # Generate BACEN compliance report
        >>> bacen_reporter = BACENComplianceReporter(report)
        >>> compliance_doc = bacen_reporter.generate_report()
        >>> bacen_reporter.save_html("bacen_compliance.html")

    References:
        BACEN Res. 4.658/2018: https://www.bcb.gov.br/estabilidadefinanceira/exibenormativo?tipo=Resolu%C3%A7%C3%A3o&numero=4658
    """

    def __init__(self, fairness_report: FairnessReport):
        """
        Initialize BACEN Compliance Reporter.

        Args:
            fairness_report: FairnessReport instance with fairness analysis
        """
        self.fairness_report = fairness_report
        self.compliance_data: dict[str, Any] = {}

    def generate_report(self) -> dict[str, Any]:
        """
        Generate BACEN compliance report.

        Returns:
            Dictionary with compliance documentation sections:
                - identificacao_modelo: Model identification
                - validacao_modelo: Model validation results
                - governanca: Governance information
                - risco_modelo: Model risk assessment
                - monitoramento: Performance monitoring
                - fairness_assessment: Fairness analysis
                - recomendacoes: Recommendations

        Example:
            >>> compliance_doc = bacen_reporter.generate_report()
            >>> print(compliance_doc['identificacao_modelo']['tipo'])
            'Modelo de Classificação Binária'
        """
        # Extract data from fairness report
        result = self.fairness_report.fairness_result

        # 1. Identificação do Modelo
        self.compliance_data["identificacao_modelo"] = {
            "tipo": "Modelo de Classificação Binária",
            "framework": self._get_model_type(),
            "finalidade": "Apoio à decisão automatizada",
            "data_validacao": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
            "versao_avaliacao": "1.0",
        }

        # 2. Validação do Modelo
        self.compliance_data["validacao_modelo"] = {
            "metricas_calculadas": len(result.metrics),
            "atributos_sensíveis_analisados": result.protected_attrs,
            "grupos_avaliados": self._get_analyzed_groups(),
            "metodologia": "Análise de Fairness com múltiplas métricas",
        }

        # 3. Governança
        self.compliance_data["governanca"] = {
            "framework_utilizado": "JusticeAI - Fairness Evaluation",
            "processo_avaliacao": "Automatizado com revisão",
            "frequencia_recomendada": "Mensal ou sob demanda",
            "documentacao": "Relatório completo de fairness disponível",
        }

        # 4. Risco do Modelo
        self.compliance_data["risco_modelo"] = self._assess_model_risk()

        # 5. Monitoramento
        self.compliance_data["monitoramento"] = {
            "metricas_monitoradas": self._get_monitored_metrics(),
            "alertas_configurados": self._get_alert_configuration(),
            "frequencia_monitoramento": "Contínuo",
        }

        # 6. Fairness Assessment
        self.compliance_data["fairness_assessment"] = {
            "disparidades_identificadas": self._identify_disparities(),
            "nivel_risco_fairness": self._assess_fairness_risk(),
            "ações_mitigacao": self._suggest_mitigation_actions(),
        }

        # 7. Recomendações
        self.compliance_data["recomendacoes"] = self._generate_recommendations()

        return self.compliance_data

    def _get_model_type(self) -> str:
        """Get model framework/type."""
        result = self.fairness_report.fairness_result
        if hasattr(result, "model"):
            return type(result.model).__name__
        return "Classificador ML"

    def _get_analyzed_groups(self) -> dict[str, list[str]]:
        """Get list of analyzed groups per protected attribute."""
        result = self.fairness_report.fairness_result
        groups = {}

        for attr in result.protected_attrs:
            if attr in result.metrics:
                groups[attr] = list(result.metrics[attr].keys())

        return groups

    def _assess_model_risk(self) -> dict[str, Any]:
        """Assess model risk according to BACEN criteria."""
        disparities = self._identify_disparities()

        # Risk classification based on number and severity of disparities
        num_high_severity = sum(
            1 for d in disparities if d.get("severidade") == "Alta"
        )
        num_medium_severity = sum(
            1 for d in disparities if d.get("severidade") == "Média"
        )

        if num_high_severity > 0:
            risk_level = "ALTO"
            risk_description = (
                f"{num_high_severity} disparidade(s) de alta severidade identificada(s)"
            )
        elif num_medium_severity > 0:
            risk_level = "MÉDIO"
            risk_description = (
                f"{num_medium_severity} disparidade(s) de média severidade identificada(s)"
            )
        else:
            risk_level = "BAIXO"
            risk_description = "Nenhuma disparidade crítica identificada"

        return {
            "nivel_risco": risk_level,
            "descricao": risk_description,
            "total_disparidades": len(disparities),
            "disparidades_alta_severidade": num_high_severity,
            "disparidades_media_severidade": num_medium_severity,
            "requer_acao_imediata": num_high_severity > 0,
        }

    def _identify_disparities(self) -> list[dict[str, Any]]:
        """Identify disparities exceeding fairness thresholds."""
        result = self.fairness_report.fairness_result
        disparities = []

        threshold = 0.8  # 80% rule for fairness

        for attr in result.protected_attrs:
            if attr in result.metrics:
                for group, group_metrics in result.metrics[attr].items():
                    # Check statistical parity
                    if "statistical_parity" in group_metrics:
                        sp_ratio = group_metrics["statistical_parity"]
                        if sp_ratio < threshold:
                            disparities.append(
                                {
                                    "atributo": attr,
                                    "grupo": group,
                                    "metrica": "Statistical Parity",
                                    "valor": sp_ratio,
                                    "threshold": threshold,
                                    "desvio": threshold - sp_ratio,
                                    "severidade": "Alta"
                                    if sp_ratio < 0.6
                                    else "Média",
                                }
                            )

                    # Check equal opportunity
                    if "equal_opportunity" in group_metrics:
                        eo_ratio = group_metrics["equal_opportunity"]
                        if eo_ratio < threshold:
                            disparities.append(
                                {
                                    "atributo": attr,
                                    "grupo": group,
                                    "metrica": "Equal Opportunity",
                                    "valor": eo_ratio,
                                    "threshold": threshold,
                                    "desvio": threshold - eo_ratio,
                                    "severidade": "Alta"
                                    if eo_ratio < 0.6
                                    else "Média",
                                }
                            )

        return disparities

    def _get_monitored_metrics(self) -> list[str]:
        """Get list of metrics being monitored."""
        result = self.fairness_report.fairness_result

        # Collect all unique metric names
        metric_names = set()
        for attr in result.protected_attrs:
            if attr in result.metrics:
                for group_metrics in result.metrics[attr].values():
                    metric_names.update(group_metrics.keys())

        return sorted(list(metric_names))

    def _get_alert_configuration(self) -> dict[str, Any]:
        """Get alert configuration for monitoring."""
        return {
            "threshold_fairness": 0.8,
            "threshold_critico": 0.6,
            "alertas_ativos": [
                "Statistical Parity < 0.8",
                "Equal Opportunity < 0.8",
                "Predictive Parity < 0.8",
            ],
            "canais_notificacao": ["Email", "Dashboard", "API"],
        }

    def _assess_fairness_risk(self) -> str:
        """Assess overall fairness risk level."""
        disparities = self._identify_disparities()

        num_high_severity = sum(
            1 for d in disparities if d.get("severidade") == "Alta"
        )

        if num_high_severity > 0:
            return "ALTO"
        elif len(disparities) > 0:
            return "MÉDIO"
        else:
            return "BAIXO"

    def _suggest_mitigation_actions(self) -> list[str]:
        """Suggest mitigation actions for identified risks."""
        disparities = self._identify_disparities()
        actions = []

        if not disparities:
            actions.append(
                "Manter monitoramento contínuo das métricas de fairness"
            )
            return actions

        # Specific actions based on disparities
        has_statistical_parity_issue = any(
            d["metrica"] == "Statistical Parity" for d in disparities
        )
        has_equal_opportunity_issue = any(
            d["metrica"] == "Equal Opportunity" for d in disparities
        )

        if has_statistical_parity_issue:
            actions.append(
                "Revisar processo de coleta de dados para garantir "
                "representatividade dos grupos"
            )
            actions.append(
                "Considerar técnicas de re-balanceamento de dados (oversampling/undersampling)"
            )

        if has_equal_opportunity_issue:
            actions.append(
                "Avaliar features que podem estar correlacionadas com "
                "atributos protegidos"
            )
            actions.append(
                "Considerar técnicas de fairness-aware learning durante treinamento"
            )

        actions.append(
            "Implementar sistema de monitoramento contínuo para detectar drift"
        )
        actions.append(
            "Realizar revisão periódica (mensal) das métricas de fairness"
        )
        actions.append(
            "Documentar todas as intervenções e resultados para auditoria"
        )

        return actions

    def _generate_recommendations(self) -> list[str]:
        """Generate BACEN compliance recommendations."""
        risk_assessment = self._assess_model_risk()

        recommendations = [
            "Manter documentação completa do modelo conforme Resolução BACEN 4.658/2018",
            "Realizar validação periódica do modelo (mínimo trimestral)",
            "Implementar controles de governança de modelos",
            "Manter registro de todas as avaliações para fins de auditoria",
        ]

        if risk_assessment["nivel_risco"] == "ALTO":
            recommendations.insert(
                0,
                "⚠️ AÇÃO URGENTE: Risco ALTO identificado. "
                "Revisar modelo antes de uso em produção.",
            )
            recommendations.append(
                "Considerar suspensão do modelo até mitigação dos riscos identificados"
            )
        elif risk_assessment["nivel_risco"] == "MÉDIO":
            recommendations.insert(
                0, "Risco MÉDIO: Implementar plano de mitigação no curto prazo."
            )

        recommendations.append(
            "Estabelecer processo de monitoramento contínuo com alertas automáticos"
        )
        recommendations.append(
            "Capacitar equipe técnica em práticas de fairness e compliance"
        )

        return recommendations

    def save_html(self, output_path: str) -> None:
        """
        Save BACEN compliance report as HTML file.

        Args:
            output_path: Path to save HTML file

        Example:
            >>> bacen_reporter.save_html("compliance/bacen_report.html")
        """
        if not self.compliance_data:
            self.generate_report()

        html_content = self._generate_html()

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    def _generate_html(self) -> str:
        """Generate HTML content for BACEN compliance report."""
        # Start with fairness report HTML
        base_html = self.fairness_report.to_html()

        # Add BACEN compliance section
        compliance_section = self._create_compliance_section_html()

        # Insert compliance section before closing body tag
        html_with_compliance = base_html.replace(
            "</body>", f"{compliance_section}</body>"
        )

        return html_with_compliance

    def _create_compliance_section_html(self) -> str:
        """Create HTML section for BACEN compliance."""
        if not self.compliance_data:
            self.generate_report()

        # Determine risk color
        risk_level = self.compliance_data["risco_modelo"]["nivel_risco"]
        risk_color = {"ALTO": "#dc3545", "MÉDIO": "#ffc107", "BAIXO": "#28a745"}.get(
            risk_level, "#6c757d"
        )

        html = f"""
        <div style="margin-top: 40px; padding: 20px; background-color: #f8f9fa; border-left: 4px solid #006400;">
            <h2>🏦 Relatório de Conformidade BACEN</h2>
            <p><strong>Resolução BACEN nº 4.658/2018</strong></p>
            <p><em>Gestão de Risco de Modelos e Governança</em></p>

            <h3>1. Identificação do Modelo</h3>
            <ul>
                <li><strong>Tipo:</strong> {self.compliance_data['identificacao_modelo']['tipo']}</li>
                <li><strong>Framework:</strong> {self.compliance_data['identificacao_modelo']['framework']}</li>
                <li><strong>Finalidade:</strong> {self.compliance_data['identificacao_modelo']['finalidade']}</li>
                <li><strong>Data de Validação:</strong> {self.compliance_data['identificacao_modelo']['data_validacao']}</li>
            </ul>

            <h3>2. Avaliação de Risco do Modelo</h3>
            <div style="padding: 15px; background-color: white; border-left: 4px solid {risk_color}; margin: 10px 0;">
                <p style="margin: 0;"><strong>Nível de Risco:</strong>
                    <span style="color: {risk_color}; font-weight: bold; font-size: 1.2em;">
                        {self.compliance_data['risco_modelo']['nivel_risco']}
                    </span>
                </p>
                <p style="margin: 5px 0 0 0;">{self.compliance_data['risco_modelo']['descricao']}</p>
            </div>
            <ul>
                <li><strong>Total de Disparidades:</strong> {self.compliance_data['risco_modelo']['total_disparidades']}</li>
                <li><strong>Alta Severidade:</strong> {self.compliance_data['risco_modelo']['disparidades_alta_severidade']}</li>
                <li><strong>Média Severidade:</strong> {self.compliance_data['risco_modelo']['disparidades_media_severidade']}</li>
                <li><strong>Requer Ação Imediata:</strong> {'Sim' if self.compliance_data['risco_modelo']['requer_acao_imediata'] else 'Não'}</li>
            </ul>
        """

        # Add disparities if any
        disparities = self.compliance_data["fairness_assessment"][
            "disparidades_identificadas"
        ]
        if disparities:
            html += "<h3>⚠️ Disparidades Identificadas</h3><ul>"
            for disp in disparities:
                html += f"""
                    <li><strong>{disp['atributo']} - {disp['grupo']}:</strong>
                        {disp['metrica']} = {disp['valor']:.3f}
                        (Desvio: {disp['desvio']:.3f}, Severidade: {disp['severidade']})
                    </li>
                """
            html += "</ul>"

        # Add mitigation actions
        html += "<h3>3. Ações de Mitigação Recomendadas</h3><ul>"
        for action in self.compliance_data["fairness_assessment"]["ações_mitigacao"]:
            html += f"<li>{action}</li>"
        html += "</ul>"

        # Add governance recommendations
        html += "<h3>4. Recomendações de Governança</h3><ul>"
        for rec in self.compliance_data["recomendacoes"]:
            html += f"<li>{rec}</li>"
        html += "</ul>"

        html += """
            <hr>
            <p style="font-size: 0.9em; color: #666;">
                <strong>Base Legal:</strong> Resolução BACEN nº 4.658/2018<br>
                Este relatório documenta a gestão de risco de modelo conforme exigido pelo Banco Central do Brasil.
            </p>
        </div>
        """

        return html

    def to_dict(self) -> dict[str, Any]:
        """
        Export compliance data as dictionary.

        Returns:
            Dictionary with all compliance data

        Example:
            >>> compliance_dict = bacen_reporter.to_dict()
            >>> import json
            >>> json.dump(compliance_dict, open('bacen_compliance.json', 'w'))
        """
        if not self.compliance_data:
            self.generate_report()

        return self.compliance_data
