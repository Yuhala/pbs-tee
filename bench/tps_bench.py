#!/usr/bin/env python3

import os
import random
import time
import csv
import matplotlib.pyplot as plt
from web3 import Web3
from eth_account import Account
from concurrent.futures import ThreadPoolExecutor, as_completed
from threading import Lock


# configuration
RPC_URL = "http://localhost:8545" #check op-geth http port from devnet
DURATION = 60             # total benchmark duration (seconds)
TX_RATE = 20              # transactions per second
CLIENT_THREADS = 8       # number of parallel client threads
CSV_FILE = "tps_results.csv"
PLOT_FILE = "tps_plot.png"

PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
SENDER_ADDRESS = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
RECEIVER_ADDRESS = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"

SENDER = Web3.to_checksum_address(SENDER_ADDRESS)
RECEIVER = Web3.to_checksum_address(RECEIVER_ADDRESS)

# Web3 connection
w3 = Web3(Web3.HTTPProvider(RPC_URL))
assert w3.is_connected(), "Cannot connect to RPC endpoint."

print(f"Connected to chain id: {w3.eth.chain_id}")

sender_account = Account.from_key(PRIVATE_KEY)
sender = sender_account.address
print(f"Sender: {sender}") ## this is the same as SENDER_ADDRESS above

#os._exit(0)

# Thread-safe global nonce
nonce_lock = Lock()
global_nonce = w3.eth.get_transaction_count(sender)


def get_next_nonce():
    global global_nonce
    with nonce_lock:
        n = global_nonce
        global_nonce += 1
    return n


def send_tx(nonce, gas):
    """Send a simple ETH transfer transaction."""
    tx = {
        "to": RECEIVER,
        "value": w3.to_wei(gas, "ether"),
        "gas": 21000,
        "maxFeePerGas": w3.to_wei("0.001", "gwei"),
        "maxPriorityFeePerGas": w3.to_wei("0.001", "gwei"),
        "nonce": nonce,
        "chainId": w3.eth.chain_id,
        "type": 2,
    }
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.raw_transaction)
    return tx_hash.hex()


print(f"\nStarting TPS benchmark for {DURATION} seconds at {TX_RATE} tx/s\n")

start_time = time.time()
tps_log = []

with ThreadPoolExecutor(max_workers=CLIENT_THREADS) as executor:
    for second in range(DURATION):
        second_start = time.time()
        tx_futures = []

        # Submit TX_RATE transactions for this second
        for i in range(TX_RATE):
            tx_nonce = get_next_nonce()
            gas = 0.00001 + random.random() * 1e-8 # used to vary the gas value
            future = executor.submit(send_tx, tx_nonce, gas)
            tx_futures.append(future)

        sent_tx = 0
        for future in as_completed(tx_futures):
            try:
                _ = future.result()
                sent_tx += 1
            except Exception as e:
                print(f"TX failed: {e}")

        # Compute TPS for the second
        tps = sent_tx / (time.time() - second_start)
        tps_log.append((second + 1, tps))

        print(f"Second {second+1}: {sent_tx} TXs sent | TPS = {tps:.2f}")

        # Maintain timing
        delay = 1.0 - (time.time() - second_start)
        if delay > 0:
            time.sleep(delay)

# Save CSV file
with open(CSV_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "time_sec", "tps"])
    for i, (t, tps) in enumerate(tps_log, start=1):
        writer.writerow([i, t, round(tps, 3)])

print(f"\nTPS data saved to {CSV_FILE}")

# Plot results
times = [t for t, _ in tps_log]
tps_values = [v for _, v in tps_log]

plt.figure(figsize=(8, 4))
plt.plot(times, tps_values, marker="o", label="TPS per second")
plt.title("Transaction Throughput Benchmark")
plt.xlabel("Time (seconds)")
plt.ylabel("Transactions per Second (TPS)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(PLOT_FILE)
print(f"Plot saved to {PLOT_FILE}")

plt.show()
