#!/usr/bin/env python3
import time
import random
import threading
import statistics
import matplotlib.pyplot as plt
from web3 import Web3

# --- Configuration ---
RPC_URL = "http://localhost:8547"      # L2 devnet RPC endpoint
NUM_TXS = 100                          # Total transactions to send
CONCURRENCY = 3                        # Number of concurrent threads
SLEEP_BETWEEN_TXS = 0.05               # Seconds between txs per thread
GAS_PRICE_GWEI = 1000
ETH_VALUE_MAX = 0.0001                  # Max ether per tx

# --- Wallet setup ---
PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"  # insert your devnet key
SENDER = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"  # corresponding address
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

# --- Metrics ---
latencies = []
latency_lock = threading.Lock()

# --- Transaction sending ---
def send_transaction(tx_id):
    tx = {
        "from": SENDER,
        "to": RECEIVER,  # send to self (no-op)
        "value": w3.to_wei(0.01, "ether"),
        "gas": 21000,
        "gasPrice": w3.to_wei(GAS_PRICE_GWEI, "gwei"),
        "nonce": get_nonce(),
        "chainId": w3.eth.chain_id,
    }
    signed = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)

    #tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    start = time.time()
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)
    latency = time.time() - start

    with latency_lock:
        latencies.append(latency)

    print(f"[TX {tx_id}] Mined in {latency:.2f}s, block {receipt.blockNumber}")

# --- Worker threads ---
def worker(thread_id, tx_count):
    for i in range(tx_count):
        try:
            send_transaction(f"{thread_id}-{i}")
        except Exception as e:
            print(f"Error sending TX {thread_id}-{i}: {e}")
        time.sleep(SLEEP_BETWEEN_TXS)

# --- Run load test ---
threads = []
txs_per_thread = NUM_TXS // CONCURRENCY

print(f"Sending {NUM_TXS} transactions using {CONCURRENCY} threads...")

for t_id in range(CONCURRENCY):
    t = threading.Thread(target=worker, args=(t_id, txs_per_thread))
    threads.append(t)
    t.start()

for t in threads:
    t.join()

# --- Report ---
if latencies:
    print("\nLoad test completed")
    print(f"Sent {len(latencies)} transactions.")
    print(f"Avg latency: {statistics.mean(latencies):.2f}s")
    print(f"Min latency: {min(latencies):.2f}s")
    print(f"Max latency: {max(latencies):.2f}s")
else:
    print("No transactions were successfully sent.")

# --- Plot ---
plt.figure(figsize=(8, 4))
plt.plot(latencies, marker="o")
plt.title("L2 Transaction Latency (seconds)")
plt.xlabel("Transaction #")
plt.ylabel("Latency (s)")
plt.grid(True)
plt.tight_layout()
plt.savefig("latency_graph.png")
plt.show()
