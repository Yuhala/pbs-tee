#!/usr/bin/env python3
import sys
import csv
import os

# =========================
# CONFIGURATION
# =========================
# Set the Pod name you want to extract metrics for
#TARGET_POD = "beacon-85cbbc7d7b-t2cbt"   # <-- change this

TARGET_POD = "op-geth-75f4676cdc-n84lh"   # <-- change this


# =========================
# SCRIPT
# =========================
def main():
    if len(sys.argv) != 2:
        print(f"Usage: {sys.argv[0]} <input_csv_file>")
        sys.exit(1)

    input_file = sys.argv[1]

    if not os.path.isfile(input_file):
        print(f"Error: file not found: {input_file}")
        sys.exit(1)

    base, ext = os.path.splitext(input_file)
    output_file = f"{base}_cpu_ram.csv"

    rows = []

    with open(input_file, newline="") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if row.get("Pod") == TARGET_POD:
                rows.append({
                    "Timestamp": row.get("Timestamp"),
                    "CPU(m)": row.get("CPU(m)"),
                    "RAM(Mi)": row.get("RAM(Mi)")
                })

    if not rows:
        print(f"No data found for pod: {TARGET_POD}")
        sys.exit(1)

    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)

        # Header
        writer.writerow(["Index", "Timestamp", "CPU(m)", "RAM(Mi)"])

        # Data
        for idx, row in enumerate(rows):
            writer.writerow([
                idx,
                row["Timestamp"],
                row["CPU(m)"],
                row["RAM(Mi)"]
            ])

    print(f"Output written to: {output_file}")


if __name__ == "__main__":
    main()
