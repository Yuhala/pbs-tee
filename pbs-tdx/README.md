## PBS
> In this setting we have proposer-builder separation. The proposer runs in a regular VM while the builder runs in a TDX VM



## Setup
- Build and start the proposer VM
```bash
./boot_normal_vm.sh
```

- Setup TDX server if not yet done. See [readme from Canonical](https://github.com/canonical/tdx/tree/3.3?tab=readme-ov-file#4-setup-host-os)
- Build and start the TDX builder VM
```bash
cd tdx/guest-tools/image
sudo ./create-td-image.sh -v 24.04
cd ..
./run_td
```
