#!/bin/bash

#
# This scripts downloads an OS image and creates a VM image from it
# We use Ubuntu 24.04 based images for all; future version will provide options to use others
#

VM_NAME="builder-vm"
CLOUD_IMG="noble-server-cloudimg-amd64.img"
SEED_IMG="seed.img"
LOGFILE=/tmp/pbs-vm-setup.txt
RAM_MB=2048
CPUS=4
SSH_PORT=2223


# Download Ubuntu cloud image if not already present
if [ ! -f "$CLOUD_IMG" ]; then
    echo "Downloading Ubuntu cloud image..."
    wget https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img
    
fi

qemu-img resize noble-server-cloudimg-amd64.img 20G

# Create cloud init config
mkdir -p cloud-init
cat > cloud-init/user-data <<EOF
#cloud-config
hostname: ${VM_NAME}
users:
  - name: ubuntu
    sudo: ALL=(ALL) NOPASSWD:ALL
    groups: sudo
    shell: /bin/bash
    plain_text_passwd: '123456'
    lock_passwd: false
ssh_pwauth: true
chpasswd:
  list: |
    ubuntu:123456
  expire: false
disable_root: false
EOF

# Create cloud-init meta-data
cat > cloud-init/meta-data <<EOF
instance-id: iid-${VM_NAME}
local-hostname: ${VM_NAME}
EOF

# Generate seed image
cloud-localds ${SEED_IMG} cloud-init/user-data cloud-init/meta-data

echo "Booting VM with QEMU"
# Boot VM with QEMU
qemu-system-x86_64 \
  -enable-kvm \
  -m ${RAM_MB} \
  -cpu host \
  -name ${VM_NAME} \
  -smp ${CPUS} \
  -drive file=${CLOUD_IMG},format=qcow2 \
  -drive file=${SEED_IMG},format=raw \
  -netdev bridge,id=net0,br=virbr0 \
  -device virtio-net-pci,netdev=net0 \
  -nographic


  # login to VM with: ssh -p 2223 ubuntu@localhost

