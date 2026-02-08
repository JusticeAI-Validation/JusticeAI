"""Integration tests for FairnessEvaluator."""

import numpy as np
import pandas as pd
import pytest
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression

from justiceai import FairnessEvaluator
from justiceai.reports import FairnessReport


class TestFairnessEvaluator:
    """Integration tests for FairnessEvaluator class."""

    @pytest.fixture
    def sample_data(self) -> tuple:
        """Create sample classification data with sensitive attribute."""
        X, y = make_classification(
            n_samples=200,
            n_features=5,
            n_classes=2,
            random_state=42,
            flip_y=0.1,
        )

        # Create sensitive attribute (gender)
        gender = pd.Series(
            np.random.choice(["M", "F"], size=200, p=[0.6, 0.4]),
            name="gender",
        )

        return X, y, gender

    @pytest.fixture
    def trained_model(self, sample_data: tuple) -> RandomForestClassifier:
        """Create and train a model."""
        X, y, _ = sample_data
        model = RandomForestClassifier(n_estimators=50, random_state=42)
        model.fit(X, y)
        return model

    def test_evaluate_with_sklearn_model(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test evaluate() with sklearn model."""
        X, y, gender = sample_data
        evaluator = FairnessEvaluator(fairness_threshold=0.05)

        report = evaluator.evaluate(
            model=trained_model,
            X=X,
            y_true=y,
            sensitive_attrs=gender,
        )

        assert isinstance(report, FairnessReport)
        assert report.get_overall_score() is not None
        assert isinstance(report.get_overall_score(), (int, float))
        assert 0 <= report.get_overall_score() <= 100

    def test_evaluate_with_dataframe(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test evaluate() with pandas DataFrame."""
        X, y, gender = sample_data
        X_df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(X.shape[1])])
        y_series = pd.Series(y, name="target")

        evaluator = FairnessEvaluator()

        report = evaluator.evaluate(
            model=trained_model,
            X=X_df,
            y_true=y_series,
            sensitive_attrs=gender,
        )

        assert isinstance(report, FairnessReport)
        assert report.get_overall_score() >= 0

    def test_evaluate_with_dict_sensitive_attrs(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test evaluate() with dictionary of sensitive attributes."""
        X, y, gender = sample_data

        evaluator = FairnessEvaluator()

        report = evaluator.evaluate(
            model=trained_model,
            X=X,
            y_true=y,
            sensitive_attrs={"gender": gender},
        )

        assert isinstance(report, FairnessReport)

    def test_evaluate_without_probabilities(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test evaluate() without probability-based metrics."""
        X, y, gender = sample_data

        evaluator = FairnessEvaluator()

        report = evaluator.evaluate(
            model=trained_model,
            X=X,
            y_true=y,
            sensitive_attrs=gender,
            return_probabilities=False,
        )

        assert isinstance(report, FairnessReport)

    def test_evaluate_predictions(self, sample_data: tuple) -> None:
        """Test evaluate_predictions() with pre-computed predictions."""
        X, y, gender = sample_data

        # Create predictions
        y_pred = np.random.choice([0, 1], size=len(y))

        evaluator = FairnessEvaluator()

        report = evaluator.evaluate_predictions(
            y_true=y,
            y_pred=y_pred,
            sensitive_attrs=gender,
        )

        assert isinstance(report, FairnessReport)
        assert report.get_overall_score() >= 0

    def test_evaluate_predictions_with_probabilities(
        self, sample_data: tuple
    ) -> None:
        """Test evaluate_predictions() with probabilities."""
        X, y, gender = sample_data

        # Create predictions and probabilities
        y_pred = np.random.choice([0, 1], size=len(y))
        y_pred_proba = np.random.random(size=len(y))

        evaluator = FairnessEvaluator()

        report = evaluator.evaluate_predictions(
            y_true=y,
            y_pred=y_pred,
            sensitive_attrs=gender,
            y_pred_proba=y_pred_proba,
        )

        assert isinstance(report, FairnessReport)

    def test_evaluate_predictions_with_features(
        self, sample_data: tuple
    ) -> None:
        """Test evaluate_predictions() with features."""
        X, y, gender = sample_data

        y_pred = np.random.choice([0, 1], size=len(y))

        evaluator = FairnessEvaluator()

        report = evaluator.evaluate_predictions(
            y_true=y,
            y_pred=y_pred,
            sensitive_attrs=gender,
            X=X,
        )

        assert isinstance(report, FairnessReport)

    def test_evaluate_predictions_with_dict_sensitive_attrs(
        self, sample_data: tuple
    ) -> None:
        """Test evaluate_predictions() with dictionary."""
        X, y, gender = sample_data

        y_pred = np.random.choice([0, 1], size=len(y))

        evaluator = FairnessEvaluator()

        report = evaluator.evaluate_predictions(
            y_true=y,
            y_pred=y_pred,
            sensitive_attrs={"gender": gender},
        )

        assert isinstance(report, FairnessReport)

    def test_evaluate_predictions_with_series(
        self, sample_data: tuple
    ) -> None:
        """Test evaluate_predictions() with pandas Series."""
        X, y, gender = sample_data

        y_true_series = pd.Series(y, name="target")
        y_pred_series = pd.Series(np.random.choice([0, 1], size=len(y)), name="pred")

        evaluator = FairnessEvaluator()

        report = evaluator.evaluate_predictions(
            y_true=y_true_series,
            y_pred=y_pred_series,
            sensitive_attrs=gender,
        )

        assert isinstance(report, FairnessReport)

    def test_quick_check(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test quick_check() method."""
        X, y, gender = sample_data

        evaluator = FairnessEvaluator()

        metrics = evaluator.quick_check(
            model=trained_model,
            X=X,
            y_true=y,
            sensitive_attrs=gender,
        )

        assert isinstance(metrics, dict)
        assert "overall_score" in metrics
        assert "passes_fairness" in metrics
        assert "n_violations" in metrics
        assert "summary" in metrics

        assert isinstance(metrics["overall_score"], (int, float))
        assert isinstance(metrics["passes_fairness"], bool)
        assert isinstance(metrics["n_violations"], int)
        assert isinstance(metrics["summary"], dict)

    def test_custom_fairness_threshold(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test evaluator with custom fairness threshold."""
        X, y, gender = sample_data

        evaluator = FairnessEvaluator(fairness_threshold=0.10)

        report = evaluator.evaluate(
            model=trained_model,
            X=X,
            y_true=y,
            sensitive_attrs=gender,
        )

        assert isinstance(report, FairnessReport)

    def test_multiple_models(self, sample_data: tuple) -> None:
        """Test evaluator with different model types."""
        X, y, gender = sample_data

        models = [
            RandomForestClassifier(n_estimators=10, random_state=42),
            LogisticRegression(random_state=42, max_iter=1000),
        ]

        evaluator = FairnessEvaluator()

        for model in models:
            model.fit(X, y)

            report = evaluator.evaluate(
                model=model,
                X=X,
                y_true=y,
                sensitive_attrs=gender,
            )

            assert isinstance(report, FairnessReport)
            assert report.get_overall_score() >= 0

    def test_report_methods_integration(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test that report methods work correctly."""
        X, y, gender = sample_data

        evaluator = FairnessEvaluator()

        report = evaluator.evaluate(
            model=trained_model,
            X=X,
            y_true=y,
            sensitive_attrs=gender,
        )

        # Test report methods
        assert isinstance(report.get_overall_score(), (int, float))
        assert isinstance(report.passes_fairness(), bool)
        assert isinstance(report.get_issues(), list)
        assert isinstance(report.get_summary(), dict)

    def test_evaluate_with_numpy_arrays(
        self, trained_model: RandomForestClassifier, sample_data: tuple
    ) -> None:
        """Test evaluate() with numpy arrays."""
        X, y, gender = sample_data

        evaluator = FairnessEvaluator()

        report = evaluator.evaluate(
            model=trained_model,
            X=np.array(X),
            y_true=np.array(y),
            sensitive_attrs=gender,
        )

        assert isinstance(report, FairnessReport)

    def test_evaluate_predictions_with_dataframe(
        self, sample_data: tuple
    ) -> None:
        """Test evaluate_predictions() with DataFrame features."""
        X, y, gender = sample_data

        X_df = pd.DataFrame(X, columns=[f"feature_{i}" for i in range(X.shape[1])])
        y_pred = np.random.choice([0, 1], size=len(y))

        evaluator = FairnessEvaluator()

        report = evaluator.evaluate_predictions(
            y_true=y,
            y_pred=y_pred,
            sensitive_attrs=gender,
            X=X_df,
        )

        assert isinstance(report, FairnessReport)
