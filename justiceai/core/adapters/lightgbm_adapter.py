"""
LightGBM model adapter.

This module provides an adapter for LightGBM models to work with JusticeAI.
"""

from typing import Any

import numpy as np

from justiceai.core.adapters.base_adapter import BaseModelAdapter


class LightGBMAdapter(BaseModelAdapter):
    """
    Adapter for LightGBM models.

    This adapter allows LightGBM classifiers to be used with JusticeAI's
    fairness evaluation tools.

    Supported models:
        - lightgbm.LGBMClassifier
        - lightgbm.Booster (trained for classification)

    Example:
        >>> import lightgbm as lgb
        >>> from justiceai.core.adapters import LightGBMAdapter
        >>>
        >>> # Train LightGBM model
        >>> model = lgb.LGBMClassifier()
        >>> model.fit(X_train, y_train)
        >>>
        >>> # Create adapter
        >>> adapter = LightGBMAdapter(model)
        >>> predictions = adapter.predict(X_test)
        >>> probabilities = adapter.predict_proba(X_test)
    """

    def __init__(self, model: Any):
        """
        Initialize LightGBM adapter.

        Args:
            model: LightGBM model instance (LGBMClassifier or Booster)

        Raises:
            ValueError: If model is not a valid LightGBM model
        """
        super().__init__(model)

    def _validate_model(self) -> None:
        """
        Validate that model is a valid LightGBM model.

        Raises:
            ValueError: If model doesn't have required LightGBM methods
        """
        model_class = type(self.model).__name__

        # Check if it's LGBMClassifier (has predict method)
        if hasattr(self.model, "predict"):
            return

        # Check if it's Booster (has predict method)
        if model_class == "Booster" and hasattr(self.model, "predict"):
            return

        raise ValueError(
            f"Model {model_class} must be a LightGBM model "
            f"(LGBMClassifier or Booster) with a 'predict' method"
        )

    def predict(self, X: np.ndarray | Any) -> np.ndarray:
        """
        Generate predictions using LightGBM model.

        Args:
            X: Features to predict on (numpy array or pandas DataFrame)

        Returns:
            Binary predictions (0 or 1) as numpy array

        Example:
            >>> predictions = adapter.predict(X_test)
            >>> predictions
            array([0, 1, 1, 0, 1])
        """
        model_class = type(self.model).__name__

        # Handle LGBMClassifier
        if model_class == "LGBMClassifier":
            predictions = self.model.predict(X)
            return np.asarray(predictions)

        # Handle Booster
        if model_class == "Booster":
            # Booster.predict returns probabilities by default
            probas = self.model.predict(X)

            # Handle multi-dimensional output
            if len(probas.shape) == 2:
                # Multi-class: use argmax
                predictions = np.argmax(probas, axis=1)
            else:
                # Binary: threshold at 0.5
                predictions = (probas > 0.5).astype(int)

            return predictions

        # Fallback to direct predict
        predictions = self.model.predict(X)
        return np.asarray(predictions)

    def predict_proba(self, X: np.ndarray | Any) -> np.ndarray | None:
        """
        Generate probability predictions using LightGBM model.

        Args:
            X: Features to predict on (numpy array or pandas DataFrame)

        Returns:
            Probabilities for positive class (class 1) as numpy array,
            or None if model doesn't support probabilities

        Example:
            >>> probabilities = adapter.predict_proba(X_test)
            >>> probabilities
            array([0.23, 0.87, 0.65, 0.12, 0.91])
        """
        if not self.supports_proba:
            return None

        model_class = type(self.model).__name__

        # Handle LGBMClassifier
        if hasattr(self.model, "predict_proba"):
            proba = self.model.predict_proba(X)
            # Return probability of positive class for binary classification
            if len(proba.shape) == 2 and proba.shape[1] == 2:
                return proba[:, 1]
            return proba

        # Handle Booster
        if model_class == "Booster":
            probas = self.model.predict(X)

            # Handle multi-dimensional output
            if len(probas.shape) == 2 and probas.shape[1] == 2:
                # Binary classification: return positive class
                return probas[:, 1]

            # Already probabilities
            return probas

        return None

    @property
    def supports_proba(self) -> bool:
        """
        Check if model supports probability predictions.

        Returns:
            True if model can generate probabilities, False otherwise

        Note:
            LightGBM models generally support probability predictions
            for classification tasks.
        """
        # LGBMClassifier always supports probabilities
        if hasattr(self.model, "predict_proba"):
            return True

        # Booster supports probabilities for classification
        if type(self.model).__name__ == "Booster":
            return True

        return False
