#!/usr/bin/env python3
import sys
import csv
import os

# =========================
# SCRIPT
# =========================
def main():
    if len(sys.argv) != 3:
        print(f"Usage: {sys.argv[0]} <input_csv_file> <pod_prefix>")
        print(f"Example: {sys.argv[0]} metrics.csv op-geth")
        sys.exit(1)

    input_file = sys.argv[1]
    pod_prefix = sys.argv[2]   # e.g. "op-geth", "op-node", "beacon"

    if not os.path.isfile(input_file):
        print(f"Error: file not found: {input_file}")
        sys.exit(1)

    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_{pod_prefix}_cpu_ram.csv"

    rows = []

    with open(input_file, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            pod_name = row.get("Pod", "")
            if pod_name.startswith(pod_prefix):
                rows.append({
                    "Timestamp": row.get("Timestamp"),
                    "CPU(m)": row.get("CPU(m)"),
                    "RAM(Mi)": row.get("RAM(Mi)"),
                    "Pod": pod_name
                })

    if not rows:
        print(f"No data found for pods starting with: {pod_prefix}")
        sys.exit(1)

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)

        # Header
        writer.writerow(["Index", "Pod", "Timestamp", "CPU(m)", "RAM(Mi)"])

        # Data
        for idx, row in enumerate(rows):
            writer.writerow([
                idx,
                row["Pod"],
                row["Timestamp"],
                row["CPU(m)"],
                row["RAM(Mi)"]
            ])

    print(f"Output written to: {output_file}")
    print(f"Matched prefix: {pod_prefix}")
    print(f"Rows extracted: {len(rows)}")


if __name__ == "__main__":
    main()
