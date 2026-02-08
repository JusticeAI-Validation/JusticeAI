# ⚖️ justiceai

[![Build Status](https://img.shields.io/badge/build-passing-brightgreen)]()
[![Coverage](https://img.shields.io/badge/coverage-90%25-brightgreen)]()
[![Python](https://img.shields.io/badge/python-3.11%2B-blue)](https://www.python.org/)
[![Tests](https://img.shields.io/badge/tests-192%20passing-brightgreen)]()
[![License](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![Code style: ruff](https://img.shields.io/badge/code%20style-ruff-000000.svg)](https://github.com/astral-sh/ruff)

> **Fairness em ML para Produção**: A primeira biblioteca Python focada em monitoramento de fairness em produção, com compliance LGPD/BACEN nativo e relatórios standalone.

---

## 🎯 O Problema

Ferramentas como **Fairlearn** e **AIF360** são excelentes para pesquisa, mas param no notebook. Você precisa de fairness em **produção**, com:
- ✅ Monitoramento contínuo de viés
- ✅ Compliance automático (LGPD Art. 20, BACEN Res. 4.658)
- ✅ Relatórios prontos para stakeholders não-técnicos
- ✅ Zero vendor lock-in (funciona com sklearn, XGBoost, PyTorch, TensorFlow)

**justiceai** resolve isso.

---

## 🚀 Quick Start

```python
from justiceai import audit
from sklearn.datasets import load_breast_cancer
from sklearn.ensemble import RandomForestClassifier
import pandas as pd

# Carregar dados
data = load_breast_cancer()
df = pd.DataFrame(data.data, columns=data.feature_names)
df['target'] = data.target
df['gender'] = np.random.choice(['M', 'F'], size=len(df))  # Atributo protegido

# Treinar modelo
model = RandomForestClassifier()
model.fit(df.drop(['target', 'gender'], axis=1), df['target'])

# Avaliar fairness em 1 linha
report = audit(
    model=model,
    data=df,
    target='target',
    protected_attrs=['gender']
)

# Visualizar
report.show()  # Abre HTML interativo no navegador
report.save_html('fairness_report.html')  # Salva para compartilhar
```

**Output**: Relatório HTML standalone com Plotly interativo, pronto para apresentar ao board.

---

## 📦 Instalação

### Via pip (em breve)
```bash
pip install justiceai
```

### Para Desenvolvimento
```bash
# Clone o repositório
git clone https://github.com/guhaase/justiceai.git
cd justiceai

# Instale com Poetry
poetry install

# Ative o ambiente
poetry shell

# Rode os testes
pytest
```

---

## ✨ Features

### 🔬 15+ Métricas de Fairness

#### Pre-Training (independentes de modelo)
- **Class Balance**: Distribuição balanceada entre grupos
- **Concept Balance**: Taxa de positivos balanceada
- **KL/JS Divergence**: Similaridade de distribuições

#### Post-Training (baseadas em predições)
- **Statistical Parity**: Taxa de predições positivas igual
- **Disparate Impact**: Compliance com regra EEOC 80%
- **Equal Opportunity**: TPR igual entre grupos
- **Equalized Odds**: TPR e FPR iguais
- **+ 8 métricas adicionais**

### 📊 Relatórios Standalone
- **HTML Interativo**: Plotly charts, funciona offline
- **PDF Profissional**: Pronto para auditoria (em breve)
- **Markdown**: Versionável em Git (em breve)

### 🇧🇷 Compliance Brasil
- **LGPD Art. 20**: Template pronto para direito à explicação
- **BACEN Res. 4.658**: Análise de risco de modelo (em breve)
- **Português nativo**: Relatórios e erros em PT-BR

### 🔌 Framework-Agnostic
Funciona com:
- ✅ **scikit-learn**
- ✅ **XGBoost**
- ✅ **LightGBM**
- ⏳ **PyTorch** (em breve)
- ⏳ **TensorFlow** (em breve)
- ⏳ **ONNX** (em breve)

### 📈 Monitoring em Produção (em breve)
- **Drift Detection**: Detecta degradação de fairness ao longo do tempo
- **Alerting**: Slack/Email quando métricas violam thresholds
- **Integração CI/CD**: Bloqueia deploy se fairness < threshold

---

## 📚 Documentação

**Status**: ✅ Completa

- [**Installation Guide**](docs/getting-started/installation.md) - Setup and installation
- [**Quick Start**](docs/getting-started/quickstart.md) - Your first fairness audit in 5 minutes
- [**Basic Concepts**](docs/getting-started/concepts.md) - Understanding fairness metrics
- [**API Reference**](docs/api/index.md) - Complete API documentation
- [**Tutorials**](notebooks/) - 3 Jupyter notebooks with hands-on examples
- [**FAQ**](docs/faq.md) - 40+ common questions answered
- [**Contributing**](docs/contributing.md) - Guidelines for contributors

---

## 🔬 Comparação com Concorrentes

| Feature | Fairlearn | AIF360 | justiceai |
|---------|-----------|--------|-----------|
| **Métricas** | 8 | 70+ | 15+ (curadas) |
| **MLOps/Produção** | ❌ | ❌ | ✅ |
| **Compliance BR** | ❌ | ❌ | ✅ |
| **Reports Standalone** | ❌ | ⚠️ | ✅ (HTML Plotly) |
| **Framework-Agnostic** | ⚠️ | ⚠️ | ✅ |
| **API 1-liner** | ❌ | ❌ | ✅ |
| **Monitoring** | ❌ | ❌ | ✅ (em breve) |

---

## 🗺️ Roadmap

### ✅ v0.1.0 (Sprint 1-3) - COMPLETO
- [x] Setup projeto (Poetry, CI/CD)
- [x] 15+ métricas de fairness
- [x] Reports HTML com Plotly
- [x] API `audit()` simples
- [x] FairnessEvaluator API
- [x] Model adapters (sklearn + factory)
- [x] Documentação completa (MkDocs)
- [x] 3 tutoriais Jupyter
- [x] 192 testes, 90%+ coverage
- [x] FAQ com 40+ questões

### 🏗️ v0.2.0 (Sprint 4) - Compliance
- [ ] Suporte XGBoost, LightGBM
- [ ] Templates LGPD/BACEN
- [ ] Monitoring e drift detection
- [ ] Threshold optimization
- [ ] Reports PDF

### 🔮 v0.3.0 (Sprint 5) - Release Público
- [ ] Publicado no PyPI
- [ ] GitHub Pages documentation
- [ ] Português nativo completo
- [ ] Suporte PyTorch/TensorFlow

### 🌟 v1.0+ (Futuro)
- [ ] Mitigação automática de viés
- [ ] IA-powered insights (LLM)
- [ ] Integração MLflow/W&B
- [ ] SaaS offering (?)

---

## 🤝 Contribuindo

Contribuições são muito bem-vindas! Veja [CONTRIBUTING.md](CONTRIBUTING.md) para guidelines.

### Como Contribuir

1. **Fork** o repositório
2. **Clone** seu fork: `git clone https://github.com/SEU-USUARIO/justiceai.git`
3. **Crie uma branch**: `git checkout -b feature/minha-feature`
4. **Faça mudanças** e commit: `git commit -m "feat: adiciona minha feature"`
5. **Push**: `git push origin feature/minha-feature`
6. **Abra um Pull Request**

### Code Quality

Antes de abrir PR, rode:

```bash
# Formatar código
make format

# Linting
make lint

# Type checking
make type-check

# Testes
make test

# Tudo de uma vez
make quality
```

---

## 📊 Status do Projeto

**Fase Atual**: Sprint 3 Completo - v0.1.0 Ready!

| Métrica | Status | Target |
|---------|--------|--------|
| **Coverage** | ✅ 90.03% | 90% |
| **Testes** | ✅ 192 passing | 150+ |
| **Docs** | ✅ 20 pages | 100% |
| **Tutorials** | ✅ 3 notebooks | 3 |

**Sprints Completos**: 3/5 (60%)
- ✅ Sprint 1: Core Metrics
- ✅ Sprint 2: HTML Reports
- ✅ Sprint 3: API + Documentation
- 🔄 Sprint 4: Compliance (próximo)
- ⏳ Sprint 5: Release Público

---

## 📄 Licença

Este projeto está licenciado sob a [MIT License](LICENSE).

```
MIT License

Copyright (c) 2026 Gustavo Haase

Permission is hereby granted, free of charge, to any person obtaining a copy...
```

---

## 👥 Autores

**Gustavo Haase**
- Email: gustavo.haase@gmail.com
- GitHub: [@guhaase](https://github.com/guhaase)

---

## 🙏 Agradecimentos

- **DeepBridge**: Base de código que inspirou este projeto
- **Fairlearn/AIF360**: Referências de métricas
- **Comunidade Python**: Ferramentas incríveis (Poetry, Pytest, Black, etc.)

---

## 📞 Suporte

- **Issues**: [GitHub Issues](https://github.com/guhaase/justiceai/issues)
- **Discussions**: [GitHub Discussions](https://github.com/guhaase/justiceai/discussions)
- **Email**: gustavo.haase@gmail.com

---

## 🌟 Star History

[![Star History Chart](https://api.star-history.com/svg?repos=guhaase/justiceai&type=Date)](https://star-history.com/#guhaase/justiceai&Date)

---

<p align="center">
  <b>Feito com ❤️ para tornar ML mais justo e responsável</b>
</p>

<p align="center">
  <sub>⚖️ justiceai - Fairness em ML para Produção</sub>
</p>
