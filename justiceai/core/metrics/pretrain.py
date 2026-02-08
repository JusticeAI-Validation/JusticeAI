"""
Pre-training fairness metrics (model-independent).

These metrics can be calculated on the dataset before training any model,
helping identify potential biases in the data distribution.
"""

from typing import Any

import numpy as np
import pandas as pd
from scipy.stats import entropy


def class_balance(
    y: pd.Series, sensitive_attr: pd.Series
) -> dict[str, dict[str, Any]]:
    """
    Calculate class balance across sensitive attribute groups.

    Measures the distribution of target classes within each group defined
    by the sensitive attribute. Imbalanced class distributions can indicate
    potential fairness issues.

    Args:
        y: Target variable (labels)
        sensitive_attr: Sensitive attribute (e.g., gender, race)

    Returns:
        Dictionary with balance metrics per group:
        {
            'group_name': {
                'class_distribution': {class: count},
                'majority_class_ratio': float,
                'balance_score': float  # 1.0 = perfectly balanced
            }
        }

    Example:
        >>> y = pd.Series([0, 1, 0, 1, 0, 1])
        >>> sensitive = pd.Series(['A', 'A', 'B', 'B', 'B', 'B'])
        >>> result = class_balance(y, sensitive)
        >>> result['A']['balance_score']
        1.0  # Perfectly balanced for group A
    """
    results = {}

    for group in sensitive_attr.unique():
        mask = sensitive_attr == group
        y_group = y[mask]

        # Count classes
        class_counts = y_group.value_counts().to_dict()
        total = len(y_group)

        # Calculate majority class ratio
        majority_ratio = max(class_counts.values()) / total if total > 0 else 0.0

        # Balance score (1.0 = perfect balance, 0.0 = all one class)
        n_classes = len(class_counts)
        if n_classes <= 1:
            balance_score = 0.0
        else:
            # Use normalized entropy as balance score
            proportions = np.array(list(class_counts.values())) / total
            balance_score = entropy(proportions) / np.log(n_classes)

        results[str(group)] = {
            "class_distribution": class_counts,
            "majority_class_ratio": float(majority_ratio),
            "balance_score": float(balance_score),
            "total_samples": int(total),
        }

    return results


def concept_balance(
    X: pd.DataFrame, y: pd.Series, sensitive_attr: pd.Series
) -> dict[str, float]:
    """
    Calculate concept balance using mutual information.

    Measures how much information the sensitive attribute provides about
    the target variable. High mutual information indicates the sensitive
    attribute is strongly associated with the outcome.

    Args:
        X: Feature matrix (not used in current implementation)
        y: Target variable
        sensitive_attr: Sensitive attribute

    Returns:
        Dictionary with mutual information metrics:
        {
            'mutual_information': float,  # Raw MI value
            'normalized_mi': float,  # Normalized to [0, 1]
        }

    Example:
        >>> X = pd.DataFrame({'feat1': [1, 2, 3, 4]})
        >>> y = pd.Series([0, 0, 1, 1])
        >>> sensitive = pd.Series(['A', 'A', 'B', 'B'])
        >>> result = concept_balance(X, y, sensitive)
    """
    # Create contingency table
    contingency = pd.crosstab(sensitive_attr, y)

    # Calculate marginal distributions
    p_sensitive = contingency.sum(axis=1) / contingency.sum().sum()
    p_y = contingency.sum(axis=0) / contingency.sum().sum()

    # Calculate joint distribution
    p_joint = contingency / contingency.sum().sum()

    # Calculate mutual information
    mi = 0.0
    for i, sens_val in enumerate(contingency.index):
        for j, y_val in enumerate(contingency.columns):
            if p_joint.iloc[i, j] > 0:
                mi += p_joint.iloc[i, j] * np.log2(
                    p_joint.iloc[i, j] / (p_sensitive.iloc[i] * p_y.iloc[j])
                )

    # Normalize MI by entropy of target
    h_y = entropy(p_y.values, base=2)
    normalized_mi = mi / h_y if h_y > 0 else 0.0

    return {
        "mutual_information": float(mi),
        "normalized_mi": float(normalized_mi),
    }


def kl_divergence(dist1: np.ndarray, dist2: np.ndarray) -> float:
    """
    Calculate Kullback-Leibler divergence between two distributions.

    KL divergence measures how one probability distribution differs from
    a reference distribution. Useful for comparing class distributions
    across different groups.

    Args:
        dist1: First probability distribution (must sum to 1)
        dist2: Second probability distribution (must sum to 1)

    Returns:
        KL divergence value (≥ 0, where 0 means identical distributions)

    Example:
        >>> dist1 = np.array([0.5, 0.5])
        >>> dist2 = np.array([0.6, 0.4])
        >>> kl = kl_divergence(dist1, dist2)
        >>> kl > 0
        True
    """
    # Normalize to ensure they sum to 1
    dist1 = np.asarray(dist1) / np.sum(dist1)
    dist2 = np.asarray(dist2) / np.sum(dist2)

    # Add small epsilon to avoid log(0)
    epsilon = 1e-10
    dist1 = dist1 + epsilon
    dist2 = dist2 + epsilon

    # Re-normalize after adding epsilon
    dist1 = dist1 / np.sum(dist1)
    dist2 = dist2 / np.sum(dist2)

    return float(np.sum(dist1 * np.log(dist1 / dist2)))


def js_divergence(dist1: np.ndarray, dist2: np.ndarray) -> float:
    """
    Calculate Jensen-Shannon divergence between two distributions.

    JS divergence is a symmetrized and smoothed version of KL divergence.
    It's always finite and bounded between 0 and 1 (when using log2).

    Args:
        dist1: First probability distribution
        dist2: Second probability distribution

    Returns:
        JS divergence value (0 to 1, where 0 means identical distributions)

    Example:
        >>> dist1 = np.array([0.5, 0.5])
        >>> dist2 = np.array([0.6, 0.4])
        >>> js = js_divergence(dist1, dist2)
        >>> 0 <= js <= 1
        True
    """
    # Normalize distributions
    dist1 = np.asarray(dist1) / np.sum(dist1)
    dist2 = np.asarray(dist2) / np.sum(dist2)

    # Calculate average distribution
    m = 0.5 * (dist1 + dist2)

    # Calculate JS divergence
    js = 0.5 * kl_divergence(dist1, m) + 0.5 * kl_divergence(dist2, m)

    # Ensure result is in [0, 1] when using log2
    # Convert from nats to bits by dividing by log(2)
    js_bits = js / np.log(2)

    return float(min(js_bits, 1.0))


def group_distribution_difference(
    y: pd.Series, sensitive_attr: pd.Series
) -> dict[str, Any]:
    """
    Calculate distribution differences across sensitive attribute groups.

    Compares the target distribution across different groups using
    multiple divergence metrics.

    Args:
        y: Target variable
        sensitive_attr: Sensitive attribute

    Returns:
        Dictionary with pairwise divergence metrics between groups

    Example:
        >>> y = pd.Series([0, 1, 0, 1, 0, 1])
        >>> sensitive = pd.Series(['A', 'A', 'B', 'B', 'C', 'C'])
        >>> result = group_distribution_difference(y, sensitive)
    """
    groups = sensitive_attr.unique()
    results = {}

    # Calculate distribution for each group
    group_distributions = {}
    for group in groups:
        mask = sensitive_attr == group
        y_group = y[mask]
        dist = y_group.value_counts(normalize=True).sort_index()
        group_distributions[str(group)] = dist

    # Calculate pairwise divergences
    for i, group1 in enumerate(groups):
        for group2 in groups[i + 1 :]:
            dist1 = group_distributions[str(group1)]
            dist2 = group_distributions[str(group2)]

            # Align distributions (ensure same classes)
            all_classes = sorted(set(dist1.index) | set(dist2.index))
            dist1_aligned = np.array([dist1.get(c, 0.0) for c in all_classes])
            dist2_aligned = np.array([dist2.get(c, 0.0) for c in all_classes])

            pair_key = f"{group1}_vs_{group2}"
            results[pair_key] = {
                "kl_divergence": kl_divergence(dist1_aligned, dist2_aligned),
                "js_divergence": js_divergence(dist1_aligned, dist2_aligned),
            }

    return results
