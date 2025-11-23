
#!/bin/bash
set -euo pipefail


RATES=(100 200 300 400 500 600 700 800 900 1000)

#RATES=(1024 2048 4096 8192 16384)
#
# types: eth_getBlockByNumber, eth_call, eth_getBalance, eth_getCode, eth_getTransactionByHash, flood eth_getTransactionCount
TYPE=eth_call


PRIVATE_KEY="${PRIVATE_KEY:-0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80}"


# RPC endpoint of your node
RPC_ENDPOINT="${RPC_ENDPOINT:-http://localhost:8545}"

#RPC_ENDPOINT="http://localhost:8545"

echo "--- Running Flood benchmark ---"

# Run eth_getBlockByNumber against a single node
flood $TYPE nopbs-native=$RPC_ENDPOINT --rates "${RATES[@]}" --duration 60 --output=./bench-output

