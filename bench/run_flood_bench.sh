
#!/bin/bash
set -euo pipefail


PRIVATE_KEY="${PRIVATE_KEY:-0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80}"


# RPC endpoint of your node
RPC_ENDPOINT="${RPC_ENDPOINT:-http://localhost:8545}"

#RPC_ENDPOINT="http://localhost:8545"

echo "--- Running Flood benchmark ---"

# Run eth_getBlockByNumber against a single node
flood eth_getBlockByNumber nopbs-native=$RPC_ENDPOINT --rates 2 4 8 16 32 64 128 256 512 1024 --duration 60 --output=./bench/output

