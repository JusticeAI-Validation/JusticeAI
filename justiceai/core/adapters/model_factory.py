"""
Model adapter factory for automatic model type detection.

This module provides automatic detection and instantiation of the
appropriate adapter for a given model.
"""

from typing import Any

from justiceai.core.adapters.base_adapter import BaseModelAdapter
from justiceai.core.adapters.sklearn_adapter import SklearnAdapter


def create_adapter(model: Any) -> BaseModelAdapter:
    """
    Automatically create appropriate adapter for model.

    Detects the model type and returns the corresponding adapter.

    Args:
        model: ML model instance from any supported framework

    Returns:
        Appropriate adapter instance

    Raises:
        ValueError: If model type is not supported

    Example:
        >>> from sklearn.ensemble import RandomForestClassifier
        >>> from justiceai.core.adapters import create_adapter
        >>>
        >>> model = RandomForestClassifier()
        >>> model.fit(X_train, y_train)
        >>>
        >>> adapter = create_adapter(model)  # Auto-detects sklearn
        >>> predictions = adapter.predict(X_test)
    """
    model_class_name = type(model).__name__
    model_module = type(model).__module__

    # Check if it's a scikit-learn model
    if "sklearn" in model_module:
        return SklearnAdapter(model)

    # Check if it's XGBoost
    if "xgboost" in model_module or model_class_name.startswith("XGB"):
        try:
            from justiceai.core.adapters.xgboost_adapter import XGBoostAdapter

            return XGBoostAdapter(model)
        except ImportError:
            raise ValueError(
                "XGBoost adapter requires xgboost to be installed. "
                "Install with: pip install xgboost"
            )

    # Check if it's LightGBM
    if "lightgbm" in model_module or model_class_name.startswith("LGBM"):
        try:
            from justiceai.core.adapters.lightgbm_adapter import LightGBMAdapter

            return LightGBMAdapter(model)
        except ImportError:
            raise ValueError(
                "LightGBM adapter requires lightgbm to be installed. "
                "Install with: pip install lightgbm"
            )

    # If model has predict method, try sklearn adapter as fallback
    if hasattr(model, "predict"):
        return SklearnAdapter(model)

    # Model type not supported
    raise ValueError(
        f"Unsupported model type: {model_class_name} from {model_module}. "
        f"Supported frameworks: scikit-learn, XGBoost, LightGBM. "
        f"Model must have a 'predict' method."
    )


def is_model_supported(model: Any) -> bool:
    """
    Check if model type is supported.

    Args:
        model: ML model instance

    Returns:
        True if model is supported, False otherwise

    Example:
        >>> from sklearn.linear_model import LogisticRegression
        >>> model = LogisticRegression()
        >>> is_model_supported(model)
        True
    """
    try:
        create_adapter(model)
        return True
    except (ValueError, ImportError):
        return False
