# 📋 Planejamento Ágil - justiceai

**Projeto**: justiceai - Biblioteca Python para Análise de Fairness em ML
**Versão do Documento**: 1.0
**Data**: 2026-02-08
**Metodologia**: Scrum/Agile
**Duração Total Estimada**: 12 semanas (3 meses)

---

## 📑 Índice

1. [Visão Geral do Projeto](#1-visão-geral-do-projeto)
2. [Product Vision](#2-product-vision)
3. [Stakeholders](#3-stakeholders)
4. [Definição de Pronto (DoD)](#4-definição-de-pronto-dod)
5. [Arquitetura e Stack Tecnológico](#5-arquitetura-e-stack-tecnológico)
6. [Product Backlog](#6-product-backlog)
7. [Sprints Detalhadas](#7-sprints-detalhadas)
8. [Métricas de Qualidade](#8-métricas-de-qualidade)
9. [Riscos e Mitigações](#9-riscos-e-mitigações)
10. [Cronograma Visual](#10-cronograma-visual)

---

## 1. Visão Geral do Projeto

### 1.1. Descrição

**justiceai** é uma biblioteca Python open-source focada em análise de fairness (justiça) em modelos de Machine Learning, com foco especial em:

- **Produção-first**: Monitoramento contínuo de fairness em modelos deployados
- **Compliance Brasil/LATAM**: Adequação à LGPD, BACEN, CDC
- **Developer Experience**: API simples e intuitiva
- **Reports standalone**: Relatórios HTML autônomos com Plotly interativo
- **Framework-agnostic**: Suporte a sklearn, XGBoost, PyTorch, TensorFlow, ONNX

### 1.2. Objetivos de Negócio

1. **Mercado**: Preencher gap de ferramentas de fairness voltadas para produção
2. **Diferenciação**: Única biblioteca com foco em regulação brasileira/LATAM
3. **Adoção**: 500+ instalações no primeiro mês pós-lançamento
4. **Qualidade**: Code coverage ≥ 90%, Zero bugs críticos

### 1.3. Métricas de Sucesso (KPIs)

| Métrica | Target MVP | Target 3 meses |
|---------|-----------|----------------|
| **Downloads PyPI** | 100+ | 500+ |
| **Stars GitHub** | 50+ | 200+ |
| **Code Coverage** | ≥ 90% | ≥ 95% |
| **Documentação** | 100% APIs públicas | + Tutoriais |
| **Issues abertas** | < 5 | < 10 |
| **Tempo resposta issues** | < 48h | < 24h |

---

## 2. Product Vision

### 2.1. Elevator Pitch

> "**justiceai** é a primeira biblioteca Python de fairness em ML projetada para produção, oferecendo monitoramento contínuo, compliance LGPD/BACEN e relatórios standalone em HTML. Onde Fairlearn e AIF360 param no notebook, justiceai começa."

### 2.2. Canvas do Produto

```
┌─────────────────────────────────────────────────────────────┐
│                     JUSTICEAI CANVAS                        │
├──────────────────────┬──────────────────────────────────────┤
│ PROBLEMA             │ SOLUÇÃO                              │
│ • Fairness tools     │ • API simples (1-liner)              │
│   são acadêmicas     │ • Monitoring em produção             │
│ • Lock-in frameworks │ • Framework-agnostic                 │
│ • Zero compliance BR │ • Templates LGPD/BACEN               │
│ • Reports complexos  │ • HTML standalone c/ Plotly          │
├──────────────────────┼──────────────────────────────────────┤
│ USUÁRIOS             │ PROPOSTA VALOR                       │
│ • ML Engineers       │ • Fairness que vai pra produção      │
│ • Data Scientists    │ • Compliance automático              │
│ • Fintechs BR        │ • Reports prontos p/ stakeholders    │
│ • Auditores          │ • 10x mais rápido que concorrentes   │
├──────────────────────┼──────────────────────────────────────┤
│ VANTAGEM COMPETITIVA │ MÉTRICAS CHAVE                       │
│ • MLOps-first        │ • Downloads: 500+/mês                │
│ • Regulação BR       │ • Coverage: 95%+                     │
│ • DX superior        │ • Stars: 200+                        │
│ • Plotly reports     │ • NPS: 8+                            │
└──────────────────────┴──────────────────────────────────────┘
```

---

## 3. Stakeholders

| Papel | Nome/Grupo | Responsabilidades | Expectativas |
|-------|------------|-------------------|--------------|
| **Product Owner** | Gustavo Haase | Priorização backlog, aceite stories | Produto alinhado com visão |
| **Scrum Master** | [TBD] | Facilitar sprints, remover impedimentos | Velocidade constante |
| **Dev Team** | Time DeepBridge | Desenvolver features, testes, docs | Código de alta qualidade |
| **Early Adopters** | Fintechs BR | Validar features, feedback | Resolva meus problemas |
| **Open Source Community** | GitHub users | Contribuições, issues | Código limpo, docs claras |

---

## 4. Definição de Pronto (DoD)

### 4.1. DoD - User Story

Uma user story está "Pronta" quando:

- [ ] **Código**: Implementado e revisado (PR aprovado)
- [ ] **Testes**: Coverage ≥ 90% para código novo
- [ ] **Type Hints**: 100% das funções públicas
- [ ] **Documentação**: Docstrings (Google style) em todas APIs públicas
- [ ] **Linting**: Zero warnings (black, ruff, mypy, pylint)
- [ ] **Integração**: Passa em CI/CD (todas versões Python 3.10-3.12)
- [ ] **Exemplos**: Pelo menos 1 exemplo de uso documentado
- [ ] **Aceite PO**: Product Owner validou funcionalidade

### 4.2. DoD - Sprint

Uma sprint está "Pronta" quando:

- [ ] Todas as stories comprometidas foram completadas (DoD)
- [ ] Regression tests passam 100%
- [ ] Documentação atualizada (README, CHANGELOG)
- [ ] Demo realizada (interno ou para early adopters)
- [ ] Retrospectiva realizada
- [ ] Backlog refinado para próxima sprint

### 4.3. DoD - Release

Uma release está "Pronta" quando:

- [ ] Todos os critérios de sprint cumpridos
- [ ] Publicado no PyPI
- [ ] Docs publicadas (GitHub Pages ou ReadTheDocs)
- [ ] Release notes criadas
- [ ] Tag Git criada (vX.Y.Z)
- [ ] Anúncio feito (blog, redes sociais)

---

## 5. Arquitetura e Stack Tecnológico

### 5.1. Stack Core

```python
# Gerenciamento de Dependências
poetry>=1.7.0

# Python
python = ">=3.10,<3.13"

# Core Dependencies
numpy>=1.24.0
pandas>=2.0.0
scikit-learn>=1.3.0
scipy>=1.11.0

# Visualização
plotly>=5.14.0
jinja2>=3.1.0

# Validação
pydantic>=2.0.0

# Qualidade de Código
black>=23.0
ruff>=0.1.0
mypy>=1.0
pylint>=3.0
isort>=5.12

# Testes
pytest>=7.0
pytest-cov>=4.0
pytest-asyncio>=0.21

# Build & Publish
build>=1.0
twine>=4.0

# Docs
mkdocs-material>=9.0
mkdocstrings-python>=1.0
```

### 5.2. Arquitetura de Módulos

```
justiceai/
├── core/                      # Core functionality
│   ├── metrics/              # Fairness metrics implementation
│   │   ├── pretrain.py       # Pre-training metrics
│   │   ├── posttrain.py      # Post-training metrics
│   │   └── calculator.py     # Metrics calculator
│   ├── evaluators/           # Model evaluators
│   │   ├── fairness.py       # Main fairness evaluator
│   │   └── threshold.py      # Threshold analysis
│   └── adapters/             # Model adapters (framework-agnostic)
│       ├── sklearn.py
│       ├── xgboost.py
│       ├── torch.py
│       └── onnx.py
├── monitoring/                # Production monitoring
│   ├── drift.py              # Fairness drift detection
│   └── alerting.py           # Alert system
├── reports/                   # Report generation
│   ├── transformers/         # Data transformers
│   ├── renderers/            # HTML/PDF renderers
│   └── templates/            # Jinja2 templates
├── compliance/                # Compliance frameworks
│   ├── lgpd.py               # LGPD compliance
│   └── bacen.py              # BACEN compliance
└── utils/                     # Utilities
    ├── validators.py
    └── helpers.py
```

### 5.3. Princípios de Design

1. **SOLID**: Cada classe tem responsabilidade única
2. **DRY**: Evitar duplicação (herança, composição)
3. **Type Safety**: Type hints em 100% código público
4. **Testability**: Mock-friendly, injeção de dependência
5. **Extensibility**: Plugins, adapters, estratégias

---

## 6. Product Backlog

### 6.1. Épicos

| ID | Épico | Descrição | Prioridade | Estimativa |
|----|-------|-----------|------------|------------|
| **E1** | **Setup & Fundação** | Estrutura projeto, CI/CD, qualidade | MUST | 2 semanas |
| **E2** | **Métricas Core** | Implementar 15+ métricas fairness | MUST | 3 semanas |
| **E3** | **Reports HTML** | Sistema de relatórios standalone | MUST | 2 semanas |
| **E4** | **API Simplificada** | API pública 1-liner | MUST | 1 semana |
| **E5** | **Compliance Brasil** | Templates LGPD/BACEN | SHOULD | 2 semanas |
| **E6** | **Monitoring** | Drift detection, alerting | SHOULD | 1 semana |
| **E7** | **Docs & Exemplos** | Docs completas, tutoriais | MUST | 1 semana |

### 6.2. Backlog Priorizado (MoSCoW)

#### MUST HAVE (MVP)
1. Setup projeto com Poetry + CI/CD
2. 15 métricas de fairness (pre + post training)
3. Reports HTML standalone com Plotly
4. API simplificada `audit(model, data).show()`
5. Suporte sklearn, XGBoost, LightGBM
6. Documentação APIs públicas
7. Coverage ≥ 90%

#### SHOULD HAVE (v1.1)
8. Templates compliance LGPD/BACEN
9. Monitoring e drift detection
10. Suporte PyTorch, TensorFlow
11. Tutoriais e exemplos avançados

#### COULD HAVE (v1.2+)
12. Mitigação automática de viés
13. Análise de interseccionalidade
14. Integração com MLflow/Weights & Biases
15. IA-powered insights (LLM)

#### WON'T HAVE (fora escopo MVP)
16. GUI desktop
17. Serviço SaaS
18. Suporte R/Julia

---

## 7. Sprints Detalhadas

### 📅 Calendário de Sprints

| Sprint | Período | Épicos | Objetivo |
|--------|---------|--------|----------|
| **Sprint 0** | Sem 1-2 | E1 | Fundação sólida |
| **Sprint 1** | Sem 3-4 | E2 | Métricas core funcionando |
| **Sprint 2** | Sem 5-6 | E3 | Reports visuais |
| **Sprint 3** | Sem 7-8 | E4, E7 | API pública + docs |
| **Sprint 4** | Sem 9-10 | E5, E6 | Compliance + monitoring |
| **Sprint 5** | Sem 11-12 | - | Polish, release, marketing |

---

### 🚀 SPRINT 0: Fundação do Projeto (Semanas 1-2)

**Objetivo**: Criar estrutura profissional com máxima qualidade de código

**Capacity**: 80 horas (2 devs × 2 semanas × 20h/semana)

#### User Stories

##### US-001: Setup Projeto com Poetry
**Como** desenvolvedor
**Quero** um projeto Python configurado com Poetry
**Para** ter gerenciamento de dependências profissional

**Critérios de Aceite**:
- [ ] `pyproject.toml` configurado com todas dependências
- [ ] Poetry lock file gerado
- [ ] Comandos `poetry install` e `poetry shell` funcionando
- [ ] Estrutura de diretórios criada (conforme seção 5.2)
- [ ] `.gitignore` configurado
- [ ] README.md inicial criado

**Tarefas**:
- [ ] Instalar Poetry
- [ ] Executar `poetry init`
- [ ] Adicionar dependências core
- [ ] Criar estrutura de diretórios
- [ ] Inicializar Git

**Estimativa**: 4 horas
**Prioridade**: MUST
**DoD**: Projeto clonável e instalável via `poetry install`

---

##### US-002: CI/CD com GitHub Actions
**Como** desenvolvedor
**Quero** pipeline CI/CD automatizado
**Para** garantir qualidade em cada commit

**Critérios de Aceite**:
- [ ] Workflow de testes (`test.yml`)
- [ ] Workflow de linting (`quality.yml`)
- [ ] Workflow de build (`build.yml`)
- [ ] Badges no README (build, coverage, Python versions)
- [ ] Testes rodam em Python 3.10, 3.11, 3.12
- [ ] Coverage report enviado para Codecov

**Tarefas**:
- [ ] Criar `.github/workflows/test.yml`
- [ ] Criar `.github/workflows/quality.yml`
- [ ] Configurar Codecov
- [ ] Adicionar badges ao README
- [ ] Testar workflows

**Estimativa**: 6 horas
**Prioridade**: MUST
**DoD**: CI passa em todas PRs

---

##### US-003: Configurar Linters e Formatters
**Como** desenvolvedor
**Quero** ferramentas de qualidade configuradas
**Para** manter código consistente

**Critérios de Aceite**:
- [ ] Black configurado (line-length=88)
- [ ] Ruff configurado
- [ ] MyPy configurado (strict mode)
- [ ] Pylint configurado
- [ ] isort configurado
- [ ] Pre-commit hooks instalados
- [ ] Makefile com comandos `lint`, `format`, `test`

**Tarefas**:
- [ ] Adicionar configs em `pyproject.toml`
- [ ] Criar `.pre-commit-config.yaml`
- [ ] Criar `Makefile`
- [ ] Documentar em README
- [ ] Rodar em codebase inicial

**Estimativa**: 4 horas
**Prioridade**: MUST
**DoD**: `make lint` e `make format` funcionam

---

##### US-004: Setup de Testes com Pytest
**Como** desenvolvedor
**Quero** framework de testes configurado
**Para** escrever testes desde o início

**Critérios de Aceite**:
- [ ] Pytest instalado e configurado
- [ ] Pytest-cov configurado (target 90%)
- [ ] Estrutura `tests/` criada
- [ ] Fixtures básicos criados
- [ ] Teste dummy passando
- [ ] Coverage report funcionando

**Tarefas**:
- [ ] Adicionar pytest dependencies
- [ ] Configurar `[tool.pytest.ini_options]`
- [ ] Configurar `[tool.coverage]`
- [ ] Criar `tests/conftest.py`
- [ ] Criar `tests/test_dummy.py`
- [ ] Documentar como rodar testes

**Estimativa**: 4 horas
**Prioridade**: MUST
**DoD**: `pytest --cov` roda e gera relatório

---

##### US-005: Documentação Inicial
**Como** usuário
**Quero** documentação clara do projeto
**Para** entender como usar

**Critérios de Aceite**:
- [ ] README.md completo com:
  - [ ] Descrição do projeto
  - [ ] Badges (build, coverage, Python, license)
  - [ ] Quick start
  - [ ] Instalação
  - [ ] Exemplo básico
  - [ ] Contribuindo
  - [ ] Licença
- [ ] LICENSE criada (MIT)
- [ ] CHANGELOG.md iniciado
- [ ] CONTRIBUTING.md criado

**Tarefas**:
- [ ] Escrever README.md
- [ ] Escolher e adicionar LICENSE
- [ ] Criar CHANGELOG.md
- [ ] Criar CONTRIBUTING.md
- [ ] Revisar português/inglês

**Estimativa**: 6 horas
**Prioridade**: MUST
**DoD**: README renderiza bem no GitHub

---

##### US-006: Estrutura de Módulos Base
**Como** desenvolvedor
**Quero** módulos base criados
**Para** começar implementação

**Critérios de Aceite**:
- [ ] `justiceai/__init__.py` com `__version__`
- [ ] `justiceai/core/` criado
- [ ] `justiceai/core/metrics/` criado
- [ ] `justiceai/reports/` criado
- [ ] `justiceai/utils/` criado
- [ ] Todos `__init__.py` criados
- [ ] Imports funcionando

**Tarefas**:
- [ ] Criar estrutura de diretórios
- [ ] Criar `__init__.py` files
- [ ] Adicionar version string
- [ ] Testar imports básicos
- [ ] Atualizar `.gitignore`

**Estimativa**: 2 horas
**Prioridade**: MUST
**DoD**: `import justiceai` funciona

---

#### Sprint 0 - Resumo

**Total Story Points**: 26 horas
**Buffer**: 20% (5 horas para imprevistos)
**Disponível para pesquisa/estudo**: 49 horas

**Entregáveis**:
- ✅ Projeto estruturado com Poetry
- ✅ CI/CD completo
- ✅ Qualidade de código garantida
- ✅ Framework de testes pronto
- ✅ Documentação inicial

**Retrospectiva Points**:
- O que funcionou?
- O que melhorar?
- Velocidade real vs estimada?

---

### 🎯 SPRINT 1: Métricas Core (Semanas 3-4)

**Objetivo**: Implementar 15+ métricas de fairness

**Capacity**: 80 horas

#### User Stories

##### US-007: Métricas Pre-Training
**Como** data scientist
**Quero** métricas independentes de modelo
**Para** avaliar viés no dataset

**Critérios de Aceite**:
- [ ] Class Balance implementado
- [ ] Concept Balance implementado
- [ ] KL Divergence implementado
- [ ] JS Divergence implementado
- [ ] Testes unitários (coverage ≥ 95%)
- [ ] Docstrings completas
- [ ] Type hints em tudo

**Tarefas**:
- [ ] Criar `justiceai/core/metrics/pretrain.py`
- [ ] Implementar class_balance()
- [ ] Implementar concept_balance()
- [ ] Implementar kl_divergence()
- [ ] Implementar js_divergence()
- [ ] Escrever testes em `tests/core/metrics/test_pretrain.py`
- [ ] Validar com datasets sintéticos

**Estimativa**: 12 horas
**Prioridade**: MUST
**Referência**: DeepBridge `fairness/metrics.py:class_balance`

---

##### US-008: Métricas Post-Training Básicas
**Como** data scientist
**Quero** métricas dependentes de predições
**Para** avaliar viés do modelo

**Critérios de Aceite**:
- [ ] Statistical Parity implementado
- [ ] Disparate Impact implementado
- [ ] Equal Opportunity implementado
- [ ] Equalized Odds implementado
- [ ] Testes com modelos reais (sklearn)
- [ ] Edge cases cobertos

**Tarefas**:
- [ ] Criar `justiceai/core/metrics/posttrain.py`
- [ ] Implementar statistical_parity()
- [ ] Implementar disparate_impact()
- [ ] Implementar equal_opportunity()
- [ ] Implementar equalized_odds()
- [ ] Criar fixtures de modelos em `tests/conftest.py`
- [ ] Escrever testes

**Estimativa**: 14 horas
**Prioridade**: MUST
**Referência**: DeepBridge `fairness/metrics.py:statistical_parity`

---

##### US-009: Métricas Post-Training Avançadas
**Como** data scientist
**Quero** métricas adicionais de fairness
**Para** análise completa

**Critérios de Aceite**:
- [ ] False Negative Rate Difference
- [ ] Conditional Acceptance (PPV)
- [ ] Conditional Rejection (NPV)
- [ ] Precision Difference
- [ ] Accuracy Difference
- [ ] Treatment Equality
- [ ] Entropy Index

**Tarefas**:
- [ ] Implementar 7 métricas em `posttrain.py`
- [ ] Testes para cada métrica
- [ ] Validar contra Fairlearn (benchmark)
- [ ] Documentar diferenças (se houver)

**Estimativa**: 16 horas
**Prioridade**: MUST

---

##### US-010: Confusion Matrix por Grupo
**Como** data scientist
**Quero** confusion matrix estratificada
**Para** análise detalhada

**Critérios de Aceite**:
- [ ] Função `confusion_matrix_by_group()`
- [ ] Retorna TP, FP, TN, FN por grupo
- [ ] Validação com sklearn.metrics
- [ ] Testes com datasets desbalanceados

**Tarefas**:
- [ ] Implementar em `posttrain.py`
- [ ] Adicionar visualização (preparação para reports)
- [ ] Testes

**Estimativa**: 6 horas
**Prioridade**: SHOULD

---

##### US-011: Threshold Analysis
**Como** ML engineer
**Quero** análise de thresholds de decisão
**Para** otimizar fairness

**Critérios de Aceite**:
- [ ] Função `threshold_analysis()`
- [ ] Testa 100 thresholds (0.01 a 0.99)
- [ ] Retorna threshold ótimo
- [ ] Curvas de fairness vs performance

**Tarefas**:
- [ ] Criar `justiceai/core/evaluators/threshold.py`
- [ ] Implementar grid search de thresholds
- [ ] Calcular métricas para cada threshold
- [ ] Encontrar threshold ótimo
- [ ] Testes

**Estimativa**: 10 horas
**Prioridade**: SHOULD
**Referência**: DeepBridge `fairness_suite.py:run_threshold_analysis`

---

##### US-012: FairnessCalculator Facade
**Como** desenvolvedor
**Quero** uma classe unificada
**Para** calcular todas as métricas

**Critérios de Aceite**:
- [ ] Classe `FairnessCalculator`
- [ ] Métodos para todas as 15 métricas
- [ ] Método `calculate_all()`
- [ ] Caching de resultados
- [ ] Validação de inputs

**Tarefas**:
- [ ] Criar `justiceai/core/metrics/calculator.py`
- [ ] Implementar FairnessCalculator
- [ ] Adicionar validação de inputs
- [ ] Implementar caching
- [ ] Testes

**Estimativa**: 8 horas
**Prioridade**: MUST

---

#### Sprint 1 - Resumo

**Total Story Points**: 66 horas
**Buffer**: 14 horas

**Entregáveis**:
- ✅ 15+ métricas de fairness
- ✅ Confusion matrix por grupo
- ✅ Threshold analysis
- ✅ Facade pattern para APIs
- ✅ Coverage ≥ 95% nas métricas

---

### 📊 SPRINT 2: Reports HTML (Semanas 5-6)

**Objetivo**: Sistema de relatórios standalone com Plotly

**Capacity**: 80 horas

#### User Stories

##### US-013: Data Transformer para Reports
**Como** sistema
**Quero** transformar dados de métricas
**Para** formato adequado aos templates

**Critérios de Aceite**:
- [ ] Classe `FairnessDataTransformer`
- [ ] Transforma resultados de métricas para dict
- [ ] Prepara dados para Plotly
- [ ] Calcula overall fairness score
- [ ] Gera warnings e critical issues

**Tarefas**:
- [ ] Criar `justiceai/reports/transformers/data_transformer.py`
- [ ] Implementar transform()
- [ ] Implementar calculate_fairness_score()
- [ ] Testes

**Estimativa**: 10 horas
**Prioridade**: MUST
**Referência**: DeepBridge `transformers/fairness/data_transformer.py`

---

##### US-014: Chart Factory com Plotly
**Como** sistema
**Quero** gerar gráficos interativos
**Para** visualização de métricas

**Critérios de Aceite**:
- [ ] Classe `PlotlyChartFactory`
- [ ] Gráfico: Disparate Impact por grupo
- [ ] Gráfico: Statistical Parity comparison
- [ ] Gráfico: Confusion Matrix heatmap
- [ ] Gráfico: Threshold analysis curve
- [ ] Todos gráficos exportam para HTML embeddable

**Tarefas**:
- [ ] Criar `justiceai/reports/charts/plotly_charts.py`
- [ ] Implementar disparate_impact_chart()
- [ ] Implementar statistical_parity_chart()
- [ ] Implementar confusion_matrix_heatmap()
- [ ] Implementar threshold_curve_chart()
- [ ] Testes visuais (snapshots)

**Estimativa**: 16 horas
**Prioridade**: MUST
**Referência**: DeepBridge `charts/posttrain_charts.py`

---

##### US-015: Template HTML Jinja2
**Como** usuário
**Quero** report HTML profissional
**Para** apresentar para stakeholders

**Critérios de Aceite**:
- [ ] Template Jinja2 responsivo
- [ ] Seções: Summary, Metrics, Charts, Issues
- [ ] Estilo profissional (CSS embutido)
- [ ] Plotly charts interativos
- [ ] Funciona offline (standalone)
- [ ] Print-friendly

**Tarefas**:
- [ ] Criar `justiceai/reports/templates/fairness_report.html`
- [ ] Criar CSS embutido
- [ ] Adicionar Plotly.js (CDN ou embeded)
- [ ] Criar seções do report
- [ ] Testar em diferentes navegadores

**Estimativa**: 12 horas
**Prioridade**: MUST
**Referência**: DeepBridge `templates/report_types/fairness/interactive/index.html`

---

##### US-016: HTML Renderer
**Como** sistema
**Quero** renderizar template com dados
**Para** gerar arquivo HTML final

**Critérios de Aceite**:
- [ ] Classe `FairnessHTMLRenderer`
- [ ] Método `render(data, output_path)`
- [ ] Gera HTML standalone
- [ ] Valida HTML (bem-formado)
- [ ] Tamanho razoável (< 5MB)

**Tarefas**:
- [ ] Criar `justiceai/reports/renderers/html_renderer.py`
- [ ] Implementar render()
- [ ] Adicionar validação
- [ ] Testar com dados reais
- [ ] Benchmark de tamanho

**Estimativa**: 8 horas
**Prioridade**: MUST
**Referência**: DeepBridge `renderers/fairness_renderer_simple.py`

---

##### US-017: Report Builder (Facade)
**Como** usuário
**Quero** uma classe simples para gerar reports
**Para** usar em uma linha

**Critérios de Aceite**:
- [ ] Classe `FairnessReport`
- [ ] Método `from_metrics(metrics)`
- [ ] Método `save_html(path)`
- [ ] Método `show()` (abre navegador)
- [ ] Suporta customização (título, logo, etc.)

**Tarefas**:
- [ ] Criar `justiceai/reports/report_builder.py`
- [ ] Implementar FairnessReport
- [ ] Integrar transformer + renderer
- [ ] Adicionar método show() (webbrowser)
- [ ] Testes end-to-end

**Estimativa**: 10 horas
**Prioridade**: MUST

---

##### US-018: Exemplos de Reports
**Como** usuário
**Quero** ver exemplos de reports
**Para** entender output

**Critérios de Aceite**:
- [ ] Pelo menos 3 reports gerados
- [ ] Dataset: Breast Cancer (simples)
- [ ] Dataset: Adult (complexo)
- [ ] Dataset: COMPAS (real-world)
- [ ] Reports salvos em `examples/reports/`

**Tarefas**:
- [ ] Criar script `examples/generate_report_basic.py`
- [ ] Criar script `examples/generate_report_adult.py`
- [ ] Criar script `examples/generate_report_compas.py`
- [ ] Gerar e versionar HTMLs
- [ ] Documentar em README

**Estimativa**: 8 horas
**Prioridade**: SHOULD

---

#### Sprint 2 - Resumo

**Total Story Points**: 64 horas
**Buffer**: 16 horas

**Entregáveis**:
- ✅ Sistema completo de reports
- ✅ Plotly charts interativos
- ✅ HTML standalone
- ✅ Exemplos prontos

---

### 🎨 SPRINT 3: API Pública + Docs (Semanas 7-8)

**Objetivo**: API simples e documentação completa

**Capacity**: 80 horas

#### User Stories

##### US-019: Model Adapters
**Como** usuário
**Quero** suporte a múltiplos frameworks
**Para** usar com meu modelo

**Critérios de Aceite**:
- [ ] Adapter para sklearn
- [ ] Adapter para XGBoost
- [ ] Adapter para LightGBM
- [ ] Adapter para ONNX
- [ ] Detecção automática de framework
- [ ] Mensagens de erro claras

**Tarefas**:
- [ ] Criar `justiceai/core/adapters/base.py` (ABC)
- [ ] Implementar SklearnAdapter
- [ ] Implementar XGBoostAdapter
- [ ] Implementar LightGBMAdapter
- [ ] Implementar ONNXAdapter
- [ ] Criar factory auto-detect
- [ ] Testes para cada adapter

**Estimativa**: 14 horas
**Prioridade**: MUST

---

##### US-020: FairnessEvaluator (Main API)
**Como** usuário
**Quero** API simples de alto nível
**Para** avaliar fairness em 1 linha

**Critérios de Aceite**:
- [ ] Classe `FairnessEvaluator`
- [ ] Método `evaluate(model, data, protected_attrs)`
- [ ] Retorna objeto `FairnessResult`
- [ ] Suporta configuração (metrics, thresholds)
- [ ] Validação robusta de inputs

**Tarefas**:
- [ ] Criar `justiceai/core/evaluators/fairness.py`
- [ ] Implementar FairnessEvaluator
- [ ] Criar FairnessResult dataclass
- [ ] Adicionar validações
- [ ] Testes

**Estimativa**: 12 hours
**Prioridade**: MUST

---

##### US-021: API de Conveniência `audit()`
**Como** usuário
**Quero** função top-level `audit()`
**Para** usar sem imports complexos

**Critérios de Aceite**:
- [ ] Função `audit(model, data, protected_attrs)`
- [ ] Retorna `FairnessResult` com `.save_html()`, `.show()`
- [ ] Docstring exemplar
- [ ] Exportada em `__init__.py`

**Tarefas**:
- [ ] Criar `justiceai/api.py`
- [ ] Implementar audit()
- [ ] Adicionar a `__all__` em `__init__.py`
- [ ] Testes
- [ ] Exemplo em README

**Estimativa**: 6 horas
**Prioridade**: MUST

---

##### US-022: Documentação com MkDocs
**Como** usuário
**Quero** docs completas
**Para** aprender a usar

**Critérios de Aceite**:
- [ ] MkDocs Material configurado
- [ ] Página inicial (index.md)
- [ ] Getting Started
- [ ] API Reference (auto-gerado)
- [ ] Examples/Tutorials
- [ ] FAQ
- [ ] Deploy em GitHub Pages

**Tarefas**:
- [ ] Setup MkDocs
- [ ] Escrever getting_started.md
- [ ] Configurar mkdocstrings
- [ ] Escrever tutoriais
- [ ] Deploy workflow
- [ ] Revisar português/inglês

**Estimativa**: 16 horas
**Prioridade**: MUST

---

##### US-023: Jupyter Notebooks Tutorial
**Como** usuário
**Quero** notebooks interativos
**Para** aprender hands-on

**Critérios de Aceite**:
- [ ] Notebook 01: Quick Start
- [ ] Notebook 02: Advanced Metrics
- [ ] Notebook 03: Reports Customization
- [ ] Notebooks testados (nbval)
- [ ] Salvos em `examples/notebooks/`

**Tarefas**:
- [ ] Criar 3 notebooks
- [ ] Adicionar narrativas claras
- [ ] Testar com pytest-nbval
- [ ] Adicionar ao README

**Estimativa**: 10 horas
**Prioridade**: SHOULD

---

##### US-024: Docstrings Completas
**Como** desenvolvedor
**Quero** docstrings em 100% APIs
**Para** docs auto-geradas

**Critérios de Aceite**:
- [ ] Google-style docstrings
- [ ] Todas funções públicas documentadas
- [ ] Exemplos em docstrings críticas
- [ ] Type hints consistentes
- [ ] Validado por pydocstyle

**Tarefas**:
- [ ] Revisar todas funções públicas
- [ ] Adicionar/melhorar docstrings
- [ ] Adicionar exemplos
- [ ] Configurar pydocstyle
- [ ] CI valida docstrings

**Estimativa**: 12 horas
**Prioridade**: MUST

---

#### Sprint 3 - Resumo

**Total Story Points**: 70 horas
**Buffer**: 10 horas

**Entregáveis**:
- ✅ API pública simples
- ✅ Suporte múltiplos frameworks
- ✅ Docs completas (MkDocs)
- ✅ Tutoriais e notebooks

---

### 🇧🇷 SPRINT 4: Compliance Brasil + Monitoring (Semanas 9-10)

**Objetivo**: Compliance LGPD/BACEN e monitoring

**Capacity**: 80 horas

#### User Stories

##### US-025: LGPD Compliance Reporter
**Como** compliance officer
**Quero** relatório LGPD Art. 20
**Para** demonstrar conformidade

**Critérios de Aceite**:
- [ ] Classe `LGPDReporter`
- [ ] Template específico LGPD
- [ ] Seções: Transparência, Explicação, Fairness
- [ ] Linguagem português BR
- [ ] Referências legais (Art. 20)

**Tarefas**:
- [ ] Criar `justiceai/compliance/lgpd.py`
- [ ] Implementar LGPDReporter
- [ ] Criar template Jinja2
- [ ] Adicionar referências legais
- [ ] Exemplo de uso

**Estimativa**: 12 horas
**Prioridade**: SHOULD

---

##### US-026: BACEN Compliance Reporter
**Como** risk manager (banco)
**Quero** relatório BACEN Res. 4.658
**Para** auditoria

**Critérios de Aceite**:
- [ ] Classe `BACENReporter`
- [ ] Template específico BACEN
- [ ] Métricas de risco de modelo
- [ ] Assessment de fairness

**Tarefas**:
- [ ] Criar `justiceai/compliance/bacen.py`
- [ ] Implementar BACENReporter
- [ ] Criar template
- [ ] Exemplo de uso

**Estimativa**: 12 horas
**Prioridade**: SHOULD

---

##### US-027: Fairness Drift Detection
**Como** ML engineer
**Quero** detectar drift de fairness
**Para** monitorar produção

**Critérios de Aceite**:
- [ ] Classe `FairnessDriftDetector`
- [ ] Compara métricas ao longo do tempo
- [ ] Detecta drift estatisticamente significante
- [ ] Retorna alertas

**Tarefas**:
- [ ] Criar `justiceai/monitoring/drift.py`
- [ ] Implementar drift detection (KS test, PSI)
- [ ] Testes com séries temporais
- [ ] Exemplo de uso

**Estimativa**: 14 horas
**Prioridade**: SHOULD

---

##### US-028: Alerting System
**Como** ML engineer
**Quero** sistema de alertas
**Para** ser notificado de issues

**Critérios de Aceite**:
- [ ] Classe `FairnessAlerter`
- [ ] Suporta Slack webhook
- [ ] Suporta email (SMTP)
- [ ] Configurável (thresholds)

**Tarefas**:
- [ ] Criar `justiceai/monitoring/alerting.py`
- [ ] Implementar Slack integration
- [ ] Implementar email
- [ ] Testes (mock)

**Estimativa**: 10 horas
**Prioridade**: COULD

---

##### US-029: Continuous Monitoring Example
**Como** usuário
**Quero** exemplo de monitoring
**Para** implementar em produção

**Critérios de Aceite**:
- [ ] Script completo de monitoring
- [ ] Simula drift ao longo do tempo
- [ ] Gera alertas
- [ ] Documentado passo-a-passo

**Tarefas**:
- [ ] Criar `examples/monitoring_production.py`
- [ ] Simular dados com drift
- [ ] Demonstrar alerting
- [ ] Documentar

**Estimativa**: 8 horas
**Prioridade**: SHOULD

---

#### Sprint 4 - Resumo

**Total Story Points**: 56 horas
**Buffer**: 24 horas (para polish)

**Entregáveis**:
- ✅ Compliance LGPD/BACEN
- ✅ Drift detection
- ✅ Sistema de alertas
- ✅ Exemplo de monitoring

---

### 🚀 SPRINT 5: Polish & Release (Semanas 11-12)

**Objetivo**: Preparar para lançamento público

**Capacity**: 80 horas

#### User Stories

##### US-030: Code Review Completo
**Como** team
**Quero** revisar todo código
**Para** garantir qualidade máxima

**Critérios de Aceite**:
- [ ] 100% código revisado
- [ ] Refatorações feitas
- [ ] Duplicações removidas
- [ ] Performance otimizada

**Estimativa**: 16 horas
**Prioridade**: MUST

---

##### US-031: Coverage ≥ 95%
**Como** team
**Quero** cobertura de testes ≥ 95%
**Para** confiança no código

**Critérios de Aceite**:
- [ ] Coverage total ≥ 95%
- [ ] Módulos críticos 100%
- [ ] Edge cases cobertos

**Estimativa**: 12 horas
**Prioridade**: MUST

---

##### US-032: Performance Benchmarks
**Como** usuário
**Quero** saber performance
**Para** decidir se usar

**Critérios de Aceite**:
- [ ] Benchmarks vs Fairlearn, AIF360
- [ ] Documentado em README
- [ ] Gráficos de comparação

**Estimativa**: 8 horas
**Prioridade**: SHOULD

---

##### US-033: Packaging & PyPI
**Como** usuário
**Quero** instalar via pip
**Para** usar facilmente

**Critérios de Aceite**:
- [ ] Publicado no PyPI
- [ ] Instalável via `pip install justiceai`
- [ ] Wheel e source dist disponíveis

**Tarefas**:
- [ ] Build com Poetry
- [ ] Test no Test PyPI
- [ ] Publicar no PyPI
- [ ] Validar instalação

**Estimativa**: 6 horas
**Prioridade**: MUST

---

##### US-034: Release v1.0.0
**Como** PM
**Quero** lançar v1.0.0
**Para** anunciar ao público

**Critérios de Aceite**:
- [ ] Tag v1.0.0 criada
- [ ] Release notes escritas
- [ ] GitHub release publicada
- [ ] Anúncio em redes sociais

**Estimativa**: 4 horas
**Prioridade**: MUST

---

##### US-035: Marketing Materials
**Como** PM
**Quero** materiais de divulgação
**Para** atrair usuários

**Critérios de Aceite**:
- [ ] Blog post de lançamento
- [ ] Tweet thread
- [ ] LinkedIn post
- [ ] Submissão em PyPI trending

**Estimativa**: 8 horas
**Prioridade**: SHOULD

---

#### Sprint 5 - Resumo

**Total Story Points**: 54 horas
**Buffer**: 26 horas (contingência)

**Entregáveis**:
- ✅ Código revisado e polido
- ✅ Coverage ≥ 95%
- ✅ Publicado no PyPI
- ✅ Lançamento v1.0.0
- ✅ Marketing materials

---

## 8. Métricas de Qualidade

### 8.1. Code Quality Gates

| Métrica | Mínimo Aceitável | Target | Ferramenta |
|---------|------------------|--------|------------|
| **Code Coverage** | 90% | 95% | pytest-cov |
| **Type Coverage** | 90% | 100% (public APIs) | mypy |
| **Pylint Score** | 8.0 | 9.5 | pylint |
| **Complexity (CC)** | < 10 por função | < 7 | radon |
| **Duplicate Code** | < 5% | < 2% | pylint |
| **Docstring Coverage** | 90% (public) | 100% (public) | interrogate |

### 8.2. Performance Benchmarks

**Target**: Ser competitivo com Fairlearn

| Operação | Target | Medição |
|----------|--------|---------|
| Calcular 15 métricas (10k samples) | < 2s | pytest-benchmark |
| Gerar report HTML (10k samples) | < 5s | time.time() |
| Threshold analysis (100 thresholds) | < 10s | pytest-benchmark |

### 8.3. Sprint Velocity Tracking

Medir após cada sprint:
- Story points completados
- Bugs introduzidos
- Bugs resolvidos
- Tempo médio de PR review
- CI/CD build time

---

## 9. Riscos e Mitigações

| # | Risco | Probabilidade | Impacto | Mitigação |
|---|-------|---------------|---------|-----------|
| **R1** | Scope creep | ALTA | ALTO | Backlog priorizado, PO forte |
| **R2** | Dependência breaking | MÉDIA | MÉDIO | Pin versões, CI multi-version |
| **R3** | Baixa adoção inicial | MÉDIA | ALTO | Marketing, early adopters, docs |
| **R4** | Bugs críticos pós-launch | BAIXA | ALTO | Coverage ≥ 95%, beta testers |
| **R5** | Competidor lança similar | BAIXA | MÉDIO | Foco em diferenciais (Brasil, MLOps) |
| **R6** | Time não disponível | MÉDIA | ALTO | Buffer 20% em sprints, priorização |

---

## 10. Cronograma Visual

```
MESES:        │  FEV  │  MAR  │  ABR  │  MAI  │
SEMANAS:      │ 1 2 3 4│ 1 2 3 4│ 1 2 3 4│ 1 2 3 4│
─────────────────────────────────────────────────
SPRINT 0      ████████│        │        │        │ Setup
SPRINT 1            ██████████│        │        │ Métricas
SPRINT 2                  ████████████│        │ Reports
SPRINT 3                        ██████████████  │ API+Docs
SPRINT 4                              ██████████│ Compliance
SPRINT 5                                    ████ Beta/Release

MILESTONES:
  △ = Sprint Review
  ◆ = Release Candidate
  ★ = v1.0.0 Launch

    △     △     △     △     △  ◆★
```

---

## 11. Definition of Success

O projeto será considerado **sucesso** se:

### Critérios Técnicos (MVP - Sprint 5)
- [ ] ✅ Coverage ≥ 90%
- [ ] ✅ Zero bugs críticos conhecidos
- [ ] ✅ Publicado no PyPI
- [ ] ✅ Docs completas (API + tutoriais)
- [ ] ✅ 15+ métricas de fairness
- [ ] ✅ Reports HTML funcionando

### Critérios de Adoção (3 meses pós-launch)
- [ ] 500+ downloads PyPI
- [ ] 200+ stars GitHub
- [ ] 5+ contributors externos
- [ ] 10+ issues resolvidas
- [ ] 3+ empresas usando (validado)

### Critérios de Qualidade (contínuo)
- [ ] NPS ≥ 8 (de early adopters)
- [ ] Tempo resposta issues < 48h
- [ ] CI sempre verde
- [ ] Zero debt técnico crítico

---

## 12. Próximos Passos

### Imediatos (esta semana)
1. ✅ Aprovar este planejamento
2. ⏳ Criar repositório GitHub `justiceai`
3. ⏳ Setup projeto (Sprint 0, US-001)
4. ⏳ Convidar early adopters para beta

### Sprint 0 (próximas 2 semanas)
- Executar todas US-001 a US-006
- Daily standups (async ou sync)
- Sprint review ao final
- Retrospectiva

### Longo Prazo (pós v1.0)
- v1.1: PyTorch/TensorFlow support
- v1.2: Mitigation strategies
- v1.3: LLM-powered insights
- v2.0: SaaS offering (?)

---

## 📞 Contatos

**Product Owner**: Gustavo Haase
**Email**: gustavo.haase@gmail.com
**GitHub**: @guhaase

---

**Documento vivo**: Este planejamento será atualizado conforme aprendemos.
**Última atualização**: 2026-02-08
**Versão**: 1.0
**Status**: ✅ Aprovado para execução
