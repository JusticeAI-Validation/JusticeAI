# Installation

## Requirements

- Python 3.11 or higher
- pip or poetry

## Install from PyPI

```bash
pip install justiceai
```

## Install from Source

For development or to get the latest features:

```bash
# Clone the repository
git clone https://github.com/JusticeAI-Validation/JusticeAI.git
cd JusticeAI

# Install with poetry (recommended)
poetry install

# Or with pip
pip install -e .
```

## Optional Dependencies

### XGBoost Support

```bash
pip install justiceai[xgboost]
```

### LightGBM Support

```bash
pip install justiceai[lightgbm]
```

### All Optional Dependencies

```bash
pip install justiceai[all]
```

## Verify Installation

Test your installation:

```python
import justiceai

print(f"JusticeAI version: {justiceai.__version__}")

# Quick test
from justiceai import FairnessEvaluator
evaluator = FairnessEvaluator()
print("✓ Installation successful!")
```

## Development Installation

For contributors:

```bash
# Clone and install dev dependencies
git clone https://github.com/JusticeAI-Validation/JusticeAI.git
cd JusticeAI
poetry install --with dev

# Run tests
poetry run pytest

# Run with coverage
poetry run pytest --cov=justiceai

# Format code
poetry run ruff format .

# Type checking
poetry run mypy justiceai
```

## Troubleshooting

### Python Version Issues

JusticeAI requires Python 3.11+ due to scipy dependencies. If you get version errors:

```bash
# Check your Python version
python --version

# Use pyenv to install Python 3.11+
pyenv install 3.11.0
pyenv local 3.11.0
```

### Installation Errors

If you encounter installation errors:

1. **Update pip**: `pip install --upgrade pip`
2. **Check dependencies**: Ensure numpy and scipy can be installed
3. **Use virtual environment**: Always use venv or poetry

### Import Errors

If imports fail after installation:

```python
# Check installation location
import sys
print(sys.path)

# Reinstall in editable mode
pip install -e .
```

## Next Steps

- [Quick Start Guide](quickstart.md) - Your first fairness audit
- [Basic Concepts](concepts.md) - Understand fairness metrics
- [API Reference](../api/index.md) - Detailed API documentation
