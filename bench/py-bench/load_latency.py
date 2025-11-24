#!/usr/bin/env python3
import time
import random
import threading
import statistics
import matplotlib.pyplot as plt
import csv
from web3 import Web3

# --- Configuration ---
RPC_URL = "http://localhost:8550"      # L2 devnet RPC endpoint
LOAD_LEVELS = [1, 2, 5, 10, 20]        # Target transaction rates (TX/s)
TXS_PER_ROUND = 50                     # Number of transactions per load level
CONCURRENCY = 2                        # Threads used to send transactions
GAS_PRICE_GWEI = 1000
ETH_VALUE = 0.0001                     # Value per TX
CSV_FILE = "load_vs_latency.csv"       # Output CSV file

#LOAD_LEVELS = [20, 40, 80, 120, 160, 180, 200]
# --- Wallet setup (devnet) ---
PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
SENDER = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
RECEIVER = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"

SENDER = Web3.to_checksum_address(SENDER)
RECEIVER = Web3.to_checksum_address(RECEIVER)

# --- Connect to devnet ---
w3 = Web3(Web3.HTTPProvider(RPC_URL))
assert w3.is_connected(), "Cannot connect to devnet!"
print(f"Connected to L2 devnet: chain_id={w3.eth.chain_id}")

# --- Thread-safe nonce handling ---
nonce_lock = threading.Lock()
nonce = w3.eth.get_transaction_count(SENDER)

def get_nonce():
    global nonce
    with nonce_lock:
        n = nonce
        nonce += 1
        return n

# --- Function to send transactions and measure latency ---
def send_transaction(tx_id, latencies, latency_lock):
    try:
        tx = {
            "from": SENDER,
            "to": RECEIVER,
            "value": w3.to_wei(ETH_VALUE, "ether"),
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
            latencies.append(latency)

        #print(f"[{tx_id}] mined in {latency:.2f}s, block {receipt.blockNumber}")
    except Exception as e:
        print(f"Error sending TX {tx_id}: {e}")

# --- Worker thread function ---
def worker(thread_id, tx_count, delay, latencies, latency_lock):
    for i in range(tx_count):
        send_transaction(f"{thread_id}-{i}", latencies, latency_lock)
        time.sleep(delay)

# --- Run benchmark across loads ---
results = []  # [(load, avg_latency), ...]

for load in LOAD_LEVELS:
    latencies = []
    latency_lock = threading.Lock()

    txs_per_thread = TXS_PER_ROUND // CONCURRENCY
    delay_between_txs = 1.0 / (load * CONCURRENCY)  # ensures total ~load TX/s

    print(f"\n--- Load: {load} TX/s ---")
    print(f"Each of {CONCURRENCY} threads sends {txs_per_thread} txs "
          f"every {delay_between_txs:.4f}s")

    threads = []
    start_round = time.time()

    for t_id in range(CONCURRENCY):
        t = threading.Thread(
            target=worker,
            args=(t_id, txs_per_thread, delay_between_txs, latencies, latency_lock)
        )
        threads.append(t)
        t.start()

    for t in threads:
        t.join()

    end_round = time.time()
    duration = end_round - start_round

    if latencies:
        avg_lat = statistics.mean(latencies)
        results.append((load, avg_lat))
        print(f"Load {load} TX/s completed in {duration:.1f}s")
        print(f"Avg latency: {avg_lat:.2f}s | Min: {min(latencies):.2f}s | Max: {max(latencies):.2f}s")
    else:
        results.append((load, None))
        print(f" No successful TXs at load {load} TX/s")

# --- Save results to CSV ---
with open(CSV_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["load_tx_per_s", "avg_latency_s"])
    for load, avg_lat in results:
        writer.writerow([load, avg_lat if avg_lat is not None else "NaN"])

print(f"\nResults saved to {CSV_FILE}")

# --- Plot from CSV ---
loads, avg_latencies = [], []
with open(CSV_FILE, "r") as f:
    reader = csv.DictReader(f)
    for row in reader:
        loads.append(float(row["load_tx_per_s"]))
        avg_latencies.append(float(row["avg_latency_s"]) if row["avg_latency_s"] != "NaN" else None)

plt.figure(figsize=(7, 4))
plt.plot(loads, avg_latencies, marker="o", linewidth=2)
plt.title("L2 Load vs Latency")
plt.xlabel("Load (TX/s sent)")
plt.ylabel("Average Latency (s)")
plt.grid(True)
plt.tight_layout()
plt.savefig("load_vs_latency.png")
plt.show()
