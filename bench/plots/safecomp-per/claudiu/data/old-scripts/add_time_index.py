#!/usr/bin/env python3

import sys
import os
import pandas as pd

def main():
    if len(sys.argv) != 2:
        print("Usage: python add_time_index.py <input_csv>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not input_file.endswith(".csv"):
        print("Error: Input file must be a .csv file")
        sys.exit(1)

    # Read CSV
    df = pd.read_csv(input_file)

    # Create new index column (0, 5, 10, ...)
    df.insert(0, "index_s", [i * 15 for i in range(len(df))])

    # Build output filename
    base_name = os.path.splitext(input_file)[0]
    output_file = f"{base_name}_cpu_ram.csv"

    # Save CSV
    df.to_csv(output_file, index=False)

    print(f"Output written to: {output_file}")

if __name__ == "__main__":
    main()