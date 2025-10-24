import sqlite3
import pandas as pd
import os
import matplotlib.pyplot as plt

DB_PATH = "contender.db"

if not os.path.exists(DB_PATH):
    raise FileNotFoundError(f"Database {DB_PATH} not found. Run 'contender spam' first.")

conn = sqlite3.connect(DB_PATH)

# Load transaction data: use start_timestamp and end_timestamp
df_tx = pd.read_sql("""
    SELECT run_id, start_timestamp, end_timestamp
    FROM run_txs
    WHERE end_timestamp IS NOT NULL
      AND start_timestamp IS NOT NULL
      AND end_timestamp > start_timestamp
""", conn)

# Compute latency in seconds (simple integer subtraction)
df_tx["latency_sec"] = df_tx["end_timestamp"] - df_tx["start_timestamp"]

# Filter reasonable latencies (0 < latency < 600 seconds)
df_tx = df_tx[(df_tx["latency_sec"] > 0) & (df_tx["latency_sec"] < 600)]

# Load runs: txs_per_duration is your load (TPS or TPB)
df_runs = pd.read_sql("SELECT id, txs_per_duration FROM runs", conn)
df_runs.rename(columns={"txs_per_duration": "load"}, inplace=True)

# Merge
df = pd.merge(df_tx, df_runs, left_on="run_id", right_on="id")

# Aggregate median latency per load level
agg = df.groupby("load")["latency_sec"].median().reset_index()
agg = agg.sort_values("load")

print("Load vs Median Latency:")
print(agg)

# Plot
plt.figure(figsize=(8, 5))
plt.plot(agg["load"], agg["latency_sec"], marker='o', linestyle='-')
plt.xlabel("Load (txs_per_duration → TPS if using --tps)")
plt.ylabel("Median Time-to-Inclusion (seconds)")
plt.title("Load vs Latency (from Contender DB)")
plt.grid(True)
plt.tight_layout()
plt.savefig("load_vs_latency.png")
print("\nPlot saved as load_vs_latency.png")