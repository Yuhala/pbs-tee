#!/bin/bash
# Creates the devnet VM and forwards port 8547 to host

# Prerequisites
# sudo snap install multipass
# sudo apt install jq -y

#
# Connect to VM with
# Create VM with: sudo ./run_devnet_vm.sh
# sudo multipass authenticate --> enter passphrase
# sudo multipass shell devnet-vm
# sudo multipass list
#


set -e

VM_NAME="devnet-vm"
PORT=8547
RAM_GB=8G
CPUS=16


echo "Creating devnet VM: $VM_NAME..."
multipass launch noble \
  --name "$VM_NAME" \
  --cpus ${CPUS} \
  --memory ${RAM_GB} \
  --disk 30G \
  --network mpqemubr0 #verify which multipass bridge to use with multipass networks


echo "Forwarding host port $PORT → VM port $PORT..."
pkill -f "ssh.*multipass.*$PORT" 2>/dev/null || true

multipass ssh "$VM_NAME" -- "sudo ufw allow $PORT" 2>/dev/null || echo "ufw not active (ok)"
ssh -o StrictHostKeyChecking=no -N -L "127.0.0.1:$PORT:127.0.0.1:$PORT" "$(multipass info $VM_NAME --format json | jq -r '.info."devnet-vm".ipv4[0]')" &
TUNNEL_PID=$!
echo "Devnet RPC available on host: http://localhost:$PORT"
echo "Tunnel PID: $TUNNEL_PID"

echo "Devnet VM created. Access via: multipass shell $VM_NAME"