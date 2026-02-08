# 🎨 SPRINT 3: API Pública + Docs

**Período**: Semanas 7-8 (22 Mar - 5 Abr 2026)
**Objetivo**: API simples e documentação completa
**Capacity**: 80 horas

---

## 📋 Objetivos

### Objetivo Principal
Criar API pública intuitiva e documentação completa

### Entregáveis
1. Model adapters (sklearn, XGBoost, LightGBM, ONNX)
2. FairnessEvaluator (main API)
3. API de conveniência `audit()`
4. Documentação com MkDocs
5. Jupyter notebooks tutorial
6. Docstrings completas

---

## User Stories

### 🎯 US-019: Model Adapters
**Estimativa**: 14 horas

Framework-agnostic support:
- SklearnAdapter
- XGBoostAdapter
- LightGBMAdapter
- ONNXAdapter
- Auto-detection factory

### 🎯 US-020: FairnessEvaluator (Main API)
**Estimativa**: 12 horas

```python
from justiceai import FairnessEvaluator

evaluator = FairnessEvaluator()
result = evaluator.evaluate(model, data, protected_attrs=['gender'])
```

### 🎯 US-021: API de Conveniência `audit()`
**Estimativa**: 6 horas

API 1-liner:
```python
from justiceai import audit

report = audit(model, data, protected_attrs=['gender'])
report.show()
```

### 🎯 US-022: Documentação com MkDocs
**Estimativa**: 16 horas

Estrutura:
- Getting Started
- API Reference (auto-gerado)
- Tutorials
- FAQ
- Deploy em GitHub Pages

### 🎯 US-023: Jupyter Notebooks Tutorial
**Estimativa**: 10 horas

Notebooks:
- 01_quickstart.ipynb
- 02_advanced_metrics.ipynb
- 03_reports_customization.ipynb

### 🎯 US-024: Docstrings Completas
**Estimativa**: 12 horas

- Google-style docstrings
- 100% APIs públicas
- Exemplos em docstrings críticas

---

## Entregáveis

- ✅ API pública simples
- ✅ Suporte múltiplos frameworks
- ✅ Docs completas (MkDocs)
- ✅ 3 tutoriais Jupyter

**Status**: ⏳ TODO
**Sprint Anterior**: Sprint 2 (Reports HTML)
**Próxima Sprint**: Sprint 4 (Compliance + Monitoring)
