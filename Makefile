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
	poetry run pytest

test-cov:
	poetry run pytest --cov --cov-report=html
	@echo "Abra: htmlcov/index.html"

lint:
	poetry run ruff check justiceai/ tests/
	poetry run pylint justiceai/

format:
	poetry run black justiceai/ tests/
	poetry run isort justiceai/ tests/
	poetry run ruff check --fix justiceai/ tests/

type-check:
	poetry run mypy justiceai/

quality: format lint type-check test

clean:
	rm -rf build/ dist/ *.egg-info
	rm -rf .pytest_cache/ .mypy_cache/ .ruff_cache/
	rm -rf htmlcov/ .coverage
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
