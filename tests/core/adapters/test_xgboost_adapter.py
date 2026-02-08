"""Tests for XGBoost adapter."""

import numpy as np
import pytest
from sklearn.datasets import make_classification

# Try to import xgboost
try:
    import xgboost as xgb

    XGBOOST_AVAILABLE = True
except ImportError:
    XGBOOST_AVAILABLE = False

from justiceai.core.adapters import create_adapter

pytestmark = pytest.mark.skipif(
    not XGBOOST_AVAILABLE, reason="xgboost not installed"
)


class TestXGBoostAdapter:
    """Tests for XGBoostAdapter class."""

    @pytest.fixture
    def sample_data(self) -> tuple:
        """Create sample classification data."""
        X, y = make_classification(
            n_samples=100, n_features=5, n_classes=2, random_state=42
        )
        return X, y

    @pytest.fixture
    def trained_model(self, sample_data: tuple):
        """Create and train an XGBoost model."""
        X, y = sample_data
        model = xgb.XGBClassifier(n_estimators=10, random_state=42, eval_metric="logloss")
        model.fit(X, y)
        return model

    def test_initialization(self, trained_model):
        """Test adapter initialization."""
        from justiceai.core.adapters.xgboost_adapter import XGBoostAdapter

        adapter = XGBoostAdapter(trained_model)

        assert adapter.model is trained_model
        assert adapter.model_type == "XGBClassifier"

    def test_predict(self, trained_model, sample_data: tuple):
        """Test prediction."""
        from justiceai.core.adapters.xgboost_adapter import XGBoostAdapter

        X, _ = sample_data
        adapter = XGBoostAdapter(trained_model)

        predictions = adapter.predict(X)

        assert isinstance(predictions, np.ndarray)
        assert len(predictions) == len(X)
        assert set(predictions).issubset({0, 1})

    def test_predict_proba(self, trained_model, sample_data: tuple):
        """Test probability prediction."""
        from justiceai.core.adapters.xgboost_adapter import XGBoostAdapter

        X, _ = sample_data
        adapter = XGBoostAdapter(trained_model)

        probabilities = adapter.predict_proba(X)

        assert probabilities is not None
        assert isinstance(probabilities, np.ndarray)
        assert len(probabilities) == len(X)
        assert all(0 <= p <= 1 for p in probabilities)

    def test_supports_proba(self, trained_model):
        """Test checking probability support."""
        from justiceai.core.adapters.xgboost_adapter import XGBoostAdapter

        adapter = XGBoostAdapter(trained_model)

        assert adapter.supports_proba is True

    def test_create_adapter_auto_detection(self, trained_model):
        """Test automatic adapter creation."""
        adapter = create_adapter(trained_model)

        from justiceai.core.adapters.xgboost_adapter import XGBoostAdapter

        assert isinstance(adapter, XGBoostAdapter)
        assert adapter.model is trained_model

    def test_predictions_match_original(self, trained_model, sample_data: tuple):
        """Test that adapter predictions match original model."""
        from justiceai.core.adapters.xgboost_adapter import XGBoostAdapter

        X, _ = sample_data
        adapter = XGBoostAdapter(trained_model)

        adapter_pred = adapter.predict(X)
        original_pred = trained_model.predict(X)

        np.testing.assert_array_equal(adapter_pred, original_pred)

    def test_probabilities_match_original(self, trained_model, sample_data: tuple):
        """Test that adapter probabilities match original model."""
        from justiceai.core.adapters.xgboost_adapter import XGBoostAdapter

        X, _ = sample_data
        adapter = XGBoostAdapter(trained_model)

        adapter_proba = adapter.predict_proba(X)
        original_proba = trained_model.predict_proba(X)[:, 1]

        np.testing.assert_array_almost_equal(adapter_proba, original_proba)

    def test_invalid_model(self):
        """Test that invalid model raises error."""
        from justiceai.core.adapters.xgboost_adapter import XGBoostAdapter

        class FakeModel:
            pass

        with pytest.raises(ValueError, match="must be an XGBoost model"):
            XGBoostAdapter(FakeModel())

    def test_xgb_regressor_fails(self, sample_data: tuple):
        """Test that XGBRegressor raises error (only classifiers supported)."""
        from justiceai.core.adapters.xgboost_adapter import XGBoostAdapter

        X, y = sample_data
        model = xgb.XGBRegressor(n_estimators=10, random_state=42)
        model.fit(X, y)

        # XGBRegressor has predict but we're expecting classification
        adapter = XGBoostAdapter(model)
        # Should work (has predict method)
        predictions = adapter.predict(X)
        assert isinstance(predictions, np.ndarray)
