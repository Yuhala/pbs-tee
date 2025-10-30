#!/bin/bash

#HOST_IP=127.0.0.1 
HOST_IP=10.169.79.236

git clone https://github.com/flashbots/op-rbuilder.git
cd op-rbuilder
# rm old reth if present
rm -rf ~/.local/share/reth
# run op-rbuilder
cargo run -p op-rbuilder --bin op-rbuilder -- node \
    --chain $HOME/l2-genesis.json \
    --http --http.port 2222 --http.addr 0.0.0.0 \
    --authrpc.addr 0.0.0.0 --authrpc.port 4444 --authrpc.jwtsecret $HOME/jwtsecret \
    --port 30333 --disable-discovery \
    --metrics 0.0.0.0:9011 \
    --rollup.builder-secret-key ac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80 \
    --trusted-peers enode://79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8@${HOST_IP}:30304