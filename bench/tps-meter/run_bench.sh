#!/bin/bash
# 
# PYuhala: this script runs tps-meter bench: https://github.com/deblanco/tps-meter
# copy this script to the tps-meter folder
#

RPC_ENDPOINT="http://localhost:8545"
PRIVATE_KEY="0xac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80"
OPTIONAL_BATCH_SIZE=150 #150 is default value

echo "--- Running TPS meter benchmark ---"

yarn start -r $RPC_ENDPOINT -pk $PRIVATE_KEY -c $OPTIONAL_BATCH_SIZE