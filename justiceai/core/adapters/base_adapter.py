"""
Base adapter for ML model integration.

This module provides the base interface for model adapters that allow
JusticeAI to work with different ML frameworks.
"""

from abc import ABC, abstractmethod
from typing import Any

import numpy as np


class BaseModelAdapter(ABC):
    """
    Abstract base class for model adapters.

    Model adapters allow JusticeAI to work with models from different
    frameworks (scikit-learn, XGBoost, LightGBM, ONNX, etc.) by providing
    a unified interface for predictions.

    Example:
        >>> class MyAdapter(BaseModelAdapter):
        ...     def predict(self, X):
        ...         return self.model.predict(X)
        ...
        ...     def predict_proba(self, X):
        ...         return self.model.predict_proba(X)
    """

    def __init__(self, model: Any):
        """
        Initialize adapter with model.

        Args:
            model: ML model instance
        """
        self.model = model
        self._validate_model()

    def _validate_model(self) -> None:
        """
        Validate that model has required methods.

        Raises:
            ValueError: If model is missing required methods
        """
        if not hasattr(self.model, "predict"):
            raise ValueError(
                f"Model {type(self.model).__name__} must have a 'predict' method"
            )

    @abstractmethod
    def predict(self, X: np.ndarray | Any) -> np.ndarray:
        """
        Make predictions using the model.

        Args:
            X: Input features

        Returns:
            Predicted labels (binary: 0 or 1)
        """
        pass

    def predict_proba(self, X: np.ndarray | Any) -> np.ndarray | None:
        """
        Get prediction probabilities.

        Args:
            X: Input features

        Returns:
            Predicted probabilities or None if not supported

        Note:
            Returns None if model doesn't support probability predictions.
            Subclasses should override to provide probabilities when available.
        """
        return None

    @property
    def supports_proba(self) -> bool:
        """
        Check if model supports probability predictions.

        Returns:
            True if predict_proba is available
        """
        return hasattr(self.model, "predict_proba")

    @property
    def model_type(self) -> str:
        """
        Get model type string.

        Returns:
            String identifying the model type
        """
        return type(self.model).__name__
