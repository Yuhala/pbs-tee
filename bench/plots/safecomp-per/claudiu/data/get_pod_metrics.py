#!/usr/bin/env python3

import pandas as pd
import sys
from pathlib import Path


def extract_component(input_file, component_name):
    input_path = Path(input_file)

    # Read CSV
    df = pd.read_csv(input_path)

    # Parse timestamp
    df["timestamp"] = pd.to_datetime(df["timestamp"])

    # Filter component
    df = df[df["component"] == component_name].copy()

    if df.empty:
        print(f"No rows found for component: {component_name}")
        return

    # Sort by timestamp
    df = df.sort_values("timestamp").reset_index(drop=True)

    # Create time index column (0, 15, 30, ...)
    df.insert(0, "time_index (s)", df.index * 15)

    # Output file in same folder as input
    output_file = input_path.parent / f"{input_path.stem}_{component_name}.csv"

    # Write CSV
    df.to_csv(output_file, index=False)

    print(f"Written: {output_file}")


if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python get_pod_metrics.py <input.csv> <component-name>")
        sys.exit(1)

    extract_component(sys.argv[1], sys.argv[2])