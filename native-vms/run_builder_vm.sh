#!/bin/bash
# Builds the builder VM and forwards port 4444 to host

set -e

VM_NAME="builder-vm"
PORT=4444
RAM_GB=8G
CPUS=16


echo "Building builder VM: $VM_NAME..."
multipass launch noble \
  --name "$VM_NAME" \
  --cpus ${CPUS} \
  --memory ${RAM_GB} \
  --disk 30G 

echo "Forwarding host port $PORT → VM port $PORT..."
# Multipass doesn't support native port forwarding, so we set up an SSH tunnel in the background
# Kill any existing tunnel
pkill -f "ssh.*multipass.*$PORT" 2>/dev/null || true

# Start background SSH tunnel
multipass ssh "$VM_NAME" -- "sudo ufw allow $PORT" 2>/dev/null || echo "ufw not active (ok)"
ssh -o StrictHostKeyChecking=no -N -L "127.0.0.1:$PORT:127.0.0.1:$PORT" "$(multipass info $VM_NAME --format json | jq -r '.info."builder-vm".ipv4[0]')" &
TUNNEL_PID=$!
echo "Builder RPC available on host: http://localhost:$PORT"
echo "Tunnel PID: $TUNNEL_PID (keep this script running or manage tunnel separately)"

# Optional: save IP for devnet config
multipass info "$VM_NAME" --format json | jq -r '.info."builder-vm".ipv4[0]' > ./builder-vm-ip.txt

echo "Builder VM created. Access via: multipass shell $VM_NAME"