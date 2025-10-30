#!/bin/bash
#!/bin/bash

# Script to establish SSH port forwarding to a Multipass VM

# --- Configuration ---
SSH_USER="ubuntu"
# Port descriptions
# builder http: 2222
# builder metrics: 9011

#PORT_FORWARDS="-L 8547:127.0.0.1:8547 -L 8556:127.0.0.1:8556 -L 6061:127.0.0.1:6061 -L 9090:127.0.0.1:9090 -L 7300:127.0.0.1:7300"
PORT_FORWARDS="-L 2222:127.0.0.1:2222 -L 9011:127.0.0.1:9011"
# ---------------------

# Check if a VM name was provided
if [ -z "$1" ]; then
    echo "Usage: $0 <vm-name>"
    echo "Example: $0 devnet-vm"
    exit 1
fi

VM_NAME=$1

echo "--- Port Forwarding Setup ---"
echo "VM Name: $VM_NAME"
echo "Ports: 2222, 9011 (forwarded to localhost on your machine)"
echo "-----------------------------"

# 1. Get the VM's IPv4 address using multipass info
# The command is: multipass info <vm-name> | grep IPv4 | awk '{print $2}'
VM_IP=$(multipass info "$VM_NAME" 2>/dev/null | grep IPv4 | awk '{print $2}')

# Check if the IP was found
if [ -z "$VM_IP" ]; then
    echo "ERROR: Could not get the IP address for '$VM_NAME'."
    echo "       Please ensure the VM name is correct and the VM is running (multipass list)."
    exit 1
fi

echo "VM IP Address: $VM_IP"
echo ""
echo "Establishing SSH tunnel. Press Ctrl+C to disconnect and close the tunnel."
echo "------------------------------------------------------------------------"

# 2. Execute the SSH command with all port forwards
# -N: Do not execute a remote command (useful for just forwarding ports).
# -T: Disable pseudo-terminal allocation.
# -L: The port forwarding rules.
ssh -N -T $PORT_FORWARDS "$SSH_USER@$VM_IP"

# A cleanup message once the SSH command is exited (e.g., by Ctrl+C)
echo ""
echo "SSH tunnel for '$VM_NAME' has been closed."