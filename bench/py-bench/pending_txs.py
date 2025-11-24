#!/usr/bin/env python3
import time
import threading
import statistics
import csv
import random
import matplotlib.pyplot as plt
import pandas as pd
from web3 import Web3

# --- Configuration ---
RPC_URL = "http://localhost:8547"
LOADS_TX_PER_S = [1, 2, 5, 10, 20]  # TX/s loads to test
DURATION_PER_LOAD = 20               # seconds to run per load
MONITOR_INTERVAL = 1                 # seconds
CONCURRENCY = 3                      # number of threads sending txs
GAS_PRICE_GWEI = 1000
ETH_VALUE_MAX = 0.0001

# --- Wallet setup ---
PRIVATE_KEY = "0xac0974..."  # replace with devnet private key
SENDER = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
RECEIVER = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"

# --- Connect to devnet ---
w3 = Web3(Web3.HTTPProvider(RPC_URL))
SENDER = w3.to_checksum_address(SENDER)
RECEIVER = w3.to_checksum_address(RECEIVER)
assert w3.is_connected(), "Cannot connect to devnet!"
print(f"Connected to L2 devnet: chain_id={w3.eth.chain_id}")

# --- CSV files ---
LATENCY_CSV = "load_vs_latency.csv"
PENDING_CSV = "pending_txs.csv"
with open(LATENCY_CSV, "w", newline="") as f:
    csv.writer(f).writerow(["load_tx_per_s", "avg_latency_s"])
with open(PENDING_CSV, "w", newline="") as f:
    csv.writer(f).writerow(["load_tx_per_s", "time_s", "pending_txs"])

# --- Thread-safe nonce handling ---
nonce_lock = threading.Lock()
latency_lock = threading.Lock()
csv_lock = threading.Lock()

def get_nonce():
    global nonce
    with nonce_lock:
        n = nonce
        nonce += 1
        return n

# --- Transaction sending ---
def send_transaction(tx_id, latencies_list):
    try:
        tx = {
            "from": SENDER,
            "to": RECEIVER,
            "value": w3.to_wei(random.random() * ETH_VALUE_MAX, "ether"),
            "gas": 21000,
            "gasPrice": w3.to_wei(GAS_PRICE_GWEI, "gwei"),
            "nonce": get_nonce(),
            "chainId": w3.eth.chain_id,
        }
        signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        start = time.time()
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)
        latency = time.time() - start
        with latency_lock:
            latencies_list.append(latency)
    except Exception as e:
        print(f"Error sending TX {tx_id}: {e}")

# --- Worker thread for sending txs at a given load ---
def tx_worker(tx_per_s, duration, latencies_list):
    interval = 1.0 / tx_per_s
    end_time = time.time() + duration
    tx_id = 0
    while time.time() < end_time:
        send_transaction(tx_id, latencies_list)
        tx_id += 1
        time.sleep(interval)

# --- Monitor mempool thread ---
def monitor_pending(tx_per_s, duration):
    start_time = time.time()
    while time.time() - start_time < duration:
        try:
            status = w3.provider.make_request("txpool_status", {})
            pending = int(status["result"]["pending"], 16)
        except Exception:
            pending = -1
        timestamp = time.time() - start_time
        with csv_lock:
            with open(PENDING_CSV, "a", newline="") as f:
                writer = csv.writer(f)
                writer.writerow([tx_per_s, timestamp, pending])
        time.sleep(MONITOR_INTERVAL)

# --- Main loop over loads ---
for load in LOADS_TX_PER_S:
    print(f"\nRunning load test: {load} TX/s for {DURATION_PER_LOAD}s")
    # reset nonce for this run
    nonce = w3.eth.get_transaction_count(SENDER)
    latencies = []

    # start tx threads
    threads = [threading.Thread(target=tx_worker, args=(load, DURATION_PER_LOAD, latencies))
               for _ in range(CONCURRENCY)]
    # start monitor thread
    monitor_thread = threading.Thread(target=monitor_pending, args=(load, DURATION_PER_LOAD))
    monitor_thread.start()

    for t in threads:
        t.start()
    for t in threads:
        t.join()
    monitor_thread.join()

    # --- Save average latency for this load ---
    if latencies:
        avg_latency = statistics.mean(latencies)
        print(f"Load {load} TX/s, avg latency: {avg_latency:.2f}s over {len(latencies)} txs")
        with open(LATENCY_CSV, "a", newline="") as f:
            csv.writer(f).writerow([load, avg_latency])
    else:
        print(f"No transactions mined for load {load} TX/s")

# --- Plot Load vs Latency ---
df_lat = pd.read_csv(LATENCY_CSV)
plt.figure(figsize=(8,4))
plt.plot(df_lat["load_tx_per_s"], df_lat["avg_latency_s"], marker="o")
plt.title("Load vs Average Latency")
plt.xlabel("Load (TX/s)")
plt.ylabel("Avg Latency (s)")
plt.grid(True)
plt.tight_layout()
plt.savefig("load_vs_latency.png")
plt.show()

# --- Plot Pending TXs over Time ---
df_pend = pd.read_csv(PENDING_CSV)
plt.figure(figsize=(8,4))
for load in LOADS_TX_PER_S:
    df_subset = df_pend[df_pend["load_tx_per_s"]==load]
    plt.plot(df_subset["time_s"], df_subset["pending_txs"], marker="o", label=f"{load} TX/s")
plt.title("Pending Transactions over Time")
plt.xlabel("Time (s)")
plt.ylabel("Pending TXs")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.savefig("pending_txs_over_time.png")
plt.show()
