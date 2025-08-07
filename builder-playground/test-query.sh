#!/bin/bash

#
# Peterson: some curl commands to query the testnet from builder-playground
#

# Helper to print section headers
function print_section() {
  echo -e "\n==============================="
  echo -e "$1"
  echo -e "===============================\n"
}

# Helper to perform curl and print result
function do_curl() {
  local description="$1"
  local cmd="$2"

  print_section "$description"
  echo "Running: $cmd"
  echo

  # Execute command and capture output
  output=$(eval "$cmd" 2>&1)
  status=$?

  echo "$output"
  echo

  if [ $status -eq 0 ]; then
    echo "[SUCCESS] $description"
  else
    echo "[FAILED] $description"
  fi
}

# === 1. L1 Execution Layer ===
do_curl "L1 Execution Layer - Get client version" \
  "curl -s -X POST http://localhost:8545 -H 'Content-Type: application/json' -d '{\"jsonrpc\":\"2.0\",\"method\":\"web3_clientVersion\",\"params\":[],\"id\":1}'"

# === 2. L2 Execution Layer ===
do_curl "L2 Execution Layer - Check syncing" \
  "curl -s -X POST http://localhost:8547 -H 'Content-Type: application/json' -d '{\"jsonrpc\":\"2.0\",\"method\":\"eth_syncing\",\"params\":[],\"id\":1}'"

# === 3. L2 Rollup Node ===
do_curl "L2 Rollup Node - Check health" \
  "curl -s http://localhost:8549/healthz"

# === 4. Beacon Chain Head ===
do_curl "Beacon Node - Chain head" \
  "curl -s http://localhost:3500/eth/v1/beacon/chain/head"

# === 5. Prometheus metrics ===
do_curl "L1 Execution Layer - Prometheus metrics" \
  "curl -s http://localhost:9090/metrics | head -n 20"

# === 6. Rollup-Boost Authenticated RPC ===
if [ -f "./jwt.hex" ]; then
  TOKEN=$(cat ./jwt.hex)
  do_curl "Rollup Boost - engine_exchangeCapabilities" \
    "curl -s -X POST http://localhost:8553 -H 'Authorization: Bearer $TOKEN' -H 'Content-Type: application/json' -d '{\"jsonrpc\":\"2.0\",\"method\":\"engine_exchangeCapabilities\",\"params\":[],\"id\":1}'"
else
  echo "[⚠️ SKIPPED] Rollup Boost - jwt.hex not found in current directory."
fi
