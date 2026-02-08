"""
XGBoost model adapter.

This module provides an adapter for XGBoost models to work with JusticeAI.
"""

from typing import Any

import numpy as np

from justiceai.core.adapters.base_adapter import BaseModelAdapter


class XGBoostAdapter(BaseModelAdapter):
    """
    Adapter for XGBoost models.

    This adapter allows XGBoost classifiers to be used with JusticeAI's
    fairness evaluation tools.

    Supported models:
        - xgboost.XGBClassifier
        - xgboost.Booster (trained with binary:logistic)

    Example:
        >>> import xgboost as xgb
        >>> from justiceai.core.adapters import XGBoostAdapter
        >>>
        >>> # Train XGBoost model
        >>> model = xgb.XGBClassifier()
        >>> model.fit(X_train, y_train)
        >>>
        >>> # Create adapter
        >>> adapter = XGBoostAdapter(model)
        >>> predictions = adapter.predict(X_test)
        >>> probabilities = adapter.predict_proba(X_test)
    """

    def __init__(self, model: Any):
        """
        Initialize XGBoost adapter.

        Args:
            model: XGBoost model instance (XGBClassifier or Booster)

        Raises:
            ValueError: If model is not a valid XGBoost model
        """
        super().__init__(model)

    def _validate_model(self) -> None:
        """
        Validate that model is a valid XGBoost model.

        Raises:
            ValueError: If model doesn't have required XGBoost methods
        """
        model_class = type(self.model).__name__

        # Check if it's XGBClassifier (has predict method)
        if hasattr(self.model, "predict"):
            return

        # Check if it's Booster (has predict method with different signature)
        if model_class == "Booster" and hasattr(self.model, "predict"):
            return

        raise ValueError(
            f"Model {model_class} must be an XGBoost model "
            f"(XGBClassifier or Booster) with a 'predict' method"
        )

    def predict(self, X: np.ndarray | Any) -> np.ndarray:
        """
        Generate predictions using XGBoost model.

        Args:
            X: Features to predict on (numpy array or xgboost.DMatrix)

        Returns:
            Binary predictions (0 or 1) as numpy array

        Example:
            >>> predictions = adapter.predict(X_test)
            >>> predictions
            array([0, 1, 1, 0, 1])
        """
        # Handle XGBClassifier
        if hasattr(self.model, "predict"):
            predictions = self.model.predict(X)
            return np.asarray(predictions)

        # Handle Booster - need DMatrix
        try:
            import xgboost as xgb

            if not isinstance(X, xgb.DMatrix):
                X = xgb.DMatrix(X)

            # Booster.predict returns probabilities
            probas = self.model.predict(X)
            # Convert to binary predictions
            predictions = (probas > 0.5).astype(int)
            return predictions
        except ImportError:
            raise ImportError(
                "xgboost is required to use XGBoostAdapter. "
                "Install with: pip install xgboost"
            )

    def predict_proba(self, X: np.ndarray | Any) -> np.ndarray | None:
        """
        Generate probability predictions using XGBoost model.

        Args:
            X: Features to predict on (numpy array or xgboost.DMatrix)

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

        # Handle XGBClassifier
        if hasattr(self.model, "predict_proba"):
            proba = self.model.predict_proba(X)
            # Return probability of positive class
            if proba.shape[1] == 2:
                return proba[:, 1]
            return proba

        # Handle Booster
        try:
            import xgboost as xgb

            if not isinstance(X, xgb.DMatrix):
                X = xgb.DMatrix(X)

            # Booster.predict returns probabilities directly
            probas = self.model.predict(X)
            return probas
        except ImportError:
            raise ImportError(
                "xgboost is required to use XGBoostAdapter. "
                "Install with: pip install xgboost"
            )

    @property
    def supports_proba(self) -> bool:
        """
        Check if model supports probability predictions.

        Returns:
            True if model can generate probabilities, False otherwise

        Note:
            XGBoost models trained with binary:logistic objective
            support probability predictions.
        """
        # XGBClassifier always supports probabilities
        if hasattr(self.model, "predict_proba"):
            return True

        # Booster supports probabilities if objective is binary:logistic
        if type(self.model).__name__ == "Booster":
            # Assume Booster supports probabilities (most common case)
            return True

        return False
