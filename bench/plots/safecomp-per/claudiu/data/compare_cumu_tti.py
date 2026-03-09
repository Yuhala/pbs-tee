import pandas as pd
import sys

def time_at_percent(df, target):
    """Return the earliest timestamp where percent_included >= target."""
    row = df[df["percent_included"] >= target].iloc[0]
    return row["timestamp"]

def main(file1, file2):

    df1 = pd.read_csv(file1)
    df2 = pd.read_csv(file2)

    percentiles = [0.5, 0.9, 0.95]

    print("\nComparison of inclusion times\n")
    print("Percentile | File1 (ms) | File2 (ms) | Improvement (ms) | Speedup")
    print("---------------------------------------------------------------")

    for p in percentiles:
        t1 = time_at_percent(df1, p)
        t2 = time_at_percent(df2, p)

        improvement = t1 - t2
        speedup = t1 / t2 if t2 != 0 else float("inf")

        print(f"{int(p*100):>9}% | {t1:>10} | {t2:>10} | {improvement:>15} | {speedup:.2f}x")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python compare_cdf.py file1.csv file2.csv")
        sys.exit(1)

    main(sys.argv[1], sys.argv[2])