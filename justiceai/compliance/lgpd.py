"""
LGPD Compliance Reporter.

This module provides compliance reporting according to Brazilian LGPD
(Lei Geral de Proteção de Dados - Art. 20) for algorithmic transparency.

The LGPD Article 20 requires:
- Transparency about automated decision-making
- Explanation of decisions and criteria used
- Assessment of fairness and bias in models
"""

from typing import Any

import pandas as pd

from justiceai.reports.fairness_report import FairnessReport


class LGPDComplianceReporter:
    """
    LGPD Compliance Reporter for algorithmic transparency.

    This reporter generates documentation according to LGPD Art. 20,
    which mandates transparency in automated decision-making systems.

    Key requirements addressed:
        - Right to explanation (direito à explicação)
        - Transparency of automated decisions
        - Fairness and bias assessment
        - Documentation in Portuguese (BR)

    Example:
        >>> from justiceai import audit
        >>> from justiceai.compliance import LGPDComplianceReporter
        >>>
        >>> # Run fairness audit
        >>> report = audit(model, data, protected_attrs=['gender'])
        >>>
        >>> # Generate LGPD compliance report
        >>> lgpd_reporter = LGPDComplianceReporter(report)
        >>> compliance_doc = lgpd_reporter.generate_report()
        >>> lgpd_reporter.save_html("lgpd_compliance.html")

    References:
        LGPD Art. 20: https://www.planalto.gov.br/ccivil_03/_ato2015-2018/2018/lei/l13709.htm
    """

    def __init__(self, fairness_report: FairnessReport):
        """
        Initialize LGPD Compliance Reporter.

        Args:
            fairness_report: FairnessReport instance with fairness analysis
        """
        self.fairness_report = fairness_report
        self.compliance_data: dict[str, Any] = {}

    def generate_report(self) -> dict[str, Any]:
        """
        Generate LGPD compliance report.

        Returns:
            Dictionary with compliance documentation sections:
                - transparencia_algoritmica: Algorithmic transparency info
                - criterios_decisao: Decision criteria used
                - avaliacao_fairness: Fairness assessment
                - grupos_protegidos: Protected groups analyzed
                - metricas_bias: Bias metrics summary
                - recomendacoes: Recommendations for compliance

        Example:
            >>> compliance_doc = lgpd_reporter.generate_report()
            >>> print(compliance_doc['transparencia_algoritmica']['objetivo'])
            'Sistema de apoio à decisão usando Machine Learning...'
        """
        # Extract data from fairness report
        summary = self.fairness_report.get_summary()
        issues = self.fairness_report.get_issues()

        # Get metrics data
        metrics_data = self.fairness_report.metrics

        # 1. Transparência Algorítmica
        self.compliance_data["transparencia_algoritmica"] = {
            "objetivo": (
                "Sistema de apoio à decisão usando Machine Learning "
                "para classificação binária."
            ),
            "tipo_modelo": "Classificador Binário",
            "atributos_protegidos": list(summary.get("by_group", {}).keys()) if summary else [],
            "grupos_analisados": summary.get("by_group", {}) if summary else {},
            "data_avaliacao": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        # 2. Critérios de Decisão
        self.compliance_data["criterios_decisao"] = {
            "metricas_performance": summary.get("overall", {}) if summary else {},
            "metricas_fairness": summary.get("by_group", {}) if summary else {},
            "threshold_decisao": 0.5,
        }

        # 3. Avaliação de Fairness
        num_issues = len(issues) if issues else 0
        self.compliance_data["avaliacao_fairness"] = {
            "metricas_calculadas": list(metrics_data.keys()) if metrics_data else [],
            "total_metricas": len(metrics_data) if metrics_data else 0,
            "grupos_comparados": list(summary.get("by_group", {}).keys()) if summary else [],
            "disparidades_identificadas": issues if issues else [],
        }

        # 4. Grupos Protegidos
        self.compliance_data["grupos_protegidos"] = summary.get("by_group", {}) if summary else {}

        # 5. Métricas de Bias
        self.compliance_data["metricas_bias"] = {
            "total_atributos_protegidos": len(summary.get("by_group", {})) if summary else 0,
            "total_disparidades": num_issues,
            "metricas_por_atributo": summary.get("by_group", {}) if summary else {},
        }

        # 6. Recomendações
        self.compliance_data["recomendacoes"] = self._generate_recommendations(num_issues)

        return self.compliance_data

    def _generate_recommendations(self, num_issues: int) -> list[str]:
        """Generate compliance recommendations."""
        recommendations = [
            "Documentar e revisar periodicamente as métricas de fairness do modelo.",
            "Manter registro de todas as avaliações de fairness para auditoria.",
            (
                "Garantir que os titulares dos dados tenham acesso às "
                "informações sobre decisões automatizadas (LGPD Art. 20)."
            ),
        ]

        if num_issues > 0:
            recommendations.append(
                f"ATENÇÃO: {num_issues} problema(s) de fairness identificado(s). "
                "Considerar intervenções de mitigação de viés."
            )
            recommendations.append(
                "Revisar o modelo e os dados de treinamento para "
                "reduzir disparidades identificadas."
            )
        else:
            recommendations.append(
                "Nenhuma disparidade crítica identificada. "
                "Continuar monitoramento contínuo."
            )

        recommendations.append(
            "Implementar sistema de monitoramento contínuo para detectar "
            "drift nas métricas de fairness."
        )

        return recommendations

    def save_html(self, output_path: str) -> None:
        """
        Save LGPD compliance report as HTML file.

        Args:
            output_path: Path to save HTML file

        Example:
            >>> lgpd_reporter.save_html("compliance/lgpd_report.html")
        """
        if not self.compliance_data:
            self.generate_report()

        # Use the fairness report HTML as base and add compliance section
        html_content = self._generate_html()

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(html_content)

    def _generate_html(self) -> str:
        """Generate HTML content for LGPD compliance report."""
        # Start with fairness report HTML
        base_html = self.fairness_report.render_html()

        # Add LGPD compliance section
        compliance_section = self._create_compliance_section_html()

        # Insert compliance section before closing body tag
        html_with_compliance = base_html.replace(
            "</body>", f"{compliance_section}</body>"
        )

        return html_with_compliance

    def _create_compliance_section_html(self) -> str:
        """Create HTML section for LGPD compliance."""
        if not self.compliance_data:
            self.generate_report()

        html = """
        <div style="margin-top: 40px; padding: 20px; background-color: #f8f9fa; border-left: 4px solid #0066cc;">
            <h2>📋 Relatório de Conformidade LGPD</h2>
            <p><strong>Lei Geral de Proteção de Dados - Art. 20</strong></p>
            <p><em>Direito à Explicação e Transparência Algorítmica</em></p>

            <h3>1. Transparência Algorítmica</h3>
            <ul>
        """

        trans = self.compliance_data["transparencia_algoritmica"]
        html += f"""
                <li><strong>Objetivo:</strong> {trans['objetivo']}</li>
                <li><strong>Tipo de Modelo:</strong> {trans['tipo_modelo']}</li>
                <li><strong>Atributos Protegidos:</strong> {', '.join(trans['atributos_protegidos'])}</li>
                <li><strong>Data da Avaliação:</strong> {trans['data_avaliacao']}</li>
            </ul>

            <h3>2. Avaliação de Fairness</h3>
            <ul>
                <li><strong>Total de Métricas Calculadas:</strong> {self.compliance_data['avaliacao_fairness']['total_metricas']}</li>
                <li><strong>Grupos Comparados:</strong> {', '.join(self.compliance_data['avaliacao_fairness']['grupos_comparados'])}</li>
            </ul>
        """

        # Add disparities if any
        disparities = self.compliance_data["avaliacao_fairness"][
            "disparidades_identificadas"
        ]
        if disparities:
            html += "<h3>⚠️ Disparidades Identificadas</h3><ul>"
            for disp in disparities:
                html += f"""
                    <li><strong>{disp['atributo']} - {disp['grupo']}:</strong>
                        {disp['metrica']} = {disp['valor']:.3f}
                        (Threshold: {disp['threshold']}, Severidade: {disp['severidade']})
                    </li>
                """
            html += "</ul>"

        # Add recommendations
        html += "<h3>3. Recomendações de Conformidade</h3><ul>"
        for rec in self.compliance_data["recomendacoes"]:
            html += f"<li>{rec}</li>"
        html += "</ul>"

        html += """
            <hr>
            <p style="font-size: 0.9em; color: #666;">
                <strong>Base Legal:</strong> Lei nº 13.709/2018 (LGPD) - Artigo 20<br>
                Este relatório documenta a transparência algorítmica conforme exigido pela legislação brasileira.
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
            >>> compliance_dict = lgpd_reporter.to_dict()
            >>> import json
            >>> json.dump(compliance_dict, open('compliance.json', 'w'))
        """
        if not self.compliance_data:
            self.generate_report()

        return self.compliance_data
