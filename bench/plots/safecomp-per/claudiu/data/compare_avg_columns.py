#!/usr/bin/env python3
import sys
import csv

def read_column_avg(filepath, col_index_1based):
    values = []
    col_idx = col_index_1based - 1  # convert to 0-based

    with open(filepath, newline='') as f:
        reader = csv.reader(f)
        header = next(reader, None)  # skip header if present

        for row in reader:
            if len(row) <= col_idx:
                continue
            try:
                val = float(row[col_idx])
                values.append(val)
            except ValueError:
                continue  # skip non-numeric rows

    if not values:
        raise ValueError(f"No numeric values found in column {col_index_1based} of {filepath}")

    return sum(values) / len(values), len(values)

def main():
    if len(sys.argv) != 4:
        print("Usage: python compare_csv_avg.py <file1.csv> <file2.csv> <column_index_1based>")
        sys.exit(1)

    file1 = sys.argv[1]
    file2 = sys.argv[2]
    col_index = int(sys.argv[3])

    avg1, n1 = read_column_avg(file1, col_index)
    avg2, n2 = read_column_avg(file2, col_index)

    diff = avg1 - avg2
    pct = (diff / avg2) * 100 if avg2 != 0 else float('inf')
    times = (avg1 / avg2) if avg2 != 0 else float('inf')

    print(f"File 1 ({file1}) average (col {col_index}): {avg1:.3f}  [n={n1}]")
    print(f"File 2 ({file2}) average (col {col_index}): {avg2:.3f}  [n={n2}]")
    print(f"Absolute difference: {diff:.3f}")
    print(f"Percentage difference: {pct:.2f}%")
    print(f"Times higher: {times:.3f}×")

if __name__ == "__main__":
    main()