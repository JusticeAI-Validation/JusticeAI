# 📊 Product Backlog Detalhado - justiceai

**Versão**: 1.0
**Data**: 2026-02-08
**Formato**: User Stories com critérios INVEST

---

## 📌 Legenda

**Prioridade**:
- 🔴 **CRITICAL**: Bloqueante, MVP depende
- 🟠 **HIGH**: Importante para MVP
- 🟡 **MEDIUM**: Desejável para v1.0
- 🟢 **LOW**: Nice to have, v1.x

**Estimativa**: Story Points (Fibonacci: 1, 2, 3, 5, 8, 13, 21)

**Status**:
- ⏳ **TODO**: Não iniciada
- 🏗️ **IN PROGRESS**: Em desenvolvimento
- ✅ **DONE**: Completada e aceita
- ❌ **BLOCKED**: Bloqueada por dependência

---

## 🎯 ÉPICO 1: Setup & Fundação

### US-001: Setup Projeto com Poetry 🔴
**Prioridade**: CRITICAL
**Estimativa**: 3 SP
**Sprint**: Sprint 0
**Status**: ⏳ TODO

**User Story**:
> Como **desenvolvedor**,
> Eu quero um **projeto Python estruturado com Poetry**,
> Para **gerenciar dependências de forma profissional**

**Critérios de Aceite**:
```gherkin
Feature: Setup Projeto com Poetry

Scenario: Projeto é instalável
  Given repositório clonado
  When executar "poetry install"
  Then todas dependências devem ser instaladas
  And ambiente virtual deve ser criado

Scenario: Estrutura de diretórios
  Given projeto instalado
  Then deve existir diretório "justiceai/"
  And deve existir diretório "tests/"
  And deve existir "pyproject.toml"
  And deve existir "README.md"

Scenario: Import básico funciona
  Given projeto instalado
  When executar "python -c 'import justiceai'"
  Then não deve haver erros
  And deve exibir versão correta
```

**Tasks Técnicas**:
- [ ] Instalar Poetry (>= 1.7.0)
- [ ] Executar `poetry init --name justiceai`
- [ ] Configurar `pyproject.toml` completo
- [ ] Adicionar dependências core: numpy, pandas, scikit-learn, scipy
- [ ] Adicionar dependências de visualização: plotly, jinja2
- [ ] Adicionar dependências de dev: pytest, black, mypy, ruff
- [ ] Criar estrutura: `justiceai/`, `tests/`, `examples/`, `docs/`
- [ ] Criar `justiceai/__init__.py` com `__version__ = "0.1.0"`
- [ ] Inicializar Git: `git init`
- [ ] Criar `.gitignore` (Python template)
- [ ] Testar `poetry install` e `poetry shell`

**Dependências**: Nenhuma

**Referências**:
- Guia: `/home/guhaase/projetos/DeepBridge/desenvolvimento/GUIA_BUILD_PUBLICACAO_PYTHON.md`
- Template: DeepBridge `pyproject.toml`

**Definition of Done (DoD)**:
- [x] Código: `poetry install` funciona sem erros
- [x] Estrutura de diretórios criada
- [x] `import justiceai` funciona
- [x] Git inicializado com commit inicial
- [x] PR criado e aprovado
- [x] Documentado em README

---

### US-002: CI/CD com GitHub Actions 🔴
**Prioridade**: CRITICAL
**Estimativa**: 5 SP
**Sprint**: Sprint 0
**Status**: ⏳ TODO

**User Story**:
> Como **desenvolvedor**,
> Eu quero **pipeline CI/CD automatizado**,
> Para **garantir qualidade em cada commit**

**Critérios de Aceite**:
```gherkin
Feature: CI/CD Pipeline

Scenario: Workflow de testes funciona
  Given código commitado
  When push para branch main
  Then workflow "test.yml" deve executar
  And testes devem passar em Python 3.10, 3.11, 3.12
  And coverage report deve ser gerado

Scenario: Workflow de qualidade funciona
  Given código commitado
  When criar Pull Request
  Then workflow "quality.yml" deve executar
  And black/isort devem validar formatação
  And mypy deve validar tipos
  And ruff deve validar linting

Scenario: Badges no README
  Given workflows configurados
  When acessar README.md
  Then deve exibir badge "build: passing"
  And deve exibir badge "coverage: XX%"
  And deve exibir badge "python: 3.10 | 3.11 | 3.12"
```

**Tasks Técnicas**:
- [ ] Criar `.github/workflows/test.yml`
  - [ ] Matrix: Python 3.10, 3.11, 3.12
  - [ ] Matrix: OS ubuntu-latest, macos-latest, windows-latest
  - [ ] Rodar `pytest --cov`
  - [ ] Upload para Codecov
- [ ] Criar `.github/workflows/quality.yml`
  - [ ] Check: Black formatação
  - [ ] Check: isort imports
  - [ ] Check: MyPy types
  - [ ] Check: Ruff linting
  - [ ] Fail se qualquer check falhar
- [ ] Criar `.github/workflows/build.yml`
  - [ ] Build wheel e sdist
  - [ ] Validar com twine check
  - [ ] Upload artifacts
- [ ] Configurar Codecov
  - [ ] Criar conta em codecov.io
  - [ ] Adicionar token em GitHub Secrets
  - [ ] Configurar `codecov.yml`
- [ ] Adicionar badges ao README.md
  - [ ] Build status
  - [ ] Coverage
  - [ ] Python versions
  - [ ] License
  - [ ] PyPI version (placeholder)

**Dependências**: US-001 (projeto criado)

**Referências**:
- Template: DeepBridge `.github/workflows/`
- Docs: https://docs.github.com/actions

**DoD**:
- [x] Workflows executam em cada PR
- [x] Testes passam em 3 versões Python
- [x] Coverage > 80% (inicial)
- [x] Badges funcionando no README
- [x] CI documentado em CONTRIBUTING.md

---

### US-003: Configurar Linters e Formatters 🔴
**Prioridade**: CRITICAL
**Estimativa**: 3 SP
**Sprint**: Sprint 0
**Status**: ⏳ TODO

**User Story**:
> Como **desenvolvedor**,
> Eu quero **ferramentas de qualidade configuradas**,
> Para **manter código consistente e limpo**

**Critérios de Aceite**:
```gherkin
Feature: Linters e Formatters

Scenario: Black formata código
  Given arquivo Python desformatado
  When executar "make format"
  Then código deve ser formatado (line-length=88)
  And deve seguir estilo Black

Scenario: MyPy valida tipos
  Given código com type hints
  When executar "make type-check"
  Then MyPy deve validar sem erros
  And strict mode deve estar ativo

Scenario: Ruff valida linting
  Given código formatado
  When executar "make lint"
  Then Ruff deve validar sem warnings
  And deve checar: E, W, F, I, B, C4, UP, ARG, SIM

Scenario: Pre-commit hooks funcionam
  Given hooks instalados
  When tentar commitar código ruim
  Then commit deve ser bloqueado
  And deve sugerir correções
```

**Tasks Técnicas**:
- [ ] Configurar Black em `pyproject.toml`:
  ```toml
  [tool.black]
  line-length = 88
  target-version = ['py310', 'py311', 'py312']
  ```
- [ ] Configurar isort:
  ```toml
  [tool.isort]
  profile = "black"
  line_length = 88
  ```
- [ ] Configurar MyPy (strict):
  ```toml
  [tool.mypy]
  strict = true
  python_version = "3.10"
  ```
- [ ] Configurar Ruff:
  ```toml
  [tool.ruff]
  line-length = 88
  select = ["E", "W", "F", "I", "B", "C4", "UP", "ARG", "SIM"]
  ```
- [ ] Configurar Pylint:
  ```toml
  [tool.pylint.main]
  py-version = "3.10"
  ```
- [ ] Criar `.pre-commit-config.yaml`:
  - [ ] Hook: trailing-whitespace
  - [ ] Hook: end-of-file-fixer
  - [ ] Hook: black
  - [ ] Hook: isort
  - [ ] Hook: ruff
  - [ ] Hook: mypy
- [ ] Criar `Makefile`:
  - [ ] Target: `make format` (black + isort)
  - [ ] Target: `make lint` (ruff + pylint)
  - [ ] Target: `make type-check` (mypy)
  - [ ] Target: `make test` (pytest)
  - [ ] Target: `make quality` (all above)
- [ ] Instalar hooks: `pre-commit install`
- [ ] Rodar em codebase: `make quality`

**Dependências**: US-001

**Referências**:
- Guia: `GUIA_QUALIDADE_CODIGO_PYTHON.md`

**DoD**:
- [x] Todas configs em `pyproject.toml`
- [x] Pre-commit hooks instalados
- [x] `make quality` passa sem erros
- [x] Documentado em README

---

### US-004: Setup de Testes com Pytest 🔴
**Prioridade**: CRITICAL
**Estimativa**: 3 SP
**Sprint**: Sprint 0
**Status**: ⏳ TODO

**User Story**:
> Como **desenvolvedor**,
> Eu quero **framework de testes configurado**,
> Para **escrever testes desde o início**

**Critérios de Aceite**:
```gherkin
Feature: Framework de Testes

Scenario: Pytest executa testes
  Given testes escritos em tests/
  When executar "pytest"
  Then todos testes devem executar
  And deve exibir sumário

Scenario: Coverage é calculado
  Given testes executados
  When executar "pytest --cov"
  Then deve gerar relatório de coverage
  And deve mostrar linhas não cobertas
  And deve gerar HTML em htmlcov/

Scenario: Fixtures básicos disponíveis
  Given arquivo tests/conftest.py
  Then deve ter fixture "sample_data"
  And deve ter fixture "sample_model"
  And deve ter fixture "sample_predictions"
```

**Tasks Técnicas**:
- [ ] Adicionar pytest dependencies:
  ```toml
  pytest>=7.0
  pytest-cov>=4.0
  pytest-xdist>=3.0
  ```
- [ ] Configurar pytest em `pyproject.toml`:
  ```toml
  [tool.pytest.ini_options]
  testpaths = ["tests"]
  python_files = ["test_*.py"]
  addopts = "--cov=justiceai --cov-report=term-missing --cov-report=html"
  ```
- [ ] Configurar coverage:
  ```toml
  [tool.coverage.run]
  source = ["justiceai"]
  omit = ["*/tests/*"]
  branch = true

  [tool.coverage.report]
  precision = 2
  show_missing = true
  fail_under = 90
  ```
- [ ] Criar estrutura `tests/`:
  ```
  tests/
  ├── __init__.py
  ├── conftest.py          # Fixtures globais
  ├── core/
  │   ├── __init__.py
  │   └── metrics/
  │       └── test_pretrain.py
  └── test_api.py
  ```
- [ ] Criar `tests/conftest.py` com fixtures:
  ```python
  @pytest.fixture
  def sample_data():
      return pd.DataFrame(...)

  @pytest.fixture
  def sample_model():
      return RandomForestClassifier()
  ```
- [ ] Criar teste dummy que passa:
  ```python
  def test_import():
      import justiceai
      assert justiceai.__version__ == "0.1.0"
  ```
- [ ] Adicionar ao Makefile:
  ```makefile
  test:
      pytest

  test-cov:
      pytest --cov --cov-report=html
      open htmlcov/index.html  # macOS
  ```
- [ ] Documentar em CONTRIBUTING.md

**Dependências**: US-001

**DoD**:
- [x] `pytest` executa sem erros
- [x] Coverage configurado (target 90%)
- [x] Fixtures básicos criados
- [x] Pelo menos 1 teste passando
- [x] Documentado como rodar testes

---

### US-005: Documentação Inicial 🟠
**Prioridade**: HIGH
**Estimativa**: 5 SP
**Sprint**: Sprint 0
**Status**: ⏳ TODO

**User Story**:
> Como **usuário potencial**,
> Eu quero **documentação clara do projeto**,
> Para **entender o que é e como usar**

**Critérios de Aceite**:
```gherkin
Feature: Documentação Inicial

Scenario: README completo
  Given acesso ao repositório
  When abrir README.md
  Then deve ter descrição clara do projeto
  And deve ter badges (build, coverage, etc.)
  And deve ter Quick Start com exemplo
  And deve ter instruções de instalação
  And deve ter seção "Contributing"
  And deve ter link para documentação completa

Scenario: LICENSE presente
  Given repositório público
  When verificar root directory
  Then deve existir arquivo LICENSE
  And deve ser MIT License

Scenario: CHANGELOG iniciado
  Given projeto versionado
  When verificar CHANGELOG.md
  Then deve seguir formato Keep a Changelog
  And deve ter seção [Unreleased]
  And deve ter seção [0.1.0]
```

**Tasks Técnicas**:
- [ ] Escrever `README.md`:
  ```markdown
  # justiceai

  [![Build](https://github.com/.../badge.svg)]()
  [![Coverage](https://codecov.io/.../badge.svg)]()
  [![Python](https://img.shields.io/badge/python-3.10%2B-blue)]()
  [![License](https://img.shields.io/badge/license-MIT-green)]()

  > Biblioteca Python para análise de fairness em ML

  ## 🚀 Quick Start

  ```python
  from justiceai import audit

  report = audit(model, data, protected_attrs=['gender'])
  report.show()  # Abre HTML no navegador
  ```

  ## 📦 Instalação

  ```bash
  pip install justiceai  # Em breve!
  ```

  ## 🎯 Features

  - 15+ métricas de fairness
  - Reports HTML interativos
  - Compliance LGPD/BACEN
  - Framework-agnostic

  ## 📚 Documentação

  https://justiceai.readthedocs.io (em breve)

  ## 🤝 Contributing

  Veja [CONTRIBUTING.md](CONTRIBUTING.md)

  ## 📄 Licença

  MIT License - veja [LICENSE](LICENSE)
  ```
- [ ] Criar `LICENSE` (MIT):
  ```
  MIT License

  Copyright (c) 2026 Gustavo Haase
  ...
  ```
- [ ] Criar `CHANGELOG.md`:
  ```markdown
  # Changelog

  ## [Unreleased]

  ### Added
  - Projeto inicial
  - Setup com Poetry
  - CI/CD com GitHub Actions

  ## [0.1.0] - 2026-02-XX

  ### Added
  - Primeira release
  ```
- [ ] Criar `CONTRIBUTING.md`:
  ```markdown
  # Contribuindo para justiceai

  ## Desenvolvimento

  1. Fork e clone
  2. `poetry install`
  3. Criar branch: `git checkout -b feature/nova-feature`
  4. Fazer mudanças
  5. Rodar testes: `make test`
  6. Rodar qualidade: `make quality`
  7. Commit: `git commit -m "feat: adiciona nova feature"`
  8. Push e abrir PR

  ## Code of Conduct

  Seja respeitoso e profissional.

  ## Reportar Bugs

  Abra issue com template.
  ```
- [ ] Criar `.github/ISSUE_TEMPLATE/bug_report.md`
- [ ] Criar `.github/ISSUE_TEMPLATE/feature_request.md`
- [ ] Criar `.github/PULL_REQUEST_TEMPLATE.md`

**Dependências**: US-001

**DoD**:
- [x] README completo e renderiza bem
- [x] LICENSE presente (MIT)
- [x] CHANGELOG.md criado
- [x] CONTRIBUTING.md criado
- [x] Templates de issue/PR criados

---

### US-006: Estrutura de Módulos Base 🔴
**Prioridade**: CRITICAL
**Estimativa**: 2 SP
**Sprint**: Sprint 0
**Status**: ⏳ TODO

**User Story**:
> Como **desenvolvedor**,
> Eu quero **estrutura de módulos criada**,
> Para **começar implementação organizada**

**Critérios de Aceite**:
```gherkin
Feature: Estrutura de Módulos

Scenario: Imports básicos funcionam
  Given projeto instalado
  When executar "import justiceai"
  Then deve importar sem erros
  And deve ter __version__ definido

Scenario: Módulos core existem
  Given estrutura criada
  Then deve existir justiceai/core/
  And deve existir justiceai/core/metrics/
  And deve existir justiceai/core/evaluators/
  And deve existir justiceai/core/adapters/

Scenario: Todos módulos são importáveis
  Given estrutura criada
  When tentar importar cada módulo
  Then nenhum deve dar erro
```

**Tasks Técnicas**:
- [ ] Criar estrutura completa:
  ```
  justiceai/
  ├── __init__.py           # Version, exports
  ├── api.py                # High-level audit() function
  ├── core/
  │   ├── __init__.py
  │   ├── metrics/
  │   │   ├── __init__.py
  │   │   ├── pretrain.py   # Pre-training metrics
  │   │   ├── posttrain.py  # Post-training metrics
  │   │   └── calculator.py # FairnessCalculator
  │   ├── evaluators/
  │   │   ├── __init__.py
  │   │   ├── fairness.py   # FairnessEvaluator
  │   │   └── threshold.py  # ThresholdAnalyzer
  │   └── adapters/
  │       ├── __init__.py
  │       ├── base.py       # BaseAdapter (ABC)
  │       ├── sklearn.py
  │       └── xgboost.py
  ├── reports/
  │   ├── __init__.py
  │   ├── transformers/
  │   │   ├── __init__.py
  │   │   └── data_transformer.py
  │   ├── renderers/
  │   │   ├── __init__.py
  │   │   └── html_renderer.py
  │   ├── templates/
  │   │   └── fairness_report.html
  │   └── report_builder.py
  ├── compliance/
  │   ├── __init__.py
  │   ├── lgpd.py
  │   └── bacen.py
  ├── monitoring/
  │   ├── __init__.py
  │   ├── drift.py
  │   └── alerting.py
  └── utils/
      ├── __init__.py
      ├── validators.py
      └── helpers.py
  ```
- [ ] Criar `justiceai/__init__.py`:
  ```python
  """
  justiceai - Fairness Analysis for ML in Production

  A Python library for fairness analysis in machine learning,
  focused on production monitoring and Brazilian compliance (LGPD/BACEN).
  """

  __version__ = "0.1.0"
  __author__ = "Gustavo Haase"
  __email__ = "gustavo.haase@gmail.com"
  __license__ = "MIT"

  # High-level API
  from justiceai.api import audit

  __all__ = ["audit"]
  ```
- [ ] Criar todos `__init__.py` vazios nos módulos
- [ ] Criar arquivos `.py` com docstrings e `pass`:
  ```python
  """
  Module: pretrain.py
  Pre-training fairness metrics (model-independent).
  """

  # Implementation coming in Sprint 1
  ```
- [ ] Adicionar type: ignore temporários para MyPy
- [ ] Criar teste de import:
  ```python
  def test_import_justiceai():
      import justiceai
      assert justiceai.__version__ == "0.1.0"

  def test_import_submodules():
      from justiceai.core.metrics import pretrain
      from justiceai.reports import report_builder
      # etc
  ```

**Dependências**: US-001, US-004

**DoD**:
- [x] Estrutura completa criada
- [x] Todos `__init__.py` presentes
- [x] `import justiceai` funciona
- [x] Testes de import passam
- [x] MyPy passa (com ignores temporários OK)

---

## 🎯 ÉPICO 2: Métricas Core

### US-007: Métricas Pre-Training 🔴
**Ver PLANEJAMENTO_AGIL.md Sprint 1**

### US-008: Métricas Post-Training Básicas 🔴
**Ver PLANEJAMENTO_AGIL.md Sprint 1**

### US-009: Métricas Post-Training Avançadas 🔴
**Ver PLANEJAMENTO_AGIL.md Sprint 1**

... [continua com todas as outras user stories]

---

## 📊 Backlog Summary

| Épico | Stories | Total SP | Status |
|-------|---------|----------|--------|
| E1: Setup & Fundação | 6 | 21 SP | ⏳ TODO |
| E2: Métricas Core | 6 | 66 SP | ⏳ TODO |
| E3: Reports HTML | 6 | 64 SP | ⏳ TODO |
| E4: API Simplificada | 6 | 70 SP | ⏳ TODO |
| E5: Compliance Brasil | 5 | 56 SP | ⏳ TODO |
| E6: Monitoring | - | - | ⏳ TODO |
| E7: Docs & Polish | - | - | ⏳ TODO |
| **TOTAL MVP** | **~35 stories** | **~280 SP** | ⏳ TODO |

**Velocity Estimada**: ~60 SP/sprint (2 devs × 2 weeks × 15 SP/dev/week)
**Sprints Necessárias**: 5 sprints (280 SP / 60 SP/sprint ≈ 4.7 sprints)

---

**Última Atualização**: 2026-02-08
**Mantido por**: Gustavo Haase
**Formato**: Agile User Stories (INVEST)
