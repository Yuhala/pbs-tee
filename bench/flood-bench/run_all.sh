
#!/bin/bash
#set -euo pipefail

#
# Benchmark descriptions: all are read-only RPC calls which do not modify state nor consume gas
# 1. eth_call : queries data from smart contracts
# 2. eth_getBalance : returns ETH balance at a specific address and block
# 3. eth_getBlockByNumber: fetches block by number
# 4. eth_getCode: returns smart contract bytecode
# 5. eth_getStorageAt: reads a single storage slot from a contract
# 6. eth_getTransactionByHash: returns Tx object for a given Tx hash
# 7. eth_getTransactionCount: returns num. of Txs sent by an address
# 8. eth_getTransactionReceipt: returns receipt for a mined Tx

PRIVATE_KEY="${PRIVATE_KEY:-0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80}"


# Array of all RPC methods 
TYPES=(
  eth_call
  eth_getBalance
  eth_getBlockByNumber
  eth_getCode
  eth_getStorageAt
  eth_getTransactionByHash
  eth_getTransactionCount
  eth_getTransactionReceipt
)

# Rates 
RATES=(100 200 300 400 500 600 700 800 900 1000)

RPC_ENDPOINT="${RPC_ENDPOINT:-http://localhost:8545}"

echo "--- Running Flood benchmark for all RPC types ---"

for TYPE in "${TYPES[@]}"; do
    echo "=> Benchmarking $TYPE"

    OUTPUT_DIR="./bench-output/$TYPE"
    mkdir -p "$OUTPUT_DIR"

    flood "$TYPE" \
        nopbs-tee="$RPC_ENDPOINT" \
        --rates "${RATES[@]}" \
        --duration 60 \
        --output="$OUTPUT_DIR"
done

