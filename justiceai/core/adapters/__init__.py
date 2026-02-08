"""
Model adapters for framework-agnostic ML integration.

This module provides adapters to work with models from different
ML frameworks (scikit-learn, XGBoost, LightGBM, etc.).

Main components:
    - BaseModelAdapter: Abstract base class
    - SklearnAdapter: For scikit-learn models
    - create_adapter: Auto-detect and create adapter
    - is_model_supported: Check if model is supported

Example:
    >>> from justiceai.core.adapters import create_adapter
    >>> adapter = create_adapter(model)
    >>> predictions = adapter.predict(X_test)
"""

from justiceai.core.adapters.base_adapter import BaseModelAdapter
from justiceai.core.adapters.model_factory import create_adapter, is_model_supported
from justiceai.core.adapters.sklearn_adapter import SklearnAdapter

__all__ = [
    "BaseModelAdapter",
    "SklearnAdapter",
    "create_adapter",
    "is_model_supported",
]
