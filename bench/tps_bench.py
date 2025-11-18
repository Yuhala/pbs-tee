#!/usr/bin/env python3

import time
import csv
import random
import matplotlib.pyplot as plt
from web3 import Web3
from eth_account import Account
from concurrent.futures import ThreadPoolExecutor, as_completed

# --------------------------
# CONFIGURATION
# --------------------------
RPC_URL = "http://localhost:8545"   # for builder playground this is the op-geth http port
DURATION = 5                             # total benchmark time (seconds)
TX_RATE = 5                               # transactions per second
CSV_FILE = "tps_results.csv"
PLOT_FILE = "tps_plot.png"

PRIVATE_KEY = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
SENDER_ADDRESS = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
RECEIVER_ADDRESS = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"

SENDER = Web3.to_checksum_address(SENDER_ADDRESS)
RECEIVER = Web3.to_checksum_address(RECEIVER_ADDRESS)


# web3 connection
w3 = Web3(Web3.HTTPProvider(RPC_URL))
assert w3.is_connected(), "Cannot connect to L2 RPC endpoint!"
print(f"Connected to chain id: {w3.eth.chain_id}")

sender_account = Account.from_key(PRIVATE_KEY)
sender = sender_account.address
print(f"Sender: {sender}")


def send_tx(nonce):
    """Send a simple ETH transfer transaction."""
    tx = {
        "to": RECEIVER_ADDRESS,
        "value": w3.to_wei(0.00001, "ether"),
        "gas": 21000,
        "maxFeePerGas": w3.to_wei("0.001", "gwei"),
        "maxPriorityFeePerGas": w3.to_wei("0.001", "gwei"),
        "nonce": nonce,
        "chainId": w3.eth.chain_id,
        "type": 2,
    }
    signed_tx = w3.eth.account.sign_transaction(tx, PRIVATE_KEY)
    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    return tx_hash.hex()


print(f"\nStarting TPS benchmark for {DURATION}s at {TX_RATE} tx/s...\n")

start_time = time.time()
tps_log = []
nonce = w3.eth.get_transaction_count(sender)

# Thread pool for parallel TX submission
with ThreadPoolExecutor(max_workers=TX_RATE * 2) as executor:
    for second in range(DURATION):
        second_start = time.time()
        tx_hashes = []

        # Submit TX_RATE transactions for this second
        for i in range(TX_RATE):
            tx_hashes.append(executor.submit(send_tx, nonce))
            nonce += 1

        # Wait for all TXs in this second
        sent_tx = 0
        for future in as_completed(tx_hashes):
            try:
                _ = future.result()
                sent_tx += 1
            except Exception as e:
                print(f"TX failed: {e}")

        elapsed = time.time() - start_time
        tps = sent_tx / (time.time() - second_start)
        tps_log.append((second + 1, tps))
        print(f"Second {second+1}: {sent_tx} TXs sent | TPS = {tps:.2f}")

        # Sleep to maintain TX_RATE
        delay = 1.0 - (time.time() - second_start)
        if delay > 0:
            time.sleep(delay)

# save in csv file
with open(CSV_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["id", "time_sec", "tps"])
    for i, (t, tps) in enumerate(tps_log, start=1):
        writer.writerow([i, t, round(tps, 3)])

print(f"\nTPS data saved to {CSV_FILE}")

# plotting
times = [t for t, _ in tps_log]
tps_values = [v for _, v in tps_log]

plt.figure(figsize=(8, 4))
plt.plot(times, tps_values, marker="o", label="TPS per second")
plt.title("L2 Transaction Throughput Benchmark")
plt.xlabel("Time (seconds)")
plt.ylabel("Transactions per Second (TPS)")
plt.grid(True)
plt.legend()
plt.tight_layout()
plt.savefig(PLOT_FILE)
print(f"Plot saved to {PLOT_FILE}")
plt.show()
