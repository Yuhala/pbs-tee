#!/usr/bin/env python3
"""
Replay real Optimism L2 blocks for two PBS designs:
1. PBS with TEE-enabled builder (strict ordering)
2. PBS with non-TEE builder (allowing reordering)
Collects metrics and plots results.
"""

import json
import random
import csv
import matplotlib.pyplot as plt
from web3 import Web3
from datetime import datetime
import time
#from web3.middleware import geth_poa_middleware  # correct import in v6
from web3.middleware import poa

# ----------------------------
# CONFIGURATION
# ----------------------------
RPC_URL = "https://mainnet.optimism.io"
START_BLOCK = 10000000  # example starting block
NUM_BLOCKS = 100
END_BLOCK = START_BLOCK + NUM_BLOCKS    # example ending block (fetch 11 blocks)
OUTPUT_TRACE_FILE = "optimism_trace.json"

# Simulation settings
TEE_ENABLED = True  # If True, simulate strict ordering
METRICS_CSV = "pbs_metrics.csv"
PLOT_FILE = "pbs_simulation.png"

# ----------------------------
# CONNECT TO OPTIMISM
# ----------------------------
w3 = Web3(Web3.HTTPProvider(RPC_URL))

# Inject POA middleware at the base layer
w3.middleware_onion.inject(geth_poa_middleware, layer=0)

if w3.is_connected():
    latest_block = w3.eth.block_number
    print(f"Connected to Optimism: latest block {latest_block}")
else:
    print("Cannot connect to Optimism RPC")

# ----------------------------
# FETCH BLOCKS AND TRANSACTIONS
# ----------------------------
trace_blocks = []
print(f"Fetching blocks {START_BLOCK} to {END_BLOCK}...")

for blk_num in range(START_BLOCK, END_BLOCK + 1):
    block = w3.eth.get_block(blk_num, full_transactions=True)
    block_trace = {
        "number": block.number,
        "timestamp": block.timestamp,
        "transactions": [
            {
                "hash": tx.hash.hex(),
                "from": tx['from'],
                "to": tx['to'],
                "value": tx['value'],
                "gas": tx['gas'],
                "nonce": tx['nonce']
            }
            for tx in block.transactions
        ]
    }
    trace_blocks.append(block_trace)
    print(f"Fetched block {blk_num}, {len(block.transactions)} txs")
    time.sleep(0.2)  # avoid overwhelming RPC

# Save trace for reuse
with open(OUTPUT_TRACE_FILE, "w") as f:
    json.dump(trace_blocks, f, indent=2)
print(f"Saved trace to {OUTPUT_TRACE_FILE}")

# ----------------------------
# SIMULATE PBS DESIGNS
# ----------------------------
def replay_blocks(blocks, tee=True):
    """
    Simulate block replay under PBS design.
    tee=True: preserve transaction order (TEE builder)
    tee=False: allow random reordering per block (non-TEE builder)
    """
    total_txs = 0
    reordered_txs = 0
    latencies = []

    for blk in blocks:
        txs = blk["transactions"].copy()
        if not tee:
            # shuffle to simulate reordering
            random.shuffle(txs)
            reordered_txs += len(txs)

        # simple latency simulation: 0.1s per tx
        for tx in txs:
            latencies.append(0.1)  # placeholder for realistic measurement
        total_txs += len(txs)

    avg_latency = sum(latencies) / len(latencies) if latencies else 0
    throughput = total_txs / (len(latencies)*0.1) if latencies else 0
    return {
        "total_txs": total_txs,
        "avg_latency": avg_latency,
        "throughput": throughput,
        "reordered_txs": reordered_txs
    }

# Run both designs
metrics_tee = replay_blocks(trace_blocks, tee=True)
metrics_non_tee = replay_blocks(trace_blocks, tee=False)

print("\nSimulation results:")
print("TEE Builder:", metrics_tee)
print("Non-TEE Builder:", metrics_non_tee)

# ----------------------------
# SAVE METRICS TO CSV
# ----------------------------
with open(METRICS_CSV, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["Design", "Total TXs", "Avg Latency (s)", "Throughput (tx/s)", "Reordered TXs"])
    writer.writerow(["TEE Builder", metrics_tee["total_txs"], metrics_tee["avg_latency"], metrics_tee["throughput"], metrics_tee["reordered_txs"]])
    writer.writerow(["Non-TEE Builder", metrics_non_tee["total_txs"], metrics_non_tee["avg_latency"], metrics_non_tee["throughput"], metrics_non_tee["reordered_txs"]])

print(f"Metrics saved to {METRICS_CSV}")

# ----------------------------
# PLOT RESULTS
# ----------------------------
labels = ["TEE Builder", "Non-TEE Builder"]
throughputs = [metrics_tee["throughput"], metrics_non_tee["throughput"]]
avg_latencies = [metrics_tee["avg_latency"], metrics_non_tee["avg_latency"]]

fig, ax1 = plt.subplots(figsize=(8,5))

color = 'tab:blue'
ax1.set_xlabel('PBS Design')
ax1.set_ylabel('Throughput (tx/s)', color=color)
ax1.bar(labels, throughputs, color=color, alpha=0.6)
ax1.tick_params(axis='y', labelcolor=color)

ax2 = ax1.twinx()
color = 'tab:red'
ax2.set_ylabel('Avg Latency (s)', color=color)
ax2.plot(labels, avg_latencies, color=color, marker='o', linewidth=2)
ax2.tick_params(axis='y', labelcolor=color)

plt.title("PBS Simulation: TEE vs Non-TEE Builder")
plt.tight_layout()
plt.savefig(PLOT_FILE)
plt.show()
print(f"Plot saved to {PLOT_FILE}")
