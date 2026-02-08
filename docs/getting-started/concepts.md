# Basic Concepts

Understanding fairness metrics and how JusticeAI evaluates ML models.

## What is Fairness in ML?

Fairness in machine learning means ensuring that models make decisions without discriminating based on protected attributes like gender, race, age, or other sensitive characteristics.

## Key Terminology

### Protected/Sensitive Attributes
Attributes that should not influence model decisions (gender, race, age, etc.)

### Privileged vs Unprivileged Groups
- **Privileged Group**: The group that historically receives more favorable outcomes
- **Unprivileged Group**: The group that may face discrimination

Example: In a hiring model, if men receive more job offers, they are the privileged group.

### Pre-training vs Post-training Metrics

**Pre-training metrics** analyze data *before* model training:
- Identify bias in the dataset itself
- Check if sensitive attributes correlate with outcomes

**Post-training metrics** analyze model *predictions*:
- Measure fairness of model decisions
- Compare outcomes across groups

## Fairness Metrics Explained

### Statistical Parity (Demographic Parity)

**What it measures**: Whether positive outcomes are equally distributed across groups.

**Formula**: Difference in positive prediction rates between groups

```python
P(ŷ = 1 | Gender = Male) - P(ŷ = 1 | Gender = Female)
```

**Example**:
- 60% of male applicants approved for loans
- 50% of female applicants approved
- Statistical Parity Difference = 0.10

**Fair if**: Close to 0 (typically < 0.05)

**Use case**: When you want equal representation in outcomes

### Disparate Impact Ratio (80% Rule)

**What it measures**: Ratio of positive outcomes between groups (from US Equal Employment Opportunity Commission).

**Formula**: Ratio of positive rates

```python
P(ŷ = 1 | Unprivileged) / P(ŷ = 1 | Privileged)
```

**Example**:
- 50% of female applicants approved
- 60% of male applicants approved
- Disparate Impact = 50/60 = 0.83

**Fair if**: ≥ 0.80 (80% rule)

**Use case**: Legal compliance, hiring decisions

### Equal Opportunity

**What it measures**: Whether model gives equal true positive rates across groups.

**Formula**: Difference in TPR (sensitivity)

```python
TPR(Unprivileged) - TPR(Privileged)
```

**Example**: Among qualified applicants:
- 80% of qualified males get loans
- 70% of qualified females get loans
- Equal Opportunity Diff = -0.10

**Fair if**: Close to 0

**Use case**: When false negatives are costly (medical diagnosis, loan approvals)

### Equalized Odds

**What it measures**: Whether model has equal TPR *and* FPR across groups.

**Formula**: Maximum of TPR difference and FPR difference

```python
max(|TPR_diff|, |FPR_diff|)
```

**Fair if**: Both TPR and FPR are similar across groups

**Use case**: When both false positives and false negatives matter

### Calibration

**What it measures**: Whether predicted probabilities match actual outcomes for each group.

**Example**: If model predicts 70% probability:
- Does 70% of group A with this prediction actually get positive outcome?
- Does 70% of group B with this prediction actually get positive outcome?

**Fair if**: Predictions are equally calibrated for all groups

**Use case**: Risk scores, probability predictions

## Pre-training Metrics

### Class Balance

Measures if target variable is balanced across sensitive attribute groups.

```python
# Example: Credit default rates
Male: 20% default rate
Female: 22% default rate
Difference: 0.02 (balanced)
```

### Concept Balance

Measures correlation between sensitive attribute and target.

High correlation indicates potential bias in data collection.

### KL Divergence / JS Divergence

Measures how different the feature distributions are between groups.

Higher values indicate more different distributions, which may lead to unfair models.

## Fairness Thresholds

JusticeAI uses configurable thresholds to determine fairness violations:

```python
# Default (LGPD recommended)
evaluator = FairnessEvaluator(fairness_threshold=0.05)

# Strict
evaluator = FairnessEvaluator(fairness_threshold=0.02)

# Lenient
evaluator = FairnessEvaluator(fairness_threshold=0.10)
```

**Violations occur when**:
- Statistical Parity Diff > threshold
- Equal Opportunity Diff > threshold
- Disparate Impact < 0.80
- Equalized Odds differences > threshold

## Overall Fairness Score

JusticeAI computes an overall score (0-100) based on:

1. Number of metric violations
2. Severity of violations
3. Pre-training data quality

**Score Interpretation**:
- **90-100**: Excellent fairness
- **70-89**: Good fairness, minor issues
- **50-69**: Moderate issues, review needed
- **Below 50**: Significant fairness concerns

## Trade-offs in Fairness

!!! warning "Impossibility Theorem"
    It's mathematically impossible to satisfy all fairness metrics simultaneously (except in trivial cases). You must choose which metric(s) matter most for your use case.

### Common Trade-offs

**Statistical Parity vs Equal Opportunity**:
- Statistical parity ignores whether predictions are correct
- Equal opportunity focuses only on qualified individuals

**Individual Fairness vs Group Fairness**:
- Group fairness: Similar outcomes for groups
- Individual fairness: Similar individuals get similar predictions

**Fairness vs Accuracy**:
- Sometimes improving fairness slightly reduces overall accuracy
- JusticeAI helps you find the best balance

## Choosing the Right Metric

| Use Case | Primary Metric | Why |
|----------|---------------|-----|
| Hiring | Disparate Impact | Legal requirement (80% rule) |
| Loan Approval | Equal Opportunity | Don't deny qualified applicants |
| Medical Diagnosis | Equalized Odds | Both false pos/neg are critical |
| Marketing | Statistical Parity | Equal exposure to opportunities |
| Risk Scoring | Calibration | Probabilities must be accurate |

## Practical Recommendations

### 1. Start with Multiple Metrics
Don't rely on just one metric. JusticeAI evaluates multiple metrics to give you a complete picture.

### 2. Understand Your Context
What does "fair" mean for your specific application? Consult with domain experts and stakeholders.

### 3. Consider Base Rates
Different base rates between groups don't always indicate unfairness - they may reflect real differences in the target variable.

### 4. Iterate
Use JusticeAI's reports to identify issues, adjust your model or data, and re-evaluate.

### 5. Monitor Continuously
Fairness can drift over time. Regular audits are essential in production.

## Next Steps

- [User Guide](../guide/overview.md) - Learn all features
- [Fairness Metrics Reference](../guide/metrics.md) - Detailed metric explanations
- [Tutorials](../tutorials/index.md) - Hands-on examples
- [API Reference](../api/index.md) - Complete API documentation

## Further Reading

- [Fairness Definitions Explained](https://fairware.cs.umass.edu/papers/Verma.pdf) - Academic paper on fairness metrics
- [LGPD Guidelines](https://www.gov.br/lgpd) - Brazilian data protection law
- [BACEN Regulations](https://www.bcb.gov.br/) - Banking regulations on ML fairness
