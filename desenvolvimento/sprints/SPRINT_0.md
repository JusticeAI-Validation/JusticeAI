# 🚀 SPRINT 0: Fundação do Projeto

**Período**: Semanas 1-2 (8-22 Fev 2026)
**Objetivo**: Criar estrutura profissional com máxima qualidade de código
**Capacity**: 80 horas (2 devs × 2 semanas × 20h/semana)

---

## 📋 Índice

1. [Visão Geral](#visão-geral)
2. [Objetivos da Sprint](#objetivos-da-sprint)
3. [User Stories](#user-stories)
4. [Definition of Done](#definition-of-done)
5. [Tarefas Técnicas](#tarefas-técnicas)
6. [Métricas de Sucesso](#métricas-de-sucesso)
7. [Riscos e Mitigações](#riscos-e-mitigações)
8. [Entregáveis](#entregáveis)

---

## Visão Geral

Sprint 0 é a sprint de fundação onde estabelecemos a infraestrutura profissional do projeto. Ao final desta sprint, teremos:

- ✅ Projeto estruturado com Poetry
- ✅ CI/CD completo com GitHub Actions
- ✅ Ferramentas de qualidade configuradas
- ✅ Framework de testes pronto
- ✅ Documentação base criada

---

## Objetivos da Sprint

### Objetivo Principal
Estabelecer fundação sólida e profissional para o desenvolvimento do justiceai

### Objetivos Específicos
1. **Setup Técnico**: Poetry, estrutura de diretórios, Git
2. **Qualidade**: Linters, formatters, type checkers configurados
3. **CI/CD**: GitHub Actions funcionando
4. **Testes**: Pytest configurado com coverage
5. **Documentação**: README, CONTRIBUTING, LICENSE

---

## User Stories

### 🎯 US-001: Setup Projeto com Poetry

**Prioridade**: 🔴 CRITICAL
**Estimativa**: 3 SP (4 horas)
**Status**: ⏳ TODO

#### User Story
> Como **desenvolvedor**,
> Eu quero um **projeto Python estruturado com Poetry**,
> Para **gerenciar dependências de forma profissional**

#### Critérios de Aceite
- [ ] `pyproject.toml` configurado com todas dependências
- [ ] Poetry lock file gerado
- [ ] Comandos `poetry install` e `poetry shell` funcionando
- [ ] Estrutura de diretórios criada (conforme arquitetura)
- [ ] `.gitignore` configurado
- [ ] README.md inicial criado

#### Tarefas Técnicas
```bash
# 1. Instalar Poetry
curl -sSL https://install.python-poetry.org | python3 -

# 2. Inicializar projeto
poetry init --name justiceai \
            --description "Fairness analysis for ML in production" \
            --author "Gustavo Haase <gustavo.haase@gmail.com>" \
            --python ">=3.10,<3.13" \
            --license MIT

# 3. Adicionar dependências core
poetry add numpy pandas scikit-learn scipy plotly jinja2 pydantic

# 4. Adicionar dependências dev
poetry add --group dev pytest pytest-cov black ruff mypy pylint isort pre-commit

# 5. Adicionar dependências docs
poetry add --group docs mkdocs-material mkdocstrings-python

# 6. Instalar tudo
poetry install

# 7. Criar estrutura de diretórios
mkdir -p justiceai/{core/{metrics,evaluators,adapters},reports/{transformers,renderers,templates},compliance,monitoring,utils}
mkdir -p tests/{core/{metrics,evaluators,adapters},reports,compliance,monitoring,utils}
mkdir -p docs examples/{notebooks,scripts}

# 8. Criar __init__.py em todos os módulos
find justiceai -type d -exec touch {}/__init__.py \;
find tests -type d -exec touch {}/__init__.py \;
```

#### Definition of Done
- [x] Código: `poetry install` funciona sem erros
- [x] Estrutura de diretórios criada
- [x] `import justiceai` funciona
- [x] Git inicializado com commit inicial
- [x] PR criado e aprovado
- [x] Documentado em README

#### Referências
- Guia: `/home/guhaase/projetos/DeepBridge/desenvolvimento/GUIA_BUILD_PUBLICACAO_PYTHON.md`
- Template: DeepBridge `pyproject.toml`

---

### 🎯 US-002: CI/CD com GitHub Actions

**Prioridade**: 🔴 CRITICAL
**Estimativa**: 5 SP (6 horas)
**Status**: ⏳ TODO

#### User Story
> Como **desenvolvedor**,
> Eu quero **pipeline CI/CD automatizado**,
> Para **garantir qualidade em cada commit**

#### Critérios de Aceite
- [ ] Workflow de testes (`test.yml`)
- [ ] Workflow de linting (`quality.yml`)
- [ ] Workflow de build (`build.yml`)
- [ ] Badges no README (build, coverage, Python versions)
- [ ] Testes rodam em Python 3.10, 3.11, 3.12
- [ ] Coverage report enviado para Codecov

#### Tarefas Técnicas
- [ ] Criar `.github/workflows/test.yml`:
  - Matrix: Python 3.10, 3.11, 3.12
  - Matrix: OS ubuntu-latest, macos-latest, windows-latest
  - Rodar `pytest --cov`
  - Upload para Codecov
- [ ] Criar `.github/workflows/quality.yml`:
  - Check: Black formatação
  - Check: isort imports
  - Check: MyPy types
  - Check: Ruff linting
- [ ] Criar `.github/workflows/build.yml`:
  - Build wheel e sdist
  - Validar com twine check
- [ ] Configurar Codecov:
  - Criar conta em codecov.io
  - Adicionar token em GitHub Secrets
  - Configurar `codecov.yml`
- [ ] Adicionar badges ao README.md

#### Definition of Done
- [x] Workflows executam em cada PR
- [x] Testes passam em 3 versões Python
- [x] Coverage > 80% (inicial)
- [x] Badges funcionando no README
- [x] CI documentado em CONTRIBUTING.md

#### Referências
- Template: DeepBridge `.github/workflows/`
- Docs: https://docs.github.com/actions

---

### 🎯 US-003: Configurar Linters e Formatters

**Prioridade**: 🔴 CRITICAL
**Estimativa**: 3 SP (4 horas)
**Status**: ⏳ TODO

#### User Story
> Como **desenvolvedor**,
> Eu quero **ferramentas de qualidade configuradas**,
> Para **manter código consistente e limpo**

#### Critérios de Aceite
- [ ] Black configurado (line-length=88)
- [ ] Ruff configurado
- [ ] MyPy configurado (strict mode)
- [ ] Pylint configurado
- [ ] isort configurado
- [ ] Pre-commit hooks instalados
- [ ] Makefile com comandos `lint`, `format`, `test`

#### Tarefas Técnicas
```toml
# Adicionar em pyproject.toml

[tool.black]
line-length = 88
target-version = ['py310', 'py311', 'py312']

[tool.isort]
profile = "black"
line_length = 88

[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true

[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP", "ARG", "SIM"]
ignore = ["E501"]
```

```yaml
# Criar .pre-commit-config.yaml
repos:
  - repo: https://github.com/pre-commit/pre-commit-hooks
    rev: v4.5.0
    hooks:
      - id: trailing-whitespace
      - id: end-of-file-fixer
      - id: check-yaml
      - id: check-added-large-files

  - repo: https://github.com/psf/black
    rev: 24.1.1
    hooks:
      - id: black

  - repo: https://github.com/pycqa/isort
    rev: 5.13.2
    hooks:
      - id: isort

  - repo: https://github.com/astral-sh/ruff-pre-commit
    rev: v0.1.15
    hooks:
      - id: ruff
        args: [--fix]
```

```makefile
# Criar Makefile
.PHONY: help install test lint format type-check quality clean

help:
	@echo "Comandos disponíveis:"
	@echo "  make install     - Instala dependências"
	@echo "  make test        - Executa testes"
	@echo "  make lint        - Executa linters"
	@echo "  make format      - Formata código"
	@echo "  make type-check  - Verifica tipos"
	@echo "  make quality     - Executa todos checks"
	@echo "  make clean       - Remove arquivos temporários"

install:
	poetry install

test:
	pytest

lint:
	ruff check justiceai/ tests/
	pylint justiceai/

format:
	black justiceai/ tests/
	isort justiceai/ tests/
	ruff check --fix justiceai/ tests/

type-check:
	mypy justiceai/

quality: format lint type-check test

clean:
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/
	rm -rf htmlcov/ .coverage
	find . -type d -name __pycache__ -exec rm -rf {} +
```

#### Definition of Done
- [x] Todas configs em `pyproject.toml`
- [x] Pre-commit hooks instalados
- [x] `make quality` passa sem erros
- [x] Documentado em README

#### Referências
- Guia: `GUIA_QUALIDADE_CODIGO_PYTHON.md`

---

### 🎯 US-004: Setup de Testes com Pytest

**Prioridade**: 🔴 CRITICAL
**Estimativa**: 3 SP (4 horas)
**Status**: ⏳ TODO

#### User Story
> Como **desenvolvedor**,
> Eu quero **framework de testes configurado**,
> Para **escrever testes desde o início**

#### Critérios de Aceite
- [ ] Pytest instalado e configurado
- [ ] Pytest-cov configurado (target 90%)
- [ ] Estrutura `tests/` criada
- [ ] Fixtures básicos criados
- [ ] Teste dummy passando
- [ ] Coverage report funcionando

#### Tarefas Técnicas
```toml
# Adicionar em pyproject.toml

[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = [
    "--verbose",
    "--cov=justiceai",
    "--cov-report=term-missing",
    "--cov-report=html",
]

[tool.coverage.run]
source = ["justiceai"]
omit = ["*/tests/*"]
branch = true

[tool.coverage.report]
precision = 2
show_missing = true
fail_under = 90
exclude_lines = [
    "pragma: no cover",
    "def __repr__",
    "raise NotImplementedError",
    "if __name__ == .__main__.:",
    "if TYPE_CHECKING:",
]
```

```python
# tests/conftest.py
import pytest
import pandas as pd
from sklearn.ensemble import RandomForestClassifier

@pytest.fixture
def sample_data():
    """Sample dataset for testing."""
    return pd.DataFrame({
        'feature1': [1, 2, 3, 4, 5],
        'feature2': [2, 4, 6, 8, 10],
        'sensitive_attr': ['A', 'B', 'A', 'B', 'A'],
        'label': [0, 1, 0, 1, 0]
    })

@pytest.fixture
def sample_model():
    """Sample ML model for testing."""
    return RandomForestClassifier(random_state=42)
```

```python
# tests/test_import.py
"""Test basic imports."""

def test_import_justiceai():
    """Test that justiceai can be imported."""
    import justiceai

    assert justiceai.__version__ == "0.1.0"
    assert justiceai.__author__ == "Gustavo Haase"
```

#### Definition of Done
- [x] `pytest` executa sem erros
- [x] Coverage configurado (target 90%)
- [x] Fixtures básicos criados
- [x] Pelo menos 1 teste passando
- [x] Documentado como rodar testes

---

### 🎯 US-005: Documentação Inicial

**Prioridade**: 🟠 HIGH
**Estimativa**: 5 SP (6 horas)
**Status**: ⏳ TODO

#### User Story
> Como **usuário potencial**,
> Eu quero **documentação clara do projeto**,
> Para **entender o que é e como usar**

#### Critérios de Aceite
- [ ] README.md completo com:
  - Descrição do projeto
  - Badges (build, coverage, Python, license)
  - Quick start
  - Instalação
  - Exemplo básico
  - Contribuindo
  - Licença
- [ ] LICENSE criada (MIT)
- [ ] CHANGELOG.md iniciado
- [ ] CONTRIBUTING.md criado

#### Tarefas Técnicas
- [ ] Escrever README.md completo
- [ ] Criar LICENSE (MIT)
- [ ] Criar CHANGELOG.md (Keep a Changelog format)
- [ ] Criar CONTRIBUTING.md
- [ ] Criar `.github/ISSUE_TEMPLATE/bug_report.md`
- [ ] Criar `.github/ISSUE_TEMPLATE/feature_request.md`
- [ ] Criar `.github/PULL_REQUEST_TEMPLATE.md`

#### Definition of Done
- [x] README completo e renderiza bem
- [x] LICENSE presente (MIT)
- [x] CHANGELOG.md criado
- [x] CONTRIBUTING.md criado
- [x] Templates de issue/PR criados

---

### 🎯 US-006: Estrutura de Módulos Base

**Prioridade**: 🔴 CRITICAL
**Estimativa**: 2 SP (2 horas)
**Status**: ⏳ TODO

#### User Story
> Como **desenvolvedor**,
> Eu quero **estrutura de módulos criada**,
> Para **começar implementação organizada**

#### Critérios de Aceite
- [ ] `justiceai/__init__.py` com `__version__`
- [ ] `justiceai/core/` criado
- [ ] `justiceai/core/metrics/` criado
- [ ] `justiceai/reports/` criado
- [ ] `justiceai/utils/` criado
- [ ] Todos `__init__.py` criados
- [ ] Imports funcionando

#### Tarefas Técnicas
```python
# justiceai/__init__.py
"""
justiceai - Fairness Analysis for ML in Production

A Python library for fairness analysis in machine learning,
focused on production monitoring and Brazilian compliance (LGPD/BACEN).
"""

__version__ = "0.1.0"
__author__ = "Gustavo Haase"
__email__ = "gustavo.haase@gmail.com"
__license__ = "MIT"

# High-level API (will be implemented in Sprint 1)
# from justiceai.api import audit
# __all__ = ["audit"]

__all__ = []
```

#### Definition of Done
- [x] Estrutura completa criada
- [x] Todos `__init__.py` presentes
- [x] `import justiceai` funciona
- [x] Testes de import passam
- [x] MyPy passa (com ignores temporários OK)

---

## Definition of Done

### DoD - User Story
Uma user story está "Pronta" quando:
- [ ] Código implementado e revisado (PR aprovado)
- [ ] Testes escritos (coverage ≥ 90% para código novo)
- [ ] Type hints em 100% das funções públicas
- [ ] Docstrings (Google style) em todas APIs públicas
- [ ] Linting: Zero warnings (black, ruff, mypy, pylint)
- [ ] Integração: Passa em CI/CD
- [ ] Exemplos: Pelo menos 1 exemplo de uso documentado
- [ ] Aceite PO: Product Owner validou funcionalidade

### DoD - Sprint
Esta sprint está "Pronta" quando:
- [ ] Todas as stories comprometidas foram completadas (DoD)
- [ ] Regression tests passam 100%
- [ ] Documentação atualizada (README, CHANGELOG)
- [ ] Demo realizada (interno ou para early adopters)
- [ ] Retrospectiva realizada
- [ ] Backlog refinado para próxima sprint

---

## Tarefas Técnicas

### Semana 1 (8-14 Fev)
- [x] Dia 1-2: US-001 (Setup Poetry)
- [x] Dia 3: US-002 (CI/CD) - parte 1
- [x] Dia 4: US-003 (Linters)
- [x] Dia 5: US-004 (Testes)

### Semana 2 (15-21 Fev)
- [ ] Dia 1: US-002 (CI/CD) - finalizar
- [ ] Dia 2-3: US-005 (Documentação)
- [ ] Dia 4: US-006 (Estrutura módulos)
- [ ] Dia 5: Sprint Review + Retrospectiva

---

## Métricas de Sucesso

| Métrica | Target | Medição |
|---------|--------|---------|
| **Stories Completadas** | 6/6 | 100% |
| **Code Coverage** | ≥ 80% | pytest-cov |
| **CI Passing** | 100% | GitHub Actions |
| **Linting Score** | 10/10 | ruff + pylint |
| **Type Coverage** | 100% APIs públicas | mypy |
| **Documentação** | README completo | Manual review |

---

## Riscos e Mitigações

| Risco | Probabilidade | Impacto | Mitigação |
|-------|---------------|---------|-----------|
| **R1**: Dependências quebradas | BAIXA | MÉDIO | Pin versões, test em múltiplas versões Python |
| **R2**: CI/CD complexo demais | MÉDIA | BAIXO | Começar simples, iterar |
| **R3**: Time indisponível | MÉDIA | ALTO | Buffer 20% em estimativas |

---

## Entregáveis

Ao final da Sprint 0, teremos:

### 📦 Código
- ✅ Projeto estruturado com Poetry
- ✅ Estrutura de diretórios completa
- ✅ `justiceai` importável
- ✅ Testes básicos passando

### 🔧 Infraestrutura
- ✅ CI/CD completo (GitHub Actions)
- ✅ Linters e formatters configurados
- ✅ Pre-commit hooks instalados
- ✅ Codecov integrado

### 📚 Documentação
- ✅ README.md completo
- ✅ LICENSE (MIT)
- ✅ CHANGELOG.md iniciado
- ✅ CONTRIBUTING.md
- ✅ Templates de issue/PR

### 📊 Qualidade
- ✅ Coverage ≥ 80%
- ✅ CI passing
- ✅ Zero linting warnings
- ✅ Type hints configurados

---

## Sprint Review

**Data**: 21 Fev 2026 (final da Sprint 0)

**Agenda**:
1. Demo de entregáveis (15 min)
2. Métricas da sprint (5 min)
3. Feedback e ajustes (10 min)

**Participantes**: Time + stakeholders

---

## Sprint Retrospectiva

**Data**: 21 Fev 2026 (após Review)

**Agenda**:
1. O que funcionou bem? (10 min)
2. O que pode melhorar? (10 min)
3. Action items para próxima sprint (5 min)

**Participantes**: Time apenas

---

**Status**: ⏳ TODO
**Última Atualização**: 2026-02-08
**Próxima Sprint**: Sprint 1 (Métricas Core)
