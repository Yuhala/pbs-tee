import requests
import matplotlib.pyplot as plt
import time
import re
import csv
from datetime import datetime

# ------------------ CONFIG ------------------
METRICS_URL = "http://127.0.0.1:9011/metrics"

# Metrics of interest — edit this list to your needs
METRICS_OF_INTEREST = [
    'reth_sync_block_validation_payload_validation_histogram{quantile="0"}',
    'reth_sync_block_validation_payload_validation_histogram{quantile="0"}',
    'reth_sync_block_validation_payload_validation_histogram{quantile="0.5"}',
    'reth_sync_block_validation_payload_validation_histogram{quantile="0.5"}', 
]

DURATION_SEC = 60           # Total time to sample (seconds)
INTERVAL_SEC = 5            # Sampling interval
CSV_FILENAME = "builder_metrics.csv"
PLOT_FILENAME = "builder_metrics_subplots.png"
# --------------------------------------------

def scrape_metrics(url):
    """Fetch Prometheus-style metrics and return a dict of {metric_name: value}."""
    try:
        resp = requests.get(url, timeout=2)
        resp.raise_for_status()
        metrics = {}
        for line in resp.text.splitlines():
            if line.startswith("#"):
                continue
            match = re.match(r"^([\w:]+)\s+([0-9.eE+-]+)$", line)
            if match:
                name, val = match.groups()
                metrics[name] = float(val)
        return metrics
    except Exception as e:
        print(f"[WARN] Error fetching metrics: {e}")
        return {}

def main():
    print(f"Scraping metrics from {METRICS_URL} every {INTERVAL_SEC}s for {DURATION_SEC}s...")
    start_time = time.time()
    samples = []
    timestamps = []

    # Collect metrics over time
    while time.time() - start_time < DURATION_SEC:
        data = scrape_metrics(METRICS_URL)
        if data:
            timestamps.append(time.time() - start_time)
            samples.append(data)
        time.sleep(INTERVAL_SEC)

    # Prepare data for each metric of interest
    series = {name: [] for name in METRICS_OF_INTEREST}
    for sample in samples:
        for name in METRICS_OF_INTEREST:
            series[name].append(sample.get(name, None))

    # ---------------- CSV SAVE ----------------
    print(f"Saving metrics to {CSV_FILENAME} ...")
    with open(CSV_FILENAME, "w", newline="") as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["time_sec"] + METRICS_OF_INTEREST)
        for i, t in enumerate(timestamps):
            row = [t] + [series[name][i] for name in METRICS_OF_INTEREST]
            writer.writerow(row)

    # ---------------- PLOTS ----------------
    print(f"Saving plot to {PLOT_FILENAME} ...")
    num_metrics = len(METRICS_OF_INTEREST)
    fig, axes = plt.subplots(num_metrics, 1, figsize=(10, 3 * num_metrics), sharex=True)

    if num_metrics == 1:
        axes = [axes]

    for ax, name in zip(axes, METRICS_OF_INTEREST):
        ax.plot(timestamps, series[name], marker='o', linestyle='-')
        ax.set_title(name)
        ax.set_ylabel("Value")
        ax.grid(True, linestyle="--", linewidth=0.5)

    axes[-1].set_xlabel("Time (seconds)")

    plt.tight_layout()
    plt.savefig(PLOT_FILENAME)
    plt.close()

    print("Done. CSV and subplot figure saved successfully.")

if __name__ == "__main__":
    main()
