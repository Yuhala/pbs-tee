#!/usr/bin/env bash
set +e  # Don't stop on errors

# install packages
#sudo apt install sysstat ifstat jq
#curl -L https://foundry.paradigm.xyz | bash
#source ~/.bashrc
foundryup 

# ===== CONFIGURATION =====
RPC_URL="http://localhost:8545" #http://op-geth:8545
PRIVATE_KEY="0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6" # from docker-compose file used to build devnet
TO_ADDRESS="0x0000000000000000000000000000000000000001"
TX_COUNT=1
#TX_VALUE="0.001ether" # using fractional ether may not work, convert to wei
TX_VALUE="100000000000000000"
REPORT_DIR="./benchmark_reports"
TIMESTAMP=$(date +"%Y%m%d_%H%M%S")
REPORT_FILE="$REPORT_DIR/report_$TIMESTAMP.txt"

mkdir -p "$REPORT_DIR"

log() {
    echo -e "\n[INFO] $1"
    echo -e "\n===== $1 =====" >> "$REPORT_FILE"
}

log "Starting Benchmark Run ($TIMESTAMP)"
echo "RPC URL: $RPC_URL" >> "$REPORT_FILE"

# ===== 1. Send Transactions =====
log "Sending $TX_COUNT test transactions using Foundry cast"
for i in $(seq 1 $TX_COUNT); do
    OUTPUT=$(cast send "$TO_ADDRESS" --value "$TX_VALUE" --private-key "$PRIVATE_KEY" --rpc-url "$RPC_URL" 2>&1)
    echo "$OUTPUT" >> "$REPORT_FILE"
done

# ===== 2. Blockchain Metrics =====
log "Querying latest block data"
LATEST_BLOCK=$(cast block latest --rpc-url "$RPC_URL" --json)
echo "$LATEST_BLOCK" >> "$REPORT_FILE"

log "Calculating average block time over last 5 blocks"
BLOCK_TIMES=()
for i in $(seq 0 4); do
    TS=$(cast block latest-$i --rpc-url "$RPC_URL" --json | jq -r '.timestamp')
    BLOCK_TIMES+=($TS)
done
for i in $(seq 0 3); do
    DELTA=$((BLOCK_TIMES[i] - BLOCK_TIMES[i+1]))
    echo "Block $(($i)) → $(($i+1)): $DELTA sec" >> "$REPORT_FILE"
done



# ===== 5. Summary =====
log "Benchmark run completed"
echo "Results saved in $REPORT_FILE"

cast block latest --rpc-url http://localhost:8545

cast send --rpc-url http://localhost:8545 \
--private-key 0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6 \
--value 10000 0x00d7b6990105719101dAbEb77144F2A3385C8033 \
--gas-price 1000000000 -v
