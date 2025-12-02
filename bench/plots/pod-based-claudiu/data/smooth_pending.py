#!/usr/bin/env python3

import sys
import os
import pandas as pd

def main():
    if len(sys.argv) < 2:
        print("Usage: python smooth_pending.py <input_csv_file>")
        sys.exit(1)

    input_path = sys.argv[1]

    if not os.path.isfile(input_path):
        print(f"Error: File '{input_path}' not found.")
        sys.exit(1)

    # Read input CSV
    df = pd.read_csv(input_path)

    if "num_pending_transactions" not in df.columns:
        print("Error: Input CSV must contain 'num_pending_transactions' column.")
        sys.exit(1)

    values = df["num_pending_transactions"].tolist()
    smoothed = []

    for i in range(len(values)):
        if i < len(values) - 1:
            smoothed.append((values[i] + values[i+1]) / 2)
        else:
            smoothed.append(values[i])  # Last value stays unchanged

    df["smoothed_pending_transactions"] = smoothed

    # Build output file path
    base, ext = os.path.splitext(input_path)
    output_path = f"{base}_smoothed{ext}"

    # Save
    df.to_csv(output_path, index=False)

    print(f"Smoothed file written to: {output_path}")


if __name__ == "__main__":
    main()
