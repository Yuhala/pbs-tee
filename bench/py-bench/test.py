#!/usr/bin/env python3

import csv
import time
import matplotlib.pyplot as plt
from web3 import Web3
from eth_account import Account
import web3.exceptions

# -------------------------
# CONFIG
# -------------------------
RPC_URL = "http://localhost:8545"
#RPC_URL = "http://localhost:2222"

PRIVATE = "0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
SENDER = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266"
RECEIVER = "0x70997970C51812dc3A010C7d01b50e0d17dc79C8"

DURATION = 10                      # seconds to run each load level
LOAD_LEVELS = [5, 10, 20, 25, 50, 100, 200, 400, 800, 1000, 1600, 2000]
#LOAD_LEVELS = [20, 40, 60, 80, 100, 150, 200]   # tx/s sent
POLL_INTERVAL = 0.5               # seconds between mining checks
TX_TIMEOUT = 60                   # max seconds to wait for mining

CSV_FILE = "saturation_results.csv"
PLOT_FILE = "saturation_plot.png"

# -------------------------
# WEB3 SETUP
# -------------------------
w3 = Web3(Web3.HTTPProvider(RPC_URL))
assert w3.is_connected(), "Cannot connect to RPC."

chain_id = w3.eth.chain_id
gas_price = w3.eth.gas_price
nonce = w3.eth.get_transaction_count(SENDER)

print(f"Connected to chain {chain_id}")
print(f"Starting load sweep: {LOAD_LEVELS}")

# Signer
sender_account = Account.from_key(PRIVATE)

GAS_ETH = 0.01 #0.0001
# -------------------------
# SEND ONE TX
# -------------------------
def send_tx(nonce):
    tx = {
        "nonce": nonce,
        "to": RECEIVER,
        "value": w3.to_wei(GAS_ETH, "ether"),
        "gas": 21000,
        "gasPrice": gas_price,
        "chainId": chain_id,
    }
    signed = w3.eth.account.sign_transaction(tx, PRIVATE)
    tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
    return tx_hash.hex()

# -------------------------
# WAIT FOR MINING
# -------------------------
def wait_for_all_mined(tx_hashes, poll_interval=POLL_INTERVAL, timeout=TX_TIMEOUT):
    mined = 0
    pending = tx_hashes.copy()
    start_time = time.time()

    while pending and (time.time() - start_time) < timeout:
        still_waiting = []
        for h in pending:
            try:
                receipt = w3.eth.get_transaction_receipt(h)
                if receipt is None:
                    still_waiting.append(h)
                else:
                    mined += 1
            except web3.exceptions.TransactionNotFound:
                still_waiting.append(h)
        pending = still_waiting
        if pending:
            time.sleep(poll_interval)

    if pending:
        print(f"WARNING: {len(pending)} txs not mined after {timeout}s")
    return mined

# -------------------------
# MAIN LOAD SWEEP
# -------------------------
results = []

for load in LOAD_LEVELS:
    print(f"\n=== LOAD {load} tx/s ===")
    tx_hashes = []

    start_global = time.time()
    start_interval = time.time()
    count_sent = 0
    target_interval = 1.0 / load

    while time.time() - start_global < DURATION:
        tx_hash = send_tx(nonce)
        nonce += 1
        tx_hashes.append(tx_hash)
        count_sent += 1

        # maintain constant send rate
        elapsed = time.time() - start_interval
        if elapsed < target_interval:
            time.sleep(target_interval - elapsed)
        start_interval = time.time()

    print(f"Sent {count_sent} txs. Waiting for mining…")
    mined_start = time.time()
    mined = wait_for_all_mined(tx_hashes)
    mined_time = time.time() - mined_start

    mined_tps = mined / (mined_time if mined_time > 0 else 1)
    print(f"Mined {mined} txs in {mined_time:.2f}s → {mined_tps:.2f} TPS")

    results.append((load, mined_tps))

# -------------------------
# WRITE CSV
# -------------------------
with open(CSV_FILE, "w", newline="") as f:
    writer = csv.writer(f)
    writer.writerow(["index", "load_sent_tps", "mined_tps"])
    for i, (load, mined_tps) in enumerate(results):
        writer.writerow([i, load, round(mined_tps, 3)])

print(f"\nCSV saved to {CSV_FILE}")

# -------------------------
# PLOT SATURATION CURVE
# -------------------------
loads = [x[0] for x in results]
mined_values = [x[1] for x in results]

plt.figure(figsize=(8, 4))
plt.plot(loads, mined_values, marker="o")
plt.xlabel("Load (TX/s sent)")
plt.ylabel("Mined TPS")
plt.title("Throughput Saturation Curve")
plt.grid(True)
plt.tight_layout()
plt.savefig(PLOT_FILE)
print(f"Plot saved to {PLOT_FILE}")
plt.show()
