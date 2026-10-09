
from pathlib import Path
import json

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns


# Locate project folders
ROOT = Path(__file__).resolve().parents[2]
METRICS_PATH = ROOT / "reports" / "metrics.json"
REPORTS_DIR = ROOT / "reports"

if not METRICS_PATH.exists():
    raise FileNotFoundError(
        f"Metrics file not found: {METRICS_PATH}\n"
        "Run train.py first."
    )

# Load saved model metrics
with METRICS_PATH.open("r", encoding="utf-8") as file:
    report = json.load(file)

# Convert model metrics into a table
df = pd.DataFrame(report["models"]).T

metrics = ["accuracy", "precision", "recall", "f1", "roc_auc"]

print("\nModel comparison:")
print(df[metrics].round(3).to_string())

sns.set_theme(style="whitegrid")

# Chart 1: Compare all evaluation metrics
plot_df = df[metrics].reset_index()
plot_df = plot_df.rename(columns={"index": "Model"})

plot_df = plot_df.melt(
    id_vars="Model",
    value_vars=metrics,
    var_name="Metric",
    value_name="Score",
)

plt.figure(figsize=(11, 6))
sns.barplot(data=plot_df, x="Metric", y="Score", hue="Model")
plt.ylim(0, 1)
plt.title("Student Risk Model Comparison")
plt.ylabel("Score")
plt.xlabel("Evaluation Metric")
plt.legend(title="Model")
plt.tight_layout()
plt.savefig(REPORTS_DIR / "model_comparison.png", dpi=300)
plt.show()
plt.close()

# Chart 2: Cross-validation F1 comparison
cv_df = df.reset_index().rename(columns={"index": "Model"})

plt.figure(figsize=(9, 5))
sns.barplot(data=cv_df, x="Model", y="cv_f1_mean")
plt.title("Cross-Validation F1-Score Comparison")
plt.ylabel("Mean F1-Score")
plt.xlabel("Model")
plt.ylim(0, 1)
plt.tight_layout()
plt.savefig(REPORTS_DIR / "cross_validation_f1.png", dpi=300)
plt.show()
plt.close()

print("\nCharts saved successfully:")
print(REPORTS_DIR / "model_comparison.png")
print(REPORTS_DIR / "cross_validation_f1.png")
