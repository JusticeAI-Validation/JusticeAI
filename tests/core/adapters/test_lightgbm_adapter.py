"""Tests for LightGBM adapter."""

import numpy as np
import pytest
from sklearn.datasets import make_classification

# Try to import lightgbm
try:
    import lightgbm as lgb

    LIGHTGBM_AVAILABLE = True
except ImportError:
    LIGHTGBM_AVAILABLE = False

from justiceai.core.adapters import create_adapter

pytestmark = pytest.mark.skipif(
    not LIGHTGBM_AVAILABLE, reason="lightgbm not installed"
)


class TestLightGBMAdapter:
    """Tests for LightGBMAdapter class."""

    @pytest.fixture
    def sample_data(self) -> tuple:
        """Create sample classification data."""
        X, y = make_classification(
            n_samples=100, n_features=5, n_classes=2, random_state=42
        )
        return X, y

    @pytest.fixture
    def trained_model(self, sample_data: tuple):
        """Create and train a LightGBM model."""
        X, y = sample_data
        model = lgb.LGBMClassifier(n_estimators=10, random_state=42, verbose=-1)
        model.fit(X, y)
        return model

    def test_initialization(self, trained_model):
        """Test adapter initialization."""
        from justiceai.core.adapters.lightgbm_adapter import LightGBMAdapter

        adapter = LightGBMAdapter(trained_model)

        assert adapter.model is trained_model
        assert adapter.model_type == "LGBMClassifier"

    def test_predict(self, trained_model, sample_data: tuple):
        """Test prediction."""
        from justiceai.core.adapters.lightgbm_adapter import LightGBMAdapter

        X, _ = sample_data
        adapter = LightGBMAdapter(trained_model)

        predictions = adapter.predict(X)

        assert isinstance(predictions, np.ndarray)
        assert len(predictions) == len(X)
        assert set(predictions).issubset({0, 1})

    def test_predict_proba(self, trained_model, sample_data: tuple):
        """Test probability prediction."""
        from justiceai.core.adapters.lightgbm_adapter import LightGBMAdapter

        X, _ = sample_data
        adapter = LightGBMAdapter(trained_model)

        probabilities = adapter.predict_proba(X)

        assert probabilities is not None
        assert isinstance(probabilities, np.ndarray)
        assert len(probabilities) == len(X)
        assert all(0 <= p <= 1 for p in probabilities)

    def test_supports_proba(self, trained_model):
        """Test checking probability support."""
        from justiceai.core.adapters.lightgbm_adapter import LightGBMAdapter

        adapter = LightGBMAdapter(trained_model)

        assert adapter.supports_proba is True

    def test_create_adapter_auto_detection(self, trained_model):
        """Test automatic adapter creation."""
        adapter = create_adapter(trained_model)

        from justiceai.core.adapters.lightgbm_adapter import LightGBMAdapter

        assert isinstance(adapter, LightGBMAdapter)
        assert adapter.model is trained_model

    def test_predictions_match_original(self, trained_model, sample_data: tuple):
        """Test that adapter predictions match original model."""
        from justiceai.core.adapters.lightgbm_adapter import LightGBMAdapter

        X, _ = sample_data
        adapter = LightGBMAdapter(trained_model)

        adapter_pred = adapter.predict(X)
        original_pred = trained_model.predict(X)

        np.testing.assert_array_equal(adapter_pred, original_pred)

    def test_probabilities_match_original(self, trained_model, sample_data: tuple):
        """Test that adapter probabilities match original model."""
        from justiceai.core.adapters.lightgbm_adapter import LightGBMAdapter

        X, _ = sample_data
        adapter = LightGBMAdapter(trained_model)

        adapter_proba = adapter.predict_proba(X)
        original_proba = trained_model.predict_proba(X)[:, 1]

        np.testing.assert_array_almost_equal(adapter_proba, original_proba)

    def test_invalid_model(self):
        """Test that invalid model raises error."""
        from justiceai.core.adapters.lightgbm_adapter import LightGBMAdapter

        class FakeModel:
            pass

        with pytest.raises(ValueError, match="must be a LightGBM model"):
            LightGBMAdapter(FakeModel())

    def test_lgbm_regressor(self, sample_data: tuple):
        """Test that LGBMRegressor works (has predict method)."""
        from justiceai.core.adapters.lightgbm_adapter import LightGBMAdapter

        X, y = sample_data
        model = lgb.LGBMRegressor(n_estimators=10, random_state=42, verbose=-1)
        model.fit(X, y)

        # LGBMRegressor has predict but we're expecting classification
        adapter = LightGBMAdapter(model)
        # Should work (has predict method)
        predictions = adapter.predict(X)
        assert isinstance(predictions, np.ndarray)
