#!/bin/bash
# 
# PYuhala: this script runs tps-meter bench: https://github.com/deblanco/tps-meter
# copy this script to the tps-meter folder
#

set -euo pipefail

RPC_ENDPOINT="${RPC_ENDPOINT:-http://localhost:8545}"
PRIVATE_KEY="${PRIVATE_KEY:-0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80}"
OPTIONAL_BATCH_SIZE="${OPTIONAL_BATCH_SIZE:-150}" # 150 is default value

echo "--- Running TPS meter benchmark ---"

if ! command -v yarn >/dev/null 2>&1; then
    echo "yarn not found in PATH. Install it and retry." >&2
    exit 1
fi

# forward args to the yarn start script using --
yarn start -- -r "${RPC_ENDPOINT}" -pk "${PRIVATE_KEY}" -c "${OPTIONAL_BATCH_SIZE}"
# ...existing code...