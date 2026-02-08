"""
Scikit-learn model adapter.

Adapter for scikit-learn models.
"""

from typing import Any

import numpy as np

from justiceai.core.adapters.base_adapter import BaseModelAdapter


class SklearnAdapter(BaseModelAdapter):
    """
    Adapter for scikit-learn models.

    Supports any scikit-learn classifier with predict() and optionally
    predict_proba() methods.

    Example:
        >>> from sklearn.ensemble import RandomForestClassifier
        >>> from justiceai.core.adapters import SklearnAdapter
        >>>
        >>> model = RandomForestClassifier()
        >>> model.fit(X_train, y_train)
        >>>
        >>> adapter = SklearnAdapter(model)
        >>> predictions = adapter.predict(X_test)
        >>> probabilities = adapter.predict_proba(X_test)
    """

    def predict(self, X: np.ndarray | Any) -> np.ndarray:
        """
        Make predictions using scikit-learn model.

        Args:
            X: Input features (numpy array or pandas DataFrame)

        Returns:
            Predicted labels as numpy array
        """
        predictions = self.model.predict(X)
        return np.asarray(predictions)

    def predict_proba(self, X: np.ndarray | Any) -> np.ndarray | None:
        """
        Get prediction probabilities from scikit-learn model.

        Args:
            X: Input features

        Returns:
            Probability array or None if not supported

        Note:
            Returns probabilities for the positive class (index 1).
        """
        if not self.supports_proba:
            return None

        proba = self.model.predict_proba(X)
        # Return probabilities for positive class
        if proba.shape[1] == 2:
            return proba[:, 1]
        return proba
