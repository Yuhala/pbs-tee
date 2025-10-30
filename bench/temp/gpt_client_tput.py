#!/usr/bin/env python3
import time
import threading
import csv
import statistics
import matplotlib.pyplot as plt
from web3 import Web3

# --- Configuration ---
RPC_URL = "http://localhost:8547"
PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
SENDER = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
RECEIVER = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"
SENDER = Web3.to_checksum_address(SENDER)
RECEIVER = Web3.to_checksum_address(RECEIVER)

# Test parameters
CLIENT_LOADS = [1, 2, 4, 8]  # number of client threads to test
TXS_PER_CLIENT = 100                           # transactions per client per test
GAS_PRICE_GWEI = 10000
CSV_FILE = "throughput_vs_clients.csv"

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

# --- Send transaction ---
def send_transaction(tx_id, latencies):
    try:
        tx = {
            "from": SENDER,
            "to": RECEIVER,
            "value": w3.to_wei(0.001, "ether"),
            "gas": 21000,
            "gasPrice": w3.to_wei(GAS_PRICE_GWEI, "gwei"),
            "nonce": get_nonce(),
            "chainId": w3.eth.chain_id,
        }
        signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
        start = time.time()
        tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
        w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)
        latencies.append(time.time() - start)
    except Exception as e:
        print(f"[TX {tx_id}] Error: {e}")

# --- Worker thread ---
def worker(thread_id, tx_count, latencies):
    for i in range(tx_count):
        send_transaction(f"{thread_id}-{i}", latencies)

# --- Benchmark function ---
def benchmark(client_count):
    print(f"\n=== Running with {client_count} clients ===")
    threads = []
    latencies = []

    start_time = time.time()
    for c in range(client_count):
        t = threading.Thread(target=worker, args=(c, TXS_PER_CLIENT, latencies))
        t.start()
        threads.append(t)
    for t in threads:
        t.join()
    total_time = time.time() - start_time

    total_txs = len(latencies)
    throughput = total_txs / total_time if total_time > 0 else 0
    avg_latency = statistics.mean(latencies) if latencies else 0

    print(f"→ Clients: {client_count}, TXs: {total_txs}, Throughput: {throughput:.2f} TX/s, Avg latency: {avg_latency:.2f}s")
    return throughput, avg_latency

# --- Main test loop ---
results = []
for clients in CLIENT_LOADS:
    thr, lat = benchmark(clients)
    results.append((clients, thr, lat))

# --- Save to CSV ---
with open(CSV_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["clients", "throughput_tx_per_s", "avg_latency_s"])
    writer.writerows(results)

print(f"\nResults saved to {CSV_FILE}")

# --- Plot throughput curve ---
plt.figure(figsize=(8, 4))
plt.plot([r[0] for r in results], [r[1] for r in results], marker="o", label="Throughput (TX/s)")
plt.title("Throughput vs Number of Clients")
plt.xlabel("Number of Clients (Threads)")
plt.ylabel("Achieved Throughput (TX/s)")
plt.grid(True)
plt.tight_layout()
plt.legend()
plt.savefig("throughput_vs_clients.png")
plt.show()
