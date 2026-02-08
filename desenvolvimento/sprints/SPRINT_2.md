# 📊 SPRINT 2: Reports HTML

**Período**: Semanas 5-6 (8-22 Mar 2026)
**Objetivo**: Sistema de relatórios standalone com Plotly
**Capacity**: 80 horas

---

## 📋 Objetivos

### Objetivo Principal
Criar sistema completo de geração de reports HTML interativos

### Entregáveis
1. Data transformer para preparar dados
2. Chart factory com Plotly
3. Template HTML profissional
4. HTML renderer
5. Report builder (facade)
6. Exemplos de reports

---

## User Stories

### 🎯 US-013: Data Transformer para Reports
**Estimativa**: 10 horas | **Referência**: DeepBridge `transformers/fairness/data_transformer.py`

### 🎯 US-014: Chart Factory com Plotly
**Estimativa**: 16 horas | **Referência**: DeepBridge `charts/posttrain_charts.py`

Gráficos a implementar:
- Disparate Impact por grupo
- Statistical Parity comparison
- Confusion Matrix heatmap
- Threshold analysis curve
- Overall fairness score gauge

### 🎯 US-015: Template HTML Jinja2
**Estimativa**: 12 horas | **Referência**: DeepBridge `templates/report_types/fairness/`

Seções do report:
- Executive Summary
- Metrics Overview
- Interactive Charts
- Critical Issues & Warnings
- Recommendations

### 🎯 US-016: HTML Renderer
**Estimativa**: 8 horas

### 🎯 US-017: Report Builder (Facade)
**Estimativa**: 10 horas

API final:
```python
from justiceai.reports import FairnessReport

report = FairnessReport.from_metrics(metrics)
report.save_html('report.html')
report.show()  # Abre no navegador
```

### 🎯 US-018: Exemplos de Reports
**Estimativa**: 8 horas

Datasets:
- Breast Cancer (simples)
- Adult Income (complexo)
- COMPAS (real-world)

---

## Entregáveis

- ✅ Sistema completo de reports
- ✅ Plotly charts interativos
- ✅ HTML standalone (< 5MB)
- ✅ 3 exemplos prontos

**Status**: ⏳ TODO
**Sprint Anterior**: Sprint 1 (Métricas Core)
**Próxima Sprint**: Sprint 3 (API Pública + Docs)
