# Contributing to JusticeAI

Thank you for your interest in contributing to JusticeAI! This document provides guidelines for contributing.

## Code of Conduct

Be respectful, inclusive, and constructive in all interactions.

## How to Contribute

### Reporting Bugs

[Open an issue](https://github.com/JusticeAI-Validation/JusticeAI/issues/new) with:
- Python and JusticeAI versions
- Minimal code to reproduce
- Expected vs actual behavior
- Error messages/traceback

### Suggesting Features

[Open a feature request](https://github.com/JusticeAI-Validation/JusticeAI/issues/new) describing:
- Use case and motivation
- Proposed solution
- Alternative approaches considered

### Pull Requests

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests
5. Run the test suite
6. Commit your changes
7. Push to your fork
8. Open a Pull Request

## Development Setup

```bash
# Clone your fork
git clone https://github.com/YOUR_USERNAME/JusticeAI.git
cd JusticeAI

# Install dependencies
poetry install --with dev

# Run tests
poetry run pytest

# Run tests with coverage
poetry run pytest --cov=justiceai --cov-report=html

# Format code
poetry run ruff format .

# Type checking
poetry run mypy justiceai
```

## Code Standards

### Style

- Follow PEP 8
- Use type hints (mypy --strict)
- Maximum line length: 100 characters
- Use ruff for formatting

### Testing

- Write tests for all new features
- Maintain 90%+ code coverage
- Use pytest
- Follow existing test patterns

### Documentation

- Add Google-style docstrings
- Update relevant documentation
- Include code examples in docstrings
- Update CHANGELOG.md

## Project Structure

```
justiceai/
├── justiceai/          # Main package
│   ├── core/           # Core functionality
│   ├── reports/        # Report generation
│   └── compliance/     # Compliance features
├── tests/              # Test suite
├── docs/               # Documentation
└── desenvolvimento/    # Sprint planning
```

## Testing Guidelines

```python
# Test naming convention
def test_<function>_<scenario>():
    """Test <function> <scenario>."""
    # Arrange
    # Act
    # Assert

# Use fixtures
@pytest.fixture
def sample_data():
    return create_test_data()

# Use parametrize for multiple scenarios
@pytest.mark.parametrize("input,expected", [
    (1, 2),
    (2, 4),
])
def test_double(input, expected):
    assert double(input) == expected
```

## Commit Messages

Follow conventional commits:

```
feat: add XGBoost adapter
fix: correct statistical parity calculation
docs: update quickstart guide
test: add tests for FairnessReport
refactor: simplify metric calculator
```

## Pull Request Process

1. **Update Documentation**: Ensure docs reflect your changes
2. **Add Tests**: New code needs tests
3. **Pass CI**: All tests and checks must pass
4. **Update CHANGELOG**: Add entry for your changes
5. **Request Review**: Tag maintainers for review

## Code Review

Reviewers will check:
- Code quality and style
- Test coverage
- Documentation
- Performance implications
- Backward compatibility

## Release Process

Releases follow semantic versioning (MAJOR.MINOR.PATCH):

- **MAJOR**: Breaking changes
- **MINOR**: New features (backward compatible)
- **PATCH**: Bug fixes

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

## Questions?

- 📖 [Documentation](https://justiceai-validation.github.io/JusticeAI/)
- 💬 [Discussions](https://github.com/JusticeAI-Validation/JusticeAI/discussions)
- 📧 Email: gustavo.haase@gmail.com
