#!/bin/bash

#
# Pyuhala: invoke the python scripts here
# 

# --- Configuration ---
# Array of all available Python benchmark scripts
BENCHMARKS=("bench_devnet.py" "load_latency.py" "num_txs_lat_bench.py" "client_tput.py" "client_latency.py")

# --- Functions ---

# Function to print usage instructions
usage() {
    echo "Usage: $0 <script_index>"
    echo "Available benchmarks (Index | Script Name):"
    # Use !BENCHMARKS[@] to loop through indices and print them for clarity
    for i in "${!BENCHMARKS[@]}"; do
        printf "  - %d | %s\n" "$i" "${BENCHMARKS[$i]}"
    done
    exit 1
}

# --- Main Logic ---

# Check if an argument was provided
if [ -z "$1" ]; then
    echo "Error: No script index provided."
    usage
fi

# Store the requested index
SCRIPT_INDEX="$1"

# 1. Check if the input is a positive integer
if ! [[ "$SCRIPT_INDEX" =~ ^[0-9]+$ ]]; then
    echo "Error: Input must be a non-negative integer representing the script index."
    usage
fi

# 2. Check array bounds
MAX_INDEX=$((${#BENCHMARKS[@]} - 1))
if [ "$SCRIPT_INDEX" -gt "$MAX_INDEX" ]; then
    echo "Error: Invalid script index $SCRIPT_INDEX. Must be between 0 and $MAX_INDEX."
    usage
fi

# Retrieve the script name using the valid index
SCRIPT_NAME="${BENCHMARKS[$SCRIPT_INDEX]}"

echo "Attempting to run benchmark: Index $SCRIPT_INDEX ($SCRIPT_NAME)"

python3 "$SCRIPT_NAME"


# Check the exit status of the python command
if [ $? -eq 0 ]; then
    echo "Successfully completed $SCRIPT_NAME."
else
    echo "Error: $SCRIPT_NAME failed to run or exited with an error."
fi
