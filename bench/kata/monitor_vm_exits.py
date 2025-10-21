#!/usr/bin/env python3
"""
Monitor KVM VM exits for a QEMU process using perf and log to CSV.

Usage:
    python3 monitor_vm_exits.py <qemu_pid> [interval_seconds] [output.csv]

Example:
    python3 monitor_vm_exits.py 12345 1 vm_exits.csv
"""

import sys
import subprocess
import time
import csv

def get_vm_exit_count(qemu_pid):
    """
    Use perf to get the current number of KVM exits for a given QEMU PID.
    Returns the exit count as int.
    """
    try:
        cmd = ["perf", "stat", "-x,", "-e", "kvm:kvm_exit", "-p", str(qemu_pid), "-- sleep 0.01"]
        result = subprocess.run(cmd, capture_output=True, text=True)
        for line in result.stderr.splitlines():
            if line.strip() and "kvm:kvm_exit" in line:
                # perf outputs CSV-style because of -x,
                count = line.split(",")[0].strip()
                return int(count.replace("-", "0"))
    except Exception as e:
        print(f"Error reading perf for PID {qemu_pid}: {e}")
    return 0

def main():
    if len(sys.argv) < 2:
        print("Usage: python3 monitor_vm_exits.py <qemu_pid> [interval_seconds] [output.csv]")
        sys.exit(1)

    qemu_pid = int(sys.argv[1])
    interval = float(sys.argv[2]) if len(sys.argv) > 2 else 1.0
    output_file = sys.argv[3] if len(sys.argv) > 3 else "vm_exits.csv"

    print(f"Monitoring VM exits for PID {qemu_pid} every {interval}s, logging to {output_file}")

    with open(output_file, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["timestamp", "vm_exits"])

        while True:
            timestamp = time.time()
            exits = get_vm_exit_count(qemu_pid)
            writer.writerow([timestamp, exits])
            csvfile.flush()
            print(f"[{time.strftime('%H:%M:%S')}] VM exits: {exits}")
            time.sleep(interval)

if __name__ == "__main__":
    main()
