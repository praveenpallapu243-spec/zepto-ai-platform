import seaborn as sns
import pandas as pd

def run_eda():
    df = sns.load_dataset('titanic')
    df.to_csv("titanic.csv", index=False)

    print("Dataset Shape:", df.shape)
    missing = df.isnull().mean() * 100
    print("\nMissing Percentages:\n", missing[missing > 0])

    for col in ['age', 'fare']:
        Q1 = df[col].quantile(0.25)
        Q3 = df[col].quantile(0.75)
        IQR = Q3 - Q1
        outliers = ((df[col] < (Q1 - 1.5 * IQR)) | (df[col] > (Q3 + 1.5 * IQR))).sum()
        print(f"Outliers in {col}: {outliers}")

if __name__ == "__main__":
    run_eda()
