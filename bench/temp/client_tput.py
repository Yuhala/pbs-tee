#!/usr/bin/env python3

import threading
import time
import csv
import matplotlib.pyplot as plt
from web3 import Web3


# ----------------------------
# HARDCODED CONFIGURATION
# ----------------------------
RPC_URL = "http://localhost:8547"
CHAIN_ID = 133 #use 

# 🔑 Replace with your Builder Playground devnet keys
SENDER_PRIVATE_KEY = "0x5de4111afa1a4b94908f83103eb1f1706367c2e68ca870fc3fb9a804cdab365a"
SENDER_ADDRESS = "0x3C44CdDdB6a900fa2b585dd299e03d12FA4293BC"
RECEIVER_ADDRESS = "0xf39Fd6e51aad88F6F4ce6aB8827279cffFb92266" #SENDER_ADDRESS  # self-transfer


# Benchmark settings
GAS_LIMIT = 1000
# Using EIP-1559 standard
MAX_FEE_GWEI = 20
MAX_PRIORITY_FEE_GWEI = 1

TX_PER_CLIENT_PER_SEC = 10
DURATION_SEC = 5
MAX_CLIENTS_EXP = 7  # 2^0 to 2^7 → 1 to 128

# Global state for concurrent access
completed_txs = 0
stop_event = threading.Event()

# CRITICAL FIX: Nonce is managed globally and sequentially
NONCE_LOCK = threading.Lock()
# This counter will be initialized in main() with the latest 'pending' nonce
GLOBAL_NONCE_COUNTER = -1 

def get_next_sequential_nonce():
    """
    Acquires the lock, retrieves the current global nonce, increments the
    global counter, and returns the reserved nonce.
    """
    global GLOBAL_NONCE_COUNTER
    with NONCE_LOCK:
        nonce = GLOBAL_NONCE_COUNTER
        GLOBAL_NONCE_COUNTER += 1 # Reserve the next sequential nonce
        return nonce

def send_tx_worker():
    """Worker function to continuously send transactions."""
    global completed_txs
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    
  
    account = w3.eth.account.from_key(SENDER_PRIVATE_KEY)
    
    # Convert GWEI to WEI once
    max_fee_wei = w3.to_wei(MAX_FEE_GWEI, 'gwei')
    max_priority_fee_wei = w3.to_wei(MAX_PRIORITY_FEE_GWEI, 'gwei')

    interval = 1.0 / TX_PER_CLIENT_PER_SEC
    end_time = time.time() + DURATION_SEC

    while time.time() < end_time and not stop_event.is_set():
        start_time = time.time()
        
        # Get the next available sequential nonce from the global counter
        nonce = get_next_sequential_nonce()
        
        try:
            # 1. Transaction Parameters (using EIP-1559 format, type 2)
            tx = {
                'from': SENDER_ADDRESS,
                'to': RECEIVER_ADDRESS,
                'value': 0,
                'gas': GAS_LIMIT,
                # EIP-1559 fields
                'maxFeePerGas': max_fee_wei,
                'maxPriorityFeePerGas': max_priority_fee_wei,
                'nonce': nonce,
                'chainId': CHAIN_ID,
                'data': '0x',
                'type': 2 
            }
            
            # 2. Sign and Send
            signed = account.sign_transaction(tx)
            tx_hash = w3.eth.send_raw_transaction(signed.raw_transaction)
            
            # 3. Wait for Receipt (BLOCKING - limits max TPS)
            # This logic counts completed TXs by waiting for confirmation.
            receipt = w3.eth.wait_for_transaction_receipt(tx_hash, timeout=60)
            
            if receipt.status == 1:
                # Use lock to update shared counter safely
                with NONCE_LOCK: 
                    completed_txs += 1
            # Note: If status != 1, the transaction failed but the nonce was still consumed.
            
        except TransactionNotFound:
             # This can happen if the transaction is dropped by the node's tx pool (e.g., too many pending)
             # The nonce assigned to this thread is now effectively skipped/failed.
             pass
        except Exception as e:
            # Catch all other RPC/connection errors
            pass
            
        # Enforce the per-client rate limit
        elapsed = time.time() - start_time
        sleep_time = interval - elapsed
        if sleep_time > 0:
            time.sleep(sleep_time)

def run_benchmark(num_clients):
    """Initializes the global nonce and runs the multi-threaded test."""
    global completed_txs, stop_event, GLOBAL_NONCE_COUNTER
    completed_txs = 0
    stop_event.clear()

    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    
    # CRITICAL: Initialize the global nonce counter with the current pending nonce
    GLOBAL_NONCE_COUNTER = w3.eth.get_transaction_count(SENDER_ADDRESS, 'pending')
    
    threads = []
    for _ in range(num_clients):
        t = threading.Thread(target=send_tx_worker)
        threads.append(t)
        t.start()

    time.sleep(DURATION_SEC)
    stop_event.set()

    for t in threads:
        t.join(timeout=10)

    throughput = completed_txs / DURATION_SEC
    print(f"Clients: {num_clients:3d} | Completed: {completed_txs:4d} | Throughput: {throughput:6.2f} TPS")
    return throughput

def main():
    w3 = Web3(Web3.HTTPProvider(RPC_URL))
    
    if not w3.is_connected():
        print(f"Could not connect to RPC at {RPC_URL}. Exiting.")
        return
    
    # --- AUTOMATIC CHAIN_ID FETCH ---
    try:
        CHAIN_ID = w3.eth.chain_id
        print(f"Automatically determined Chain ID: {CHAIN_ID}")
    except Exception as e:
        print(f"Failed to get Chain ID from RPC: {e}. Exiting.")
        return
    # --------------------------------

    # Initial balance check
    try:
        balance = w3.from_wei(w3.eth.get_balance(SENDER_ADDRESS), 'ether')
        if balance < 0.1:
            print(f"⚠️ Low balance ({balance:.4f} ETH) on L2 for {SENDER_ADDRESS}. Consider funding.")
        print(f"Current L2 balance: {balance:.4f} ETH")
    except Exception:
        print("Failed to get balance. Check RPC connection and address.")
        return

    print(f"Starting benchmark (duration={DURATION_SEC}s, per-client rate={TX_PER_CLIENT_PER_SEC} TPS)")
    print(f"Sender: {SENDER_ADDRESS}")
    print(f"Using EIP-1559: Max Fee = {MAX_FEE_GWEI} GWEI")

    results = []
    row_id = 0

    for i in range(0, MAX_CLIENTS_EXP + 1):
        num_clients = 2 ** i
        throughput = run_benchmark(num_clients)
        results.append((row_id, num_clients, throughput))
        row_id += 1
        time.sleep(5) # Cooldown between runs

    # Save to CSV
    output_file = "throughput_results.csv"
    with open(output_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["row_id", "num_clients", "throughput_tps"])
        writer.writerows(results)

    # === PLOTTING ===
    num_clients_list = [r[1] for r in results]
    throughput_list = [r[2] for r in results]

    plt.figure(figsize=(8, 5))
    plt.plot(num_clients_list, throughput_list, marker='o', linestyle='-', linewidth=2, markersize=6)
    plt.xscale('log', base=2)
    plt.xlabel("Number of Clients (log scale)")
    plt.ylabel("Achieved Throughput (TPS)")
    plt.title("L2 Devnet Throughput vs. Client Concurrency")
    plt.grid(True, which="both", ls="--", linewidth=0.5)
    plt.xticks(num_clients_list, labels=[str(n) for n in num_clients_list])
    plt.tight_layout()
    plot_file = "throughput_plot.png"
    plt.savefig(plot_file)
    print(f"\nResults saved to {output_file}")
    print(f"Plot saved to {plot_file}")
    plt.show()

if __name__ == "__main__":
    main()







