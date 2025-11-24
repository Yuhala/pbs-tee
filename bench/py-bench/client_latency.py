#!/usr/bin/env python3
"""
Benchmark: Number of clients (threads) vs latency and throughput on L2 devnet.
"""

import threading
import time
import csv
import matplotlib.pyplot as plt
from web3 import Web3
import statistics

# ----------------------------
# Configuration
# ----------------------------
RPC_URL = "http://localhost:8547" # devnet
#RPC_URL = "http://localhost:2222" # external builder
CHAIN_ID = 13

SENDER_PRIVATE_KEY = "0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a"
SENDER_ADDRESS = "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC"
RECEIVER_ADDRESS = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"

GAS_LIMIT = 25000
MAX_FEE_GWEI = 20
MAX_PRIORITY_FEE_GWEI = 1

TX_PER_CLIENT_PER_SEC = 100
DURATION_SEC = 10
MAX_CLIENTS_EXP = 10

CSV_FILE_NAME = "pbs_clients_latency_throughput.csv"

# ----------------------------
# Globals
# ----------------------------
completed_txs = 0
stop_event = threading.Event()
LATENCIES = []
NONCE_LOCK = threading.Lock()
GLOBAL_NONCE_COUNTER = -1

# ----------------------------
# Functions
# ----------------------------
def get_next_nonce():
    global GLOBAL_NONCE_COUNTER
    with NONCE_LOCK:
        nonce = GLOBAL_NONCE_COUNTER
        GLOBAL_NONCE_COUNTER += 1
        return nonce


def send_tx_worker():
    """Each thread continuously sends transactions until stop_event is set."""
    global completed_txs
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    account = w3.eth.account.from_key(SENDER_PRIVATE_KEY)

    max_fee_wei = w3.to_wei(MAX_FEE_GWEI, "gwei")
    max_priority_fee_wei = w3.to_wei(MAX_PRIORITY_FEE_GWEI, "gwei")
    interval = 1.0 / TX_PER_CLIENT_PER_SEC
    end_time = time.time() + DURATION_SEC

    while time.time() < end_time and not stop_event.is_set():
        start_loop = time.time()
        nonce = get_next_nonce()
        start_tx = time.time()

        try:
            tx = {
                "from": SENDER_ADDRESS,
                "to": RECEIVER_ADDRESS,
                "value": 0,
                "gas": GAS_LIMIT,
                "maxFeePerGas": max_fee_wei,
                "maxPriorityFeePerGas": max_priority_fee_wei,
                "nonce": nonce,
                "chainId": CHAIN_ID,
                "data": "0x",
                "type": 2,
            }

            signed = account.sign_transaction(tx)
            tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)

            if receipt.status == 1:
                latency = time.time() - start_tx
                with NONCE_LOCK:
                    LATENCIES.append(latency)
                    completed_txs += 1
        except Exception:
            pass

        # enforce tx rate
        elapsed = time.time() - start_loop
        sleep_time = interval - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)


def run_benchmark(num_clients):
    """Runs the benchmark for a given number of clients."""
    global completed_txs, stop_event, LATENCIES, GLOBAL_NONCE_COUNTER
    completed_txs = 0
    LATENCIES = []
    stop_event.clear()

    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    GLOBAL_NONCE_COUNTER = w3.eth.get_transaction_count(SENDER_ADDRESS, "pending")

    threads = []
    for _ in range(num_clients):
        t = threading.Thread(target=send_tx_worker)
        threads.append(t)
        t.start()

    time.sleep(DURATION_SEC)
    stop_event.set()

    for t in threads:
        t.join(timeout=5)

    # Calculate metrics
    if LATENCIES:
        avg_latency = statistics.mean(LATENCIES)
        LATENCIES.sort()
        p95_latency = LATENCIES[int(0.95 * len(LATENCIES)) - 1]
    else:
        avg_latency = 0.0
        p95_latency = 0.0

    throughput = completed_txs / DURATION_SEC
    print(f"Clients={num_clients}, TXs={completed_txs}, AvgLat={avg_latency:.2f}s, Throughput={throughput:.2f} tx/s")

    return avg_latency, p95_latency, throughput


def main():
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    if not w3.is_connected():
        print("Cannot connect to RPC.")
        return

    global CHAIN_ID
    CHAIN_ID = w3.eth.chain_id
    print(f"Connected to chain id {CHAIN_ID}")

    balance = w3.from_wei(w3.eth.get_balance(SENDER_ADDRESS), "ether")
    print(f"Sender balance: {balance:.4f} ETH")

    results = []

    for i in range(0, MAX_CLIENTS_EXP + 1):
        num_clients = 2 ** i
        avg_latency, p95_latency, throughput = run_benchmark(num_clients)
        results.append((num_clients, avg_latency, p95_latency, throughput))
        time.sleep(5)

    # Save CSV
    with open(CSV_FILE_NAME, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["num_clients", "avg_latency_s", "p95_latency_s", "throughput_tx_per_s"])
        for row in results:
            writer.writerow(row)

    # Plot 1: Latency
    clients = [r[0] for r in results]
    avg_lats = [r[1] for r in results]
    p95_lats = [r[2] for r in results]
    throughputs = [r[3] for r in results]

    plt.figure(figsize=(9, 6))
    plt.plot(clients, avg_lats, marker="o", label="Average Latency")
    plt.plot(clients, p95_lats, marker="s", linestyle="--", label="95th Percentile Latency")
    plt.xscale("log", base=2)
    plt.xlabel("Number of Clients (log scale)")
    plt.ylabel("Latency (s)")
    plt.title("Latency vs Client Concurrency")
    plt.legend()
    plt.grid(True, which="both", ls="--")
    plt.tight_layout()
    plt.savefig("latency_vs_clients.png")
    print("Saved latency_vs_clients.png")

    # Plot 2: Throughput
    plt.figure(figsize=(9, 6))
    plt.plot(clients, throughputs, marker="^", color="tab:green", linewidth=2)
    plt.xscale("log", base=2)
    plt.xlabel("Number of Clients (log scale)")
    plt.ylabel("Throughput (tx/s)")
    plt.title("Throughput vs Client Concurrency")
    plt.grid(True, which="both", ls="--")
    plt.tight_layout()
    plt.savefig("throughput_vs_clients.png")
    print("Saved throughput_vs_clients.png")

    plt.show()


if __name__ == "__main__":
    main()
