#!/usr/bin/env python3


import json
import random
import csv
import matplotlib.pyplot as plt
from web3 import Web3
from datetime import datetime
import time
from web3.middleware import ExtraDataToPOAMiddleware

import json
from hexbytes import HexBytes

# ----------------------------
# CONFIGURATION
# ----------------------------
OPTIMISM_URL = "https://mainnet.optimism.io"
SEPOLIA_URL = "https://sepolia.optimism.io"

RPC_URL = SEPOLIA_URL
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

# Inject POA middleware for Optimism
w3.middleware_onion.inject(ExtraDataToPOAMiddleware, layer=0)

assert w3.is_connected(), "Cannot connect to Optimism RPC!"
print(f"Connected to L2 chain: latest block {w3.eth.block_number}")

# ----------------------------
# FETCH BLOCKS, TRANSACTIONS, AND RECEIPTS
# ----------------------------
trace_blocks = []
print(f"Fetching blocks {START_BLOCK} to {END_BLOCK}...")

for blk_num in range(START_BLOCK, END_BLOCK + 1):
    try:
        block = w3.eth.get_block(blk_num, full_transactions=True)
    except Exception as e:
        print(f"[!] Failed to fetch block {blk_num}: {e}")
        continue

    block_trace = {
        "number": block.number,
        "hash": block.hash.hex(),
        "parentHash": block.parentHash.hex(),
        "miner": block.get("miner"),
        "baseFeePerGas": block.get("baseFeePerGas"),
        "gasLimit": block.gasLimit,
        "gasUsed": block.gasUsed,
        "size": block.get("size"),
        "timestamp": block.timestamp,
        "transactions": []
    }

    for tx in block.transactions:
        try:
            receipt = w3.eth.get_transaction_receipt(tx["hash"])
        except Exception as e:
            print(f"  [!] Skipping TX {tx['hash'].hex()} (receipt error: {e})")
            continue

        tx_record = {
            "hash": tx["hash"].hex(),
            "from": tx["from"],
            "to": tx["to"],
            "value": int(tx["value"]),
            "gas": tx["gas"],
            "gasPrice": int(tx.get("gasPrice", 0)),
            "maxFeePerGas": int(tx.get("maxFeePerGas", 0)),
            "maxPriorityFeePerGas": int(tx.get("maxPriorityFeePerGas", 0)),
            "nonce": tx["nonce"],
            "input": tx["input"],
            "type": tx.get("type", "0x0"),
            # receipt info
            "status": receipt.status,
            "gasUsed": receipt.gasUsed,
            "contractAddress": receipt.contractAddress,
            "cumulativeGasUsed": receipt.cumulativeGasUsed,
            "logsBloom": receipt.logsBloom.hex(),
            "logs": [
                {
                    "address": log["address"],
                    "topics": [t.hex() for t in log["topics"]],
                    "data": log["data"]
                }
                for log in receipt["logs"]
            ]
        }

        block_trace["transactions"].append(tx_record)

    trace_blocks.append(block_trace)
    print(f"Fetched block {blk_num} ({len(block.transactions)} txs)")
    print(f"  ↳ hash={block.hash.hex()}, time={datetime.utcfromtimestamp(block.timestamp)}")

    # Sleep to avoid hitting rate limits
    time.sleep(0.3)

# ----------------------------
# Helper: safely convert HexBytes to hex
# ----------------------------
def make_json_safe(obj):
    """Recursively convert HexBytes and bytes to hex strings for JSON serialization."""
    if isinstance(obj, HexBytes):
        return obj.hex()
    elif isinstance(obj, bytes):
        return obj.hex()
    elif isinstance(obj, dict):
        return {k: make_json_safe(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [make_json_safe(i) for i in obj]
    else:
        return obj

# ----------------------------
# SAVE TRACE TO JSON
# ----------------------------
with open(OUTPUT_TRACE_FILE, "w") as f:
    json.dump(make_json_safe(trace_blocks), f, indent=2)

print(f"Saved block traces to {OUTPUT_TRACE_FILE}")

