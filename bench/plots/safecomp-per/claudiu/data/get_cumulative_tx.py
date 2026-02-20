#!/usr/bin/env python3

import sys
import os
import pandas as pd
import math

def main():
    if len(sys.argv) != 2:
        print("Usage: python cumu_tti.py <input_csv>")
        sys.exit(1)

    input_csv = sys.argv[1]

    if not os.path.exists(input_csv):
        print(f"Error: File not found -> {input_csv}")
        sys.exit(1)

    # Load CSV
    df = pd.read_csv(input_csv)

    # Check required columns
    required_cols = {"start_time", "end_time"}
    if not required_cols.issubset(df.columns):
        print("Error: CSV must contain 'start_time' and 'end_time' columns")
        sys.exit(1)

    # Compute TTI (in seconds)
    df["tti"] = df["end_time"] - df["start_time"]

    # Total number of transactions
    N = len(df)

    # Max TTI (for time axis)
    max_tti = int(math.ceil(df["tti"].max()))

    # Build time-based CDF
    output_rows = []

    for t in range(0, max_tti + 1):
        included = (df["tti"] <= t).sum()
        percent = (included / N) * 100.0
        output_rows.append([t, percent])

    out_df = pd.DataFrame(output_rows, columns=["timestamp", "percent_included"])

    # Output file name
    base_name = os.path.splitext(input_csv)[0]
    output_csv = f"{base_name}_cumu_tti.csv"

    # Save
    out_df.to_csv(output_csv, index=False)

    print(f"Output written to: {output_csv}")

if __name__ == "__main__":
    main()
