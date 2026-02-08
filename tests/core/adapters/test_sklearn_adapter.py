"""Tests for sklearn adapter."""

import numpy as np
import pytest
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier

from justiceai.core.adapters import SklearnAdapter, create_adapter


class TestSklearnAdapter:
    """Tests for SklearnAdapter class."""

    @pytest.fixture
    def sample_data(self) -> tuple:
        """Create sample classification data."""
        X, y = make_classification(
            n_samples=100, n_features=5, n_classes=2, random_state=42
        )
        return X, y

    @pytest.fixture
    def trained_model(self, sample_data: tuple) -> RandomForestClassifier:
        """Create and train a simple model."""
        X, y = sample_data
        model = RandomForestClassifier(n_estimators=10, random_state=42)
        model.fit(X, y)
        return model

    def test_initialization(self, trained_model: RandomForestClassifier) -> None:
        """Test adapter initialization."""
        adapter = SklearnAdapter(trained_model)

        assert adapter.model is trained_model
        assert adapter.model_type == "RandomForestClassifier"

    def test_predict(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test prediction."""
        X, _ = sample_data
        adapter = SklearnAdapter(trained_model)

        predictions = adapter.predict(X)

        assert isinstance(predictions, np.ndarray)
        assert len(predictions) == len(X)
        assert set(predictions).issubset({0, 1})

    def test_predict_proba(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test probability prediction."""
        X, _ = sample_data
        adapter = SklearnAdapter(trained_model)

        probabilities = adapter.predict_proba(X)

        assert probabilities is not None
        assert isinstance(probabilities, np.ndarray)
        assert len(probabilities) == len(X)
        assert all(0 <= p <= 1 for p in probabilities)

    def test_supports_proba(self, trained_model: RandomForestClassifier) -> None:
        """Test checking probability support."""
        adapter = SklearnAdapter(trained_model)

        assert adapter.supports_proba is True

    def test_different_sklearn_models(self, sample_data: tuple) -> None:
        """Test adapter works with different sklearn models."""
        X, y = sample_data

        models = [
            RandomForestClassifier(n_estimators=10, random_state=42),
            DecisionTreeClassifier(random_state=42),
            LogisticRegression(random_state=42),
        ]

        for model in models:
            model.fit(X, y)
            adapter = SklearnAdapter(model)

            predictions = adapter.predict(X)
            assert len(predictions) == len(X)

            if adapter.supports_proba:
                probabilities = adapter.predict_proba(X)
                assert probabilities is not None
                assert len(probabilities) == len(X)

    def test_invalid_model(self) -> None:
        """Test that invalid model raises error."""

        class FakeModel:
            pass

        with pytest.raises(ValueError, match="must have a 'predict' method"):
            SklearnAdapter(FakeModel())

    def test_create_adapter_auto_detection(
        self, trained_model: RandomForestClassifier
    ) -> None:
        """Test automatic adapter creation."""
        adapter = create_adapter(trained_model)

        assert isinstance(adapter, SklearnAdapter)
        assert adapter.model is trained_model

    def test_predictions_match_original(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test that adapter predictions match original model."""
        X, _ = sample_data
        adapter = SklearnAdapter(trained_model)

        adapter_pred = adapter.predict(X)
        original_pred = trained_model.predict(X)

        np.testing.assert_array_equal(adapter_pred, original_pred)

    def test_probabilities_match_original(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test that adapter probabilities match original model."""
        X, _ = sample_data
        adapter = SklearnAdapter(trained_model)

        adapter_proba = adapter.predict_proba(X)
        original_proba = trained_model.predict_proba(X)[:, 1]

        np.testing.assert_array_almost_equal(adapter_proba, original_proba)
