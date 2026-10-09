
from pathlib import Path

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

ROOT = Path(__file__).resolve().parents[2]
DATA_PATH = ROOT / "data" / "student-mat.csv"
REPORTS_PATH = ROOT / "reports"
REPORTS_PATH.mkdir(exist_ok=True)

# Load dataset
df = pd.read_csv(DATA_PATH, sep=";")

# Create at-risk target (same definition as the ML model)
df["at_risk"] = (df["G3"] < 10).astype(int)

print("=" * 50)
print("STUDENT PERFORMANCE - EDA REPORT")
print("=" * 50)

print("\n1. Dataset overview")
print("Dataset shape:", df.shape)
print("Number of students:", len(df))
print("Number of columns:", len(df.columns))

print("\n2. Missing values")
print(df.isnull().sum().sum(), "missing values in total")

print("\n3. Final grade (G3) statistics")
print(df["G3"].describe().round(2))

print("\n4. At-risk student analysis")
risk_counts = df["at_risk"].value_counts().sort_index()
risk_counts.index = ["Not at risk", "At risk"]
print(risk_counts)

risk_percentage = df["at_risk"].mean() * 100
print(f"At-risk students: {risk_percentage:.2f}%")

print("\n5. Average grade by study time")
print(df.groupby("studytime")["G3"].mean().round(2))

print("\n6. Average grade by past failures")
print(df.groupby("failures")["G3"].mean().round(2))

print("\n7. Correlation with final grade")
print(
    df.corr(numeric_only=True)["G3"]
    .sort_values(ascending=False)
    .round(2)
)

# Save a grade distribution chart
sns.set_theme(style="whitegrid")

plt.figure(figsize=(8, 5))
sns.histplot(df["G3"], bins=range(0, 22), discrete=True)
plt.title("Distribution of Final Grades (G3)")
plt.xlabel("Final Grade")
plt.ylabel("Number of Students")
plt.tight_layout()
plt.savefig(REPORTS_PATH / "grade_distribution.png", dpi=150)
plt.close()

# Save at-risk distribution chart
plt.figure(figsize=(7, 5))
sns.countplot(
    data=df,
    x="at_risk",
    hue="at_risk",
    legend=False
)
plt.title("At-Risk vs Not-at-Risk Students")
plt.xlabel("At risk (0 = No, 1 = Yes)")
plt.ylabel("Number of Students")
plt.tight_layout()
plt.savefig(REPORTS_PATH / "risk_distribution.png", dpi=150)
plt.close()

# Save average grade by study time
plt.figure(figsize=(8, 5))
sns.barplot(data=df, x="studytime", y="G3", errorbar=None)
plt.title("Average Final Grade by Study Time")
plt.xlabel("Study Time Category")
plt.ylabel("Average Final Grade")
plt.tight_layout()
plt.savefig(REPORTS_PATH / "studytime_vs_grade.png", dpi=150)
plt.close()

# Save summary report
summary_path = REPORTS_PATH / "eda_summary.txt"

with open(summary_path, "w", encoding="utf-8") as file:
    file.write("STUDENT PERFORMANCE EDA SUMMARY\n")
    file.write("=" * 35 + "\n\n")
    file.write(f"Dataset shape: {df.shape}\n")
    file.write(f"Missing values: {df.isnull().sum().sum()}\n")
    file.write(f"At-risk percentage: {risk_percentage:.2f}%\n\n")
    file.write("Final grade statistics:\n")
    file.write(df["G3"].describe().to_string())
    file.write("\n\nAverage grade by study time:\n")
    file.write(df.groupby("studytime")["G3"].mean().to_string())
    file.write("\n\nAverage grade by past failures:\n")
    file.write(df.groupby("failures")["G3"].mean().to_string())

print("\nEDA report and charts saved in:", REPORTS_PATH)
print("EDA analysis completed successfully!")
