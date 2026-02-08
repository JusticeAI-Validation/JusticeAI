# ✅ Próximos Passos - justiceai

**Data**: 2026-02-08
**Status**: 🎯 Pronto para Execução

---

## 🚀 Começando AGORA (Próximas 24 horas)

### ✅ Passo 1: Criar Repositório GitHub (15 min)

```bash
# 1. Criar repo no GitHub
# - Ir para: https://github.com/new
# - Nome: justiceai
# - Descrição: "Fairness analysis for ML in production - LGPD/BACEN compliance"
# - Público: ✅
# - README: ❌ (já temos)
# - .gitignore: Python
# - License: MIT

# 2. Clonar e adicionar arquivos existentes
cd /home/guhaase/projetos/justiceai

git init
git add .
git commit -m "docs: initial project planning and documentation

- Add comprehensive agile planning (PLANEJAMENTO_AGIL.md)
- Add detailed product backlog (PRODUCT_BACKLOG_DETALHADO.md)
- Add executive summary (RESUMO_EXECUTIVO.md)
- Add README with project overview
- Add INDEX for documentation navigation"

git branch -M main
git remote add origin https://github.com/guhaase/justiceai.git
git push -u origin main
```

**✅ Validação**: Acesse https://github.com/guhaase/justiceai e veja os arquivos

---

### ✅ Passo 2: Setup Projeto com Poetry (30 min)

```bash
# Ainda em /home/guhaase/projetos/justiceai

# 1. Instalar Poetry (se não tiver)
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

# 7. Ativar ambiente
poetry shell
```

**✅ Validação**: `poetry show` lista todas dependências

---

### ✅ Passo 3: Criar Estrutura de Diretórios (10 min)

```bash
# Criar estrutura completa
mkdir -p justiceai/{core/{metrics,evaluators,adapters},reports/{transformers,renderers,templates},compliance,monitoring,utils}
mkdir -p tests/{core/{metrics,evaluators,adapters},reports,compliance,monitoring,utils}
mkdir -p docs examples/{notebooks,scripts}

# Criar __init__.py em todos os módulos
find justiceai -type d -exec touch {}/__init__.py \;
find tests -type d -exec touch {}/__init__.py \;

# Criar justiceai/__init__.py principal
cat > justiceai/__init__.py << 'EOF'
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
EOF

# Criar .gitignore
cat > .gitignore << 'EOF'
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Virtual environments
venv/
ENV/
env/
.venv

# IDEs
.vscode/
.idea/
*.swp
*.swo
*~

# Testing
.pytest_cache/
.coverage
htmlcov/
.tox/
.mypy_cache/
.ruff_cache/

# Docs
docs/_build/
site/

# OS
.DS_Store
Thumbs.db
EOF
```

**✅ Validação**: `tree -L 2 justiceai` mostra estrutura

---

### ✅ Passo 4: Configurar Ferramentas de Qualidade (20 min)

```bash
# 1. Atualizar pyproject.toml com configs
cat >> pyproject.toml << 'EOF'

# Black
[tool.black]
line-length = 88
target-version = ['py310', 'py311', 'py312']

# isort
[tool.isort]
profile = "black"
line_length = 88

# MyPy
[tool.mypy]
python_version = "3.10"
strict = true
warn_return_any = true
warn_unused_configs = true

# Pytest
[tool.pytest.ini_options]
testpaths = ["tests"]
python_files = ["test_*.py"]
addopts = [
    "--verbose",
    "--cov=justiceai",
    "--cov-report=term-missing",
    "--cov-report=html",
]

# Coverage
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

# Ruff
[tool.ruff]
line-length = 88
target-version = "py310"

[tool.ruff.lint]
select = ["E", "W", "F", "I", "B", "C4", "UP", "ARG", "SIM"]
ignore = ["E501"]

[tool.ruff.lint.per-file-ignores]
"__init__.py" = ["F401"]
"tests/*" = ["S101", "ARG001"]

# Pylint
[tool.pylint.main]
py-version = "3.10"
jobs = 0

[tool.pylint.format]
max-line-length = 88
EOF

# 2. Criar Makefile
cat > Makefile << 'EOF'
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

test-cov:
	pytest --cov --cov-report=html
	@echo "Abra: htmlcov/index.html"

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
	find . -type f -name "*.pyc" -delete
EOF

# 3. Criar .pre-commit-config.yaml
cat > .pre-commit-config.yaml << 'EOF'
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
EOF

# 4. Instalar pre-commit hooks
pre-commit install

# 5. Criar teste dummy
cat > tests/test_import.py << 'EOF'
"""Test basic imports."""


def test_import_justiceai():
    """Test that justiceai can be imported."""
    import justiceai

    assert justiceai.__version__ == "0.1.0"
    assert justiceai.__author__ == "Gustavo Haase"
EOF
```

**✅ Validação**: `make quality` deve passar

---

### ✅ Passo 5: Criar LICENSE e CHANGELOG (5 min)

```bash
# 1. LICENSE (MIT)
cat > LICENSE << 'EOF'
MIT License

Copyright (c) 2026 Gustavo Haase

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOF

# 2. CHANGELOG.md
cat > CHANGELOG.md << 'EOF'
# Changelog

Todas as mudanças notáveis neste projeto serão documentadas neste arquivo.

O formato é baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/),
e este projeto adere ao [Semantic Versioning](https://semver.org/lang/pt-BR/).

## [Não lançado]

### Adicionado
- Planejamento completo do projeto (Agile/Scrum)
- Documentação inicial (README, RESUMO_EXECUTIVO, etc.)
- Setup com Poetry
- CI/CD com GitHub Actions (em breve)

## [0.1.0] - 2026-XX-XX (Sprint 0 Target)

### Adicionado
- Estrutura inicial do projeto
- Configuração de qualidade de código
- Testes básicos
- Documentação de planejamento

[Não lançado]: https://github.com/guhaase/justiceai/compare/v0.1.0...HEAD
[0.1.0]: https://github.com/guhaase/justiceai/releases/tag/v0.1.0
EOF
```

**✅ Validação**: Arquivos criados e commitados

---

## 📅 Próxima Semana (10-16 Fev)

### Segunda (10 Fev) - US-002: CI/CD

```bash
# Criar workflows GitHub Actions
mkdir -p .github/workflows

# 1. Workflow de testes
cat > .github/workflows/test.yml << 'EOF'
# (copiar do PRODUCT_BACKLOG_DETALHADO.md US-002)
EOF

# 2. Workflow de qualidade
cat > .github/workflows/quality.yml << 'EOF'
# (copiar do PRODUCT_BACKLOG_DETALHADO.md US-002)
EOF

# 3. Configurar Codecov
# - Criar conta em codecov.io
# - Adicionar token em GitHub Secrets

# 4. Push e verificar
git add .github/
git commit -m "ci: add GitHub Actions workflows"
git push
```

---

### Terça-Quarta (11-12 Fev) - US-003 a US-006

- **US-003**: Já fizemos! (linters configurados)
- **US-004**: Já fizemos! (pytest configurado)
- **US-005**: Criar CONTRIBUTING.md
- **US-006**: Já fizemos! (estrutura criada)

**Resultado**: Sprint 0 praticamente completa!

---

## 🎯 Próximo Milestone: Sprint 1 (17 Fev - 2 Mar)

### Objetivos

1. Implementar 15 métricas de fairness
2. Atingir coverage ≥ 90%
3. Benchmarks vs Fairlearn

### Preparação Necessária (esta semana)

- [ ] Estudar Fairlearn API
- [ ] Estudar AIF360 métricas
- [ ] Revisar DeepBridge `fairness/metrics.py`
- [ ] Preparar datasets de teste (Breast Cancer, Adult)

---

## 📞 Comunicação

### Daily Standups (Assíncrono)

**Canal**: GitHub Discussions (criar)

**Formato** (postar todo dia útil):
```
📅 [Data]

🟢 Ontem:
- Completei US-001 (setup Poetry)
- Iniciei US-002 (CI/CD)

🔵 Hoje:
- Finalizar US-002
- Começar US-005

🔴 Impedimentos:
- Nenhum (ou listar)
```

---

## ✅ Checklist de Hoje (8 Fev)

- [ ] Ler este arquivo completo
- [ ] Executar Passo 1: Criar repo GitHub
- [ ] Executar Passo 2: Setup Poetry
- [ ] Executar Passo 3: Criar estrutura
- [ ] Executar Passo 4: Configurar ferramentas
- [ ] Executar Passo 5: LICENSE + CHANGELOG
- [ ] Commit e push tudo
- [ ] Celebrar! 🎉 Sprint 0 começou!

---

## 🎉 Mensagem Final

**Parabéns!** Você tem agora:

✅ **Planejamento completo** (280 SP, 5 sprints)
✅ **Documentação profissional** (5 arquivos Markdown)
✅ **Estrutura de projeto** (Poetry, qualidade, CI/CD)
✅ **Roadmap claro** (MVP em 12 semanas)

**Próximo passo**: Executar os passos acima e começar a codar! 💻

---

**Criado**: 2026-02-08
**Autor**: Claude Code (baseado em planejamento de Gustavo Haase)
**Licença**: MIT
