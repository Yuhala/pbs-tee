#!/bin/bash

#
# This scripts downloads an OS image and creates a VM image from it
# We use Ubuntu 24.04 based images for all; future version will provide options to use others
#

VM_NAME="builder-vm"
CLOUD_IMG="noble-server-cloudimg-amd64.img"
SEED_IMG="seed.img"
LOGFILE=/tmp/pbs-vm-setup.txt
VM_MEMORY=2048

# Install requirments
sudo apt update
sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils cloud-image-utils -y
apt install --yes qemu-utils libguestfs-tools virtinst genisoimage # from TDX script

# to allow virt-customize to have name resolution, dhclient should be available
# on the host system. that is because virt-customize will create an appliance (with supermin)
# from the host system and will collect dhclient into the appliance
apt install --yes isc-dhcp-client #&>> ${LOGFILE}

# Download Ubuntu cloud image if not already present
if [ ! -f "$CLOUD_IMG" ]; then
    echo "Downloading Ubuntu cloud image..."
    wget https://cloud-images.ubuntu.com/noble/current/noble-server-cloudimg-amd64.img
    
fi



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

# Boot VM with QEMU
qemu-system-x86_64 \
  -enable-kvm \
  -m ${VM_MEMORY} \
  -cpu host \
  -smp 2 \
  -drive file=${CLOUD_IMG},format=qcow2 \
  -drive file=${SEED_IMG},format=raw \
  -netdev user,id=net0,hostfwd=tcp::2222-:22 \
  -device virtio-net-pci,netdev=net0 \
  -nographic


  # login to VM with: ssh -p 2222 ubuntu@localhost
