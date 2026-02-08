"""
Simple example of creating a fairness report.

This example demonstrates the basic usage of JusticeAI to create
a fairness report from model predictions.
"""

import numpy as np
import pandas as pd
from sklearn.datasets import make_classification
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split

from justiceai.reports import FairnessReport

# Set random seed for reproducibility
np.random.seed(42)

# Generate synthetic dataset
print("Generating synthetic dataset...")
X, y = make_classification(
    n_samples=1000,
    n_features=10,
    n_informative=5,
    n_redundant=3,
    n_classes=2,
    random_state=42,
)

# Create a sensitive attribute (e.g., gender)
# With intentional bias: group A has higher positive rate
sensitive = pd.Series(np.random.choice(["Group_A", "Group_B"], 1000))

# Make data slightly biased: Group A more likely to be class 1
bias_mask = sensitive == "Group_A"
y[bias_mask & (np.random.rand(1000) < 0.2)] = 1

# Split data
X_train, X_test, y_train, y_test, sens_train, sens_test = train_test_split(
    X, y, sensitive, test_size=0.3, random_state=42
)

# Train a simple model
print("Training RandomForest model...")
model = RandomForestClassifier(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# Make predictions
print("Making predictions...")
y_pred = model.predict(X_test)
y_pred_proba = model.predict_proba(X_test)[:, 1]

# Convert to DataFrame for pre-training metrics
X_test_df = pd.DataFrame(X_test, columns=[f"feature_{i}" for i in range(10)])

# Create fairness report
print("\nCreating fairness report...")
report = FairnessReport.from_predictions(
    y_true=y_test,
    y_pred=y_pred,
    sensitive_attr=sens_test,
    X=X_test_df,
    y_pred_proba=y_pred_proba,
)

# Display summary
print("\n" + "=" * 60)
print("FAIRNESS ANALYSIS SUMMARY")
print("=" * 60)

summary = report.get_summary()
print(f"\nOverall Fairness Score: {report.get_overall_score():.1f}/100")
print(f"Passes Basic Fairness: {'✓ Yes' if report.passes_fairness() else '✗ No'}")
print(f"Number of Violations: {summary['n_violations']}")
print(f"Disparate Impact Ratio: {summary.get('disparate_impact_ratio', 1.0):.3f}")
print(f"Statistical Parity Diff: {summary.get('statistical_parity_diff', 0.0):.3f}")

# Display issues
issues = report.get_issues()
if issues:
    print("\n" + "-" * 60)
    print("DETECTED ISSUES")
    print("-" * 60)
    for i, issue in enumerate(issues, 1):
        print(f"\n{i}. [{issue['severity'].upper()}] {issue['metric']}")
        print(f"   Issue: {issue['message']}")
        print(f"   Impact: {issue['impact']}")

# Display recommendations
print("\n" + "-" * 60)
print("RECOMMENDATIONS")
print("-" * 60)

recommendations = report.get_recommendations()
for i, rec in enumerate(recommendations, 1):
    print(f"\n{i}. [{rec['priority'].upper()}] {rec['action']}")
    print(f"   {rec['description']}")

# Save HTML report
output_path = "fairness_report_example.html"
print("\n" + "=" * 60)
print(f"Saving HTML report to: {output_path}")
report.save_html(output_path)
print("✓ Report saved successfully!")

print("\nTo view the report, open 'fairness_report_example.html' in your browser")
print("Or run: report.show() to open it automatically")

# Optionally, open in browser (commented out for example)
# report.show(output_path)

print("\n" + "=" * 60)
print("Example complete!")
print("=" * 60)
