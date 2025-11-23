#!/bin/bash

# --- Configuration ---

# The root directory where all benchmark results will be saved.
export TEST_DATA_DIR=./all_bench

# The primary RPC endpoint URL.
export NODE1=http://localhost:8545

# Label for the node's results in the report.
NODE_NAME=nopbs-native

# Create the output directory if it doesn't exist
mkdir -p $TEST_DATA_DIR


# --- Run Benchmarks ---

echo "Starting RPC Benchmarking..."

# eth_call (Simulation of transaction before broadcast)
flood eth_call \
    $NODE_NAME=$NODE1 \    
    --output $TEST_DATA_DIR/eth_call \
    -r 1024 2048 4096 8192 16384

# eth_getBalance (Account balance query)
flood eth_getBalance \
    $NODE_NAME=$NODE1 \    
    --output $TEST_DATA_DIR/eth_getBalance \
    -d 30 \
    -r 1024 2048 4096 8192 16384

# eth_getBlockByNumber (Block header/body query)
flood eth_getBlockByNumber \
    $NODE_NAME=$NODE1 \    
    --output $TEST_DATA_DIR/eth_getBlockByNumber \
    -r 1024 2048 4096 8192 16384

# eth_getCode (Contract bytecode query)
flood eth_getCode \
    $NODE_NAME=$NODE1 \    
    --output $TEST_DATA_DIR/eth_getCode \
    -r 1024 2048 4096 8192 16384

# eth_getLogs (Event log query)
flood eth_getLogs \
    $NODE_NAME=$NODE1 \    
    --output $TEST_DATA_DIR/eth_getLogs \
    -r 64 128 256 512 1024

# eth_getStorageAt (Storage slot query)
flood eth_getStorageAt \
    $NODE_NAME=$NODE1 \    
    --output $TEST_DATA_DIR/eth_getStorageAt \
    -r 1024 2048 4096 8192 16384

# eth_getTransactionByHash (Transaction detail query)
flood eth_getTransactionByHash \
    $NODE_NAME=$NODE1 \    
    --output $TEST_DATA_DIR/eth_getTransactionByHash \
    -r 1024 2048 4096 8192 16384

# eth_getTransactionCount (Account nonce query)
flood eth_getTransactionCount \
    $NODE_NAME=$NODE1 \   
    --output $TEST_DATA_DIR/eth_getTransactionCount \
    -r 2048 4096 8192 16384 32768

# eth_getTransactionReceipt (Transaction receipt query)
flood eth_getTransactionReceipt \
    $NODE_NAME=$NODE1 \   
    --output $TEST_DATA_DIR/eth_getTransactionReceipt \
    -r 1024 2048 4096 8192 16384


# --- Generate Report (Directory paths corrected here) ---

echo "Generating report in $TEST_DATA_DIR..."

cd $TEST_DATA_DIR

flood report \
    eth_call \
    eth_getBalance \
    eth_getBlockByNumber \
    eth_getCode \
    eth_getLogs \
    eth_getStorageAt \
    eth_getTransactionByHash \
    eth_getTransactionCount \
    eth_getTransactionReceipt

echo "Report generation complete."
