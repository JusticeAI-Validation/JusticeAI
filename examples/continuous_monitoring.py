"""
Continuous Fairness Monitoring Example.

This script demonstrates a complete continuous monitoring setup for
fairness metrics in production, including:
- Baseline establishment
- Periodic metric collection
- Drift detection
- Automatic alerting
- Trend analysis

Run this example:
    python examples/continuous_monitoring.py
"""

import time
from datetime import datetime

import numpy as np
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from justiceai import audit
from justiceai.monitoring import (
    ConsoleAlertChannel,
    FairnessAlerting,
    MetricsDriftMonitor,
)


def simulate_data_drift(X: np.ndarray, y: np.ndarray, drift_factor: float = 0.0):
    """
    Simulate data drift by modifying distributions.

    Args:
        X: Feature matrix
        y: Labels
        drift_factor: Amount of drift to introduce (0.0 = no drift, 1.0 = high drift)

    Returns:
        Drifted X and y
    """
    if drift_factor == 0.0:
        return X, y

    # Add noise proportional to drift factor
    noise = np.random.normal(0, drift_factor, X.shape)
    X_drifted = X + noise

    # Optionally flip some labels to simulate concept drift
    if drift_factor > 0.5:
        flip_ratio = (drift_factor - 0.5) * 0.2  # Up to 10% label flip
        num_flips = int(len(y) * flip_ratio)
        flip_indices = np.random.choice(len(y), num_flips, replace=False)
        y_drifted = y.copy()
        y_drifted[flip_indices] = 1 - y_drifted[flip_indices]
        return X_drifted, y_drifted

    return X_drifted, y


def extract_fairness_metrics(audit_result) -> dict[str, float]:
    """
    Extract key fairness metrics from audit result.

    Args:
        audit_result: FairnessReport from justiceai.audit()

    Returns:
        Dictionary of fairness metrics
    """
    metrics = {}
    result = audit_result.fairness_result

    # Extract metrics for first protected attribute and first group
    if result.protected_attrs:
        first_attr = result.protected_attrs[0]
        if first_attr in result.metrics:
            # Get first group
            first_group = list(result.metrics[first_attr].keys())[0]
            group_metrics = result.metrics[first_attr][first_group]

            # Extract key metrics
            for metric_name in [
                "statistical_parity",
                "equal_opportunity",
                "predictive_parity",
            ]:
                if metric_name in group_metrics:
                    metrics[metric_name] = group_metrics[metric_name]

    return metrics


def main():
    """Run continuous monitoring simulation."""
    print("=" * 70)
    print("JusticeAI - Continuous Fairness Monitoring Example")
    print("=" * 70)
    print()

    # 1. Setup: Train initial model and establish baseline
    print("Step 1: Training initial model and establishing baseline...")
    print("-" * 70)

    # Generate initial training data
    X, y = make_classification(
        n_samples=1000,
        n_features=10,
        n_informative=5,
        n_redundant=2,
        random_state=42,
    )

    # Add protected attribute (e.g., gender: 0 or 1)
    protected_attr = np.random.binomial(1, 0.5, size=len(y))

    # Split data
    X_train, X_test, y_train, y_test, protected_train, protected_test = (
        train_test_split(X, y, protected_attr, test_size=0.3, random_state=42)
    )

    # Train model
    model = RandomForestClassifier(n_estimators=50, random_state=42)
    model.fit(X_train, y_train)

    # Run initial fairness audit
    import pandas as pd

    test_data = pd.DataFrame(X_test)
    test_data["gender"] = protected_test
    test_data["target"] = y_test

    baseline_report = audit(model, test_data, protected_attrs=["gender"], target="target")

    # Extract baseline metrics
    baseline_metrics = extract_fairness_metrics(baseline_report)

    print(f"Baseline metrics established: {baseline_metrics}")
    print()

    # 2. Setup monitoring and alerting
    print("Step 2: Setting up monitoring and alerting...")
    print("-" * 70)

    # Create drift monitor
    monitor = MetricsDriftMonitor(
        baseline_metrics=baseline_metrics,
        window_size=5,  # Keep last 5 observations
        method="threshold",
        threshold=0.10,  # Alert if metric changes by more than 10%
    )

    # Setup alerting with console channel
    alerting = FairnessAlerting()
    alerting.add_channel("console", ConsoleAlertChannel())

    print("Monitoring configured:")
    print(f"  - Window size: 5 observations")
    print(f"  - Detection method: threshold")
    print(f"  - Threshold: 0.10 (10% change)")
    print(f"  - Alert channels: console")
    print()

    # 3. Simulate continuous monitoring over time
    print("Step 3: Simulating continuous monitoring (10 time periods)...")
    print("-" * 70)
    print()

    # Simulate 10 time periods with increasing drift
    for period in range(1, 11):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f"[{timestamp}] Period {period}/10")

        # Introduce gradual drift (increases over time)
        drift_factor = period * 0.08  # Gradually increase drift

        # Generate new production data with drift
        X_prod, y_prod = make_classification(
            n_samples=300,
            n_features=10,
            n_informative=5,
            n_redundant=2,
            random_state=42 + period,
        )
        X_prod, y_prod = simulate_data_drift(X_prod, y_prod, drift_factor)

        # Add protected attribute
        protected_prod = np.random.binomial(1, 0.5, size=len(y_prod))

        # Create production DataFrame
        prod_data = pd.DataFrame(X_prod)
        prod_data["gender"] = protected_prod
        prod_data["target"] = y_prod

        # Run fairness audit on production data
        prod_report = audit(model, prod_data, protected_attrs=["gender"], target="target")

        # Extract current metrics
        current_metrics = extract_fairness_metrics(prod_report)

        print(f"  Current metrics: {current_metrics}")

        # Add observation to monitor and detect drift
        drift_result = monitor.add_observation(current_metrics, timestamp=timestamp)

        if drift_result.has_drift:
            print(f"  ⚠️  DRIFT DETECTED!")
            print(f"  Drifted metrics: {list(drift_result.drifted_metrics.keys())}")

            # Send alert
            from justiceai.monitoring import FairnessDriftDetector

            detector = FairnessDriftDetector(baseline_metrics)
            alerting.send_drift_alert(drift_result, detector, timestamp=timestamp)
        else:
            print(f"  ✓ No drift detected")

        print()

        # Small delay to simulate time passing
        time.sleep(0.5)

    # 4. Summary and trend analysis
    print("=" * 70)
    print("Monitoring Summary")
    print("=" * 70)

    # Get overall drift report
    drift_report = monitor.check_drift()
    print(f"Drift detected in {drift_report['num_with_drift']}/{drift_report['num_observations']} observations")
    print(f"Drift ratio: {drift_report['drift_ratio']:.2%}")
    print(f"Overall drift status: {'⚠️ DRIFTING' if drift_report['has_drift'] else '✓ STABLE'}")
    print()

    # Get drift trends
    print("Drift Trends (drift scores over time):")
    print("-" * 70)
    trends = monitor.get_drift_trend()

    for metric_name, scores in trends.items():
        print(f"\n{metric_name}:")
        print(f"  Scores: {[f'{s:.4f}' for s in scores]}")
        print(f"  Mean: {np.mean(scores):.4f}")
        print(f"  Max: {np.max(scores):.4f}")
        print(f"  Trend: {'↑ Increasing' if scores[-1] > scores[0] else '↓ Decreasing'}")

    print()
    print("=" * 70)
    print("Monitoring simulation complete!")
    print("=" * 70)
    print()

    # 5. Recommendations
    print("Recommendations:")
    print("-" * 70)
    if drift_report["has_drift"]:
        print("⚠️  Significant drift detected. Recommended actions:")
        print("  1. Investigate root cause of drift (data distribution changes?)")
        print("  2. Consider retraining the model with recent data")
        print("  3. Review data collection and preprocessing pipelines")
        print("  4. Implement mitigation strategies for identified biases")
        print("  5. Update baseline metrics after model retraining")
    else:
        print("✓ Model fairness is stable. Continue monitoring:")
        print("  1. Maintain current monitoring frequency")
        print("  2. Review metrics periodically (weekly/monthly)")
        print("  3. Keep audit trail for compliance purposes")
        print("  4. Be prepared to act if drift is detected in future")

    print()


if __name__ == "__main__":
    main()
