"""
Model adapters for framework-agnostic ML integration.

This module provides adapters to work with models from different
ML frameworks (scikit-learn, XGBoost, LightGBM, etc.).

Main components:
    - BaseModelAdapter: Abstract base class
    - SklearnAdapter: For scikit-learn models
    - XGBoostAdapter: For XGBoost models (optional)
    - LightGBMAdapter: For LightGBM models (optional)
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

# Optional adapters (imported only if dependencies are installed)
try:
    from justiceai.core.adapters.xgboost_adapter import XGBoostAdapter
except ImportError:
    XGBoostAdapter = None  # type: ignore

try:
    from justiceai.core.adapters.lightgbm_adapter import LightGBMAdapter
except ImportError:
    LightGBMAdapter = None  # type: ignore

__all__ = [
    "BaseModelAdapter",
    "SklearnAdapter",
    "XGBoostAdapter",
    "LightGBMAdapter",
    "create_adapter",
    "is_model_supported",
]
