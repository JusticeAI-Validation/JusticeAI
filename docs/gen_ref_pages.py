"""Generate API reference pages automatically."""

from pathlib import Path

import mkdocs_gen_files

# Package root
package_root = Path("justiceai")

# Navigation items for API reference
nav = mkdocs_gen_files.Nav()

# Modules to document
modules = [
    # Main API
    ("justiceai", "Main API"),
    ("justiceai.fairness_evaluator", "FairnessEvaluator"),
    ("justiceai.api", "Convenience API"),
    ("justiceai.reports", "Reports"),
    ("justiceai.reports.fairness_report", "FairnessReport"),
    # Core
    ("justiceai.core.adapters", "Model Adapters"),
    ("justiceai.core.adapters.base_adapter", "BaseModelAdapter"),
    ("justiceai.core.adapters.sklearn_adapter", "SklearnAdapter"),
    ("justiceai.core.metrics.posttrain", "Post-training Metrics"),
    ("justiceai.core.metrics.pretrain", "Pre-training Metrics"),
    ("justiceai.core.metrics.calculator", "Metrics Calculator"),
]

for module_path, title in modules:
    # Create markdown file for each module
    doc_path = Path("api", f"{module_path.replace('.', '/')}.md")

    with mkdocs_gen_files.open(doc_path, "w") as f:
        # Write module documentation header
        f.write(f"# {title}\n\n")
        f.write(f"::: {module_path}\n")
        f.write("    options:\n")
        f.write("      show_source: true\n")
        f.write("      heading_level: 2\n")

    # Add to navigation
    parts = module_path.split(".")
    nav[parts] = doc_path.as_posix()

# Write navigation file
with mkdocs_gen_files.open("api/SUMMARY.md", "w") as nav_file:
    nav_file.writelines(nav.build_literate_nav())
