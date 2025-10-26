#!/bin/bash
# 
# pyuhala: if you pass the param "new", the previous devnet is destroyed/cleaned
# otherwise, it just starts the devnet with the previous state
#


#!/bin/bash

# --- Conditional Cleanup ---

# Check if the first parameter ($1) is NOT "new".
# If it's anything else (or empty), perform the cleanup.
if [ "$1" != "new" ]; then
    echo "No 'new' parameter detected. Removing old devnet files..."
    rm -rf ~/.local/share/reth
    sudo rm -rf ~/.playground
else
    echo "Parameter 'new' detected. Skipping file removal."
fi

# --- Main Build and Run ---

# Rebuild the binary
go build -o builder-playground .

# Run the devnet setup (uses the locally built binary)
./builder-playground cook opstack

# ----------------------------------------------------------------------------------
# TODO: Automatically retrieve the IP address for the external-builder flag
# ----------------------------------------------------------------------------------

# In many Linux-based VM/container setups, the host machine's IP address
# is the default gateway of the network. You can capture it like this:

# HOST_IP=$(ip route show default | awk '/default/ {print $3; exit}')
# echo "Automatically detected HOST_IP: $HOST_IP"

# To use this IP with the external builder, uncomment the line below:
# ./builder-playground cook opstack --external-builder http://${HOST_IP}:4444




#rm -rf ~/.local/share/reth
#sudo rm -rf ~/.playground
#go build -o builder-playground .
#./builder-playground cook opstack --external-builder http://host.docker.internal:4444
#./builder-playground cook opstack #--external-builder http://192.168.122.100:4444
