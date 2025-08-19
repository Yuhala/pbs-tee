## PBS
> In this setting we have proposer-builder separation. The proposer runs in a regular VM while the builder runs in a TDX VM



## Setup
- Install virtualization requirments
```bash
sudo apt update
sudo apt install qemu-kvm libvirt-daemon-system libvirt-clients bridge-utils cloud-image-utils -y
apt install --yes qemu-utils libguestfs-tools virtinst genisoimage # from TDX script

# to allow virt-customize to have name resolution, dhclient should be available
# on the host system. that is because virt-customize will create an appliance (with supermin)
# from the host system and will collect dhclient into the appliance
apt install --yes isc-dhcp-client #&>> ${LOGFILE}
```
- Configure libvirt
```bash
sudo virsh net-start default
# verify the state is active
sudo virsh net-list --all
```

- Build and start the proposer VM
```bash
./boot_normal_vm.sh
  # login to VM with: ssh -p 2223 ubuntu@localhost
```
- To leave VM do 
```bash
sudo shutdown -h now
# leave qemu monitor
Ctrl + a
x
```

- Setup TDX server if not yet done. See [readme from Canonical](https://github.com/canonical/tdx/tree/3.3?tab=readme-ov-file#4-setup-host-os)
- Build and start the TDX builder VM
```bash
cd tdx/guest-tools/image
sudo ./create-td-image.sh -v 24.04
cd ..
./run_td
# SSH into VM. Example: ssh -p 10022 tdx@localhost 
# Default password is: 123456
```
## Running everything in a TDX VM
> Here we run all the components: builder playground + the block builder (using Kubernetes) within a TDX VM. The instructions to set this up and test are as follows. Note that the same instructions apply if you aren't in a TDX VM.

- Install a lightweight kubernetes, we use `k3s`. 
```bash
sudo /usr/local/bin/k3s-uninstall.sh
curl -sfL https://get.k3s.io | sh -
echo "alias k='sudo /usr/local/bin/k3s kubectl'" >> ~/.bashrc
source ~/.bashrc
```
Since we are running everything in TDX, there is no need to install Kata which was used (see [Claudiu's repo](https://github.com/cbarbieru/builder-playground-opstack-k8s)) to spin kubernetes pods running in TDX VMs for specific components. We have modified the kubernetes configuration files (in the `resources` subfolder) to spin regular pods without Kata.
- Spin up and run a test with.
```bash
mkdir -p /mnt/sceal/storage #TODO: spin up builder playground pods to recreate genesis files in this storage folder.
sudo cp -a storage/. /mnt/sceal/storage/
cd resources
k create namespace tdx-vm-test
k apply -f 00_opstack_rollup_boost.yaml -f 02_op-rbuilder_tdx.yaml -f testing.yaml -n tdx-vm-test
```


