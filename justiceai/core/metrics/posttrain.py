"""
Post-training fairness metrics (model-dependent).

These metrics require model predictions and evaluate fairness
in the model's decisions across different groups.
"""

from typing import Any

import numpy as np
import pandas as pd
from sklearn.metrics import confusion_matrix


def statistical_parity(
    y_pred: np.ndarray, sensitive_attr: pd.Series
) -> dict[str, Any]:
    """
    Calculate statistical parity (demographic parity).

    Statistical parity is satisfied when P(Y_pred=1|A=a) = P(Y_pred=1|A=b)
    for all groups a, b. Measures whether different groups receive positive
    predictions at equal rates.

    Args:
        y_pred: Model predictions (binary: 0 or 1)
        sensitive_attr: Sensitive attribute groups

    Returns:
        Dictionary with:
        - 'by_group': Selection rates per group
        - 'difference': Max - Min selection rate
        - 'ratio': Min / Max selection rate
        - 'is_fair': Whether difference < 0.1 (80% rule approx)

    Example:
        >>> y_pred = np.array([1, 1, 0, 0])
        >>> sensitive = pd.Series(['A', 'A', 'B', 'B'])
        >>> result = statistical_parity(y_pred, sensitive)
        >>> result['by_group']['A']
        1.0
    """
    results_by_group = {}

    for group in sensitive_attr.unique():
        mask = sensitive_attr == group
        group_preds = y_pred[mask]

        selection_rate = np.mean(group_preds) if len(group_preds) > 0 else 0.0
        results_by_group[str(group)] = {
            "selection_rate": float(selection_rate),
            "total_samples": int(len(group_preds)),
        }

    # Calculate overall metrics
    selection_rates = [v["selection_rate"] for v in results_by_group.values()]
    max_rate = max(selection_rates) if selection_rates else 0.0
    min_rate = min(selection_rates) if selection_rates else 0.0

    difference = max_rate - min_rate
    ratio = min_rate / max_rate if max_rate > 0 else 1.0

    return {
        "by_group": results_by_group,
        "difference": float(difference),
        "ratio": float(ratio),
        "is_fair": difference < 0.1,  # Common threshold
    }


def disparate_impact(
    y_pred: np.ndarray, sensitive_attr: pd.Series
) -> dict[str, Any]:
    """
    Calculate disparate impact ratio.

    Disparate impact = min(P(Y=1|A=a)) / max(P(Y=1|A=a))

    The "80% rule" states that a ratio < 0.8 indicates potential
    discrimination (used in US employment law).

    Args:
        y_pred: Model predictions (binary)
        sensitive_attr: Sensitive attribute

    Returns:
        Dictionary with:
        - 'ratio': Disparate impact ratio
        - 'passes_80_rule': Whether ratio >= 0.8
        - 'advantaged_group': Group with highest selection rate
        - 'disadvantaged_group': Group with lowest selection rate

    Example:
        >>> y_pred = np.array([1, 1, 1, 0])
        >>> sensitive = pd.Series(['A', 'A', 'B', 'B'])
        >>> result = disparate_impact(y_pred, sensitive)
        >>> result['ratio']
        0.5
    """
    # Calculate selection rates per group
    selection_rates = {}
    for group in sensitive_attr.unique():
        mask = sensitive_attr == group
        rate = np.mean(y_pred[mask]) if np.sum(mask) > 0 else 0.0
        selection_rates[str(group)] = float(rate)

    if not selection_rates:
        return {
            "ratio": 1.0,
            "passes_80_rule": True,
            "advantaged_group": None,
            "disadvantaged_group": None,
            "by_group": {},
        }

    max_rate = max(selection_rates.values())
    min_rate = min(selection_rates.values())

    ratio = min_rate / max_rate if max_rate > 0 else 1.0

    advantaged = max(selection_rates, key=selection_rates.get)
    disadvantaged = min(selection_rates, key=selection_rates.get)

    return {
        "ratio": float(ratio),
        "passes_80_rule": ratio >= 0.8,
        "advantaged_group": advantaged,
        "disadvantaged_group": disadvantaged,
        "by_group": selection_rates,
    }


def equal_opportunity(
    y_true: np.ndarray, y_pred: np.ndarray, sensitive_attr: pd.Series
) -> dict[str, Any]:
    """
    Calculate equal opportunity (true positive rate equality).

    Equal opportunity is satisfied when TPR(A=a) = TPR(A=b) for all groups.
    Focuses on ensuring qualified individuals from all groups have equal
    chances of positive outcomes.

    Args:
        y_true: True labels
        y_pred: Model predictions
        sensitive_attr: Sensitive attribute

    Returns:
        Dictionary with:
        - 'by_group': TPR per group
        - 'difference': Max TPR - Min TPR
        - 'is_fair': Whether difference < threshold

    Example:
        >>> y_true = np.array([1, 1, 0, 0])
        >>> y_pred = np.array([1, 0, 0, 0])
        >>> sensitive = pd.Series(['A', 'A', 'B', 'B'])
        >>> result = equal_opportunity(y_true, y_pred, sensitive)
    """
    results_by_group = {}

    for group in sensitive_attr.unique():
        mask = sensitive_attr == group
        y_true_group = y_true[mask]
        y_pred_group = y_pred[mask]

        # Calculate TPR (True Positive Rate)
        tp = np.sum((y_true_group == 1) & (y_pred_group == 1))
        fn = np.sum((y_true_group == 1) & (y_pred_group == 0))

        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0.0

        results_by_group[str(group)] = {
            "tpr": float(tpr),
            "true_positives": int(tp),
            "false_negatives": int(fn),
        }

    # Calculate difference
    tprs = [v["tpr"] for v in results_by_group.values()]
    difference = max(tprs) - min(tprs) if tprs else 0.0

    return {
        "by_group": results_by_group,
        "difference": float(difference),
        "is_fair": difference < 0.1,
    }


def equalized_odds(
    y_true: np.ndarray, y_pred: np.ndarray, sensitive_attr: pd.Series
) -> dict[str, Any]:
    """
    Calculate equalized odds (TPR and FPR equality).

    Equalized odds requires both TPR and FPR to be equal across groups.
    Stricter than equal opportunity.

    Args:
        y_true: True labels
        y_pred: Model predictions
        sensitive_attr: Sensitive attribute

    Returns:
        Dictionary with:
        - 'by_group': TPR and FPR per group
        - 'tpr_difference': Max TPR - Min TPR
        - 'fpr_difference': Max FPR - Min FPR
        - 'is_fair': Whether both differences < threshold

    Example:
        >>> y_true = np.array([1, 1, 0, 0])
        >>> y_pred = np.array([1, 1, 0, 1])
        >>> sensitive = pd.Series(['A', 'A', 'B', 'B'])
        >>> result = equalized_odds(y_true, y_pred, sensitive)
    """
    results_by_group = {}

    for group in sensitive_attr.unique():
        mask = sensitive_attr == group
        y_true_group = y_true[mask]
        y_pred_group = y_pred[mask]

        # Calculate confusion matrix components
        tp = np.sum((y_true_group == 1) & (y_pred_group == 1))
        tn = np.sum((y_true_group == 0) & (y_pred_group == 0))
        fp = np.sum((y_true_group == 0) & (y_pred_group == 1))
        fn = np.sum((y_true_group == 1) & (y_pred_group == 0))

        # Calculate TPR and FPR
        tpr = tp / (tp + fn) if (tp + fn) > 0 else 0.0
        fpr = fp / (fp + tn) if (fp + tn) > 0 else 0.0

        results_by_group[str(group)] = {
            "tpr": float(tpr),
            "fpr": float(fpr),
            "tp": int(tp),
            "tn": int(tn),
            "fp": int(fp),
            "fn": int(fn),
        }

    # Calculate differences
    tprs = [v["tpr"] for v in results_by_group.values()]
    fprs = [v["fpr"] for v in results_by_group.values()]

    tpr_diff = max(tprs) - min(tprs) if tprs else 0.0
    fpr_diff = max(fprs) - min(fprs) if fprs else 0.0

    return {
        "by_group": results_by_group,
        "tpr_difference": float(tpr_diff),
        "fpr_difference": float(fpr_diff),
        "is_fair": (tpr_diff < 0.1) and (fpr_diff < 0.1),
    }


def confusion_matrix_by_group(
    y_true: np.ndarray, y_pred: np.ndarray, sensitive_attr: pd.Series
) -> dict[str, dict[str, int]]:
    """
    Calculate confusion matrix stratified by sensitive attribute.

    Args:
        y_true: True labels
        y_pred: Model predictions
        sensitive_attr: Sensitive attribute

    Returns:
        Dictionary mapping group -> confusion matrix components:
        {
            'group_name': {
                'TP': int, 'TN': int, 'FP': int, 'FN': int,
                'total': int
            }
        }

    Example:
        >>> y_true = np.array([1, 1, 0, 0])
        >>> y_pred = np.array([1, 0, 0, 1])
        >>> sensitive = pd.Series(['A', 'A', 'B', 'B'])
        >>> result = confusion_matrix_by_group(y_true, y_pred, sensitive)
        >>> result['A']['TP']
        1
    """
    results = {}

    for group in sensitive_attr.unique():
        mask = sensitive_attr == group
        y_true_group = y_true[mask]
        y_pred_group = y_pred[mask]

        # Calculate confusion matrix
        tn, fp, fn, tp = confusion_matrix(
            y_true_group, y_pred_group, labels=[0, 1]
        ).ravel()

        results[str(group)] = {
            "TP": int(tp),
            "TN": int(tn),
            "FP": int(fp),
            "FN": int(fn),
            "total": int(len(y_true_group)),
        }

    return results
