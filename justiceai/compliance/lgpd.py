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
        result = self.fairness_report.fairness_result

        # 1. Transparência Algorítmica
        self.compliance_data["transparencia_algoritmica"] = {
            "objetivo": (
                "Sistema de apoio à decisão usando Machine Learning "
                "para classificação binária."
            ),
            "tipo_modelo": self._get_model_type(),
            "atributos_protegidos": result.protected_attrs,
            "grupos_analisados": self._get_analyzed_groups(),
            "data_avaliacao": pd.Timestamp.now().strftime("%Y-%m-%d %H:%M:%S"),
        }

        # 2. Critérios de Decisão
        self.compliance_data["criterios_decisao"] = {
            "metricas_performance": self._get_performance_metrics(),
            "metricas_fairness": self._get_fairness_metrics_summary(),
            "threshold_decisao": getattr(result, "threshold", 0.5),
        }

        # 3. Avaliação de Fairness
        self.compliance_data["avaliacao_fairness"] = {
            "metricas_calculadas": list(result.metrics.keys()),
            "total_metricas": len(result.metrics),
            "grupos_comparados": self._get_group_comparisons(),
            "disparidades_identificadas": self._identify_disparities(),
        }

        # 4. Grupos Protegidos
        self.compliance_data["grupos_protegidos"] = self._analyze_protected_groups()

        # 5. Métricas de Bias
        self.compliance_data["metricas_bias"] = self._summarize_bias_metrics()

        # 6. Recomendações
        self.compliance_data["recomendacoes"] = self._generate_recommendations()

        return self.compliance_data

    def _get_model_type(self) -> str:
        """Get model type description."""
        result = self.fairness_report.fairness_result
        if hasattr(result, "model"):
            return type(result.model).__name__
        return "Classificador Binário"

    def _get_analyzed_groups(self) -> dict[str, list[str]]:
        """Get list of analyzed groups per protected attribute."""
        result = self.fairness_report.fairness_result
        groups = {}

        for attr in result.protected_attrs:
            if attr in result.metrics:
                groups[attr] = list(result.metrics[attr].keys())

        return groups

    def _get_performance_metrics(self) -> dict[str, float]:
        """Get overall performance metrics."""
        result = self.fairness_report.fairness_result
        metrics = {}

        # Try to extract overall metrics if available
        if hasattr(result, "overall_metrics"):
            metrics = result.overall_metrics

        return metrics

    def _get_fairness_metrics_summary(self) -> dict[str, dict[str, float]]:
        """Get summary of fairness metrics per protected attribute."""
        result = self.fairness_report.fairness_result
        summary = {}

        for attr in result.protected_attrs:
            if attr in result.metrics:
                attr_metrics = {}
                for group, group_metrics in result.metrics[attr].items():
                    # Get key fairness metrics
                    if "statistical_parity" in group_metrics:
                        attr_metrics[f"{group}_statistical_parity"] = group_metrics[
                            "statistical_parity"
                        ]
                    if "equal_opportunity" in group_metrics:
                        attr_metrics[f"{group}_equal_opportunity"] = group_metrics[
                            "equal_opportunity"
                        ]

                summary[attr] = attr_metrics

        return summary

    def _get_group_comparisons(self) -> list[str]:
        """Get list of group comparisons performed."""
        result = self.fairness_report.fairness_result
        comparisons = []

        for attr in result.protected_attrs:
            if attr in result.metrics:
                groups = list(result.metrics[attr].keys())
                comparisons.append(f"{attr}: {' vs '.join(groups)}")

        return comparisons

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
                                    "severidade": "Alta"
                                    if sp_ratio < 0.6
                                    else "Média",
                                }
                            )

        return disparities

    def _analyze_protected_groups(self) -> dict[str, dict[str, Any]]:
        """Analyze protected groups in detail."""
        result = self.fairness_report.fairness_result
        groups_analysis = {}

        for attr in result.protected_attrs:
            if attr in result.metrics:
                groups_analysis[attr] = {}
                for group, group_metrics in result.metrics[attr].items():
                    groups_analysis[attr][group] = {
                        "metricas_disponiveis": list(group_metrics.keys()),
                        "total_metricas": len(group_metrics),
                        "principais_metricas": {
                            k: v
                            for k, v in group_metrics.items()
                            if k
                            in [
                                "statistical_parity",
                                "equal_opportunity",
                                "predictive_parity",
                            ]
                        },
                    }

        return groups_analysis

    def _summarize_bias_metrics(self) -> dict[str, Any]:
        """Summarize bias metrics across all groups."""
        result = self.fairness_report.fairness_result
        summary = {
            "total_atributos_protegidos": len(result.protected_attrs),
            "total_grupos_analisados": 0,
            "metricas_por_atributo": {},
        }

        for attr in result.protected_attrs:
            if attr in result.metrics:
                num_groups = len(result.metrics[attr])
                summary["total_grupos_analisados"] += num_groups
                summary["metricas_por_atributo"][attr] = {
                    "grupos": num_groups,
                    "metricas_calculadas": len(
                        next(iter(result.metrics[attr].values()), {})
                    ),
                }

        return summary

    def _generate_recommendations(self) -> list[str]:
        """Generate compliance recommendations."""
        disparities = self._identify_disparities()

        recommendations = [
            "Documentar e revisar periodicamente as métricas de fairness do modelo.",
            "Manter registro de todas as avaliações de fairness para auditoria.",
            (
                "Garantir que os titulares dos dados tenham acesso às "
                "informações sobre decisões automatizadas (LGPD Art. 20)."
            ),
        ]

        if disparities:
            recommendations.append(
                f"ATENÇÃO: {len(disparities)} disparidade(s) identificada(s). "
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
        base_html = self.fairness_report.to_html()

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
