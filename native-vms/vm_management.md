## Managing VMs created with Multipass

1. Connecting to the VM
```bash
sudo multipass authenticate #enter passphrase
sudo multipass shell <vm-name>
```
2. Listing VMs created with multipass
```bash
sudo multipass list
```
3. Stopping a VM
```bash
sudo multipass stop <vm-name>
#or 
sudo multipass stop --all # to stop all VMs
```
4. Destroying VMs created with multipass
```bash
sudo multipass delete <vm-name>
sudo multipass purge
```

5. Copying files to and from VMs
```bash
# copy file output.log from builder-vm to host
multipass transfer builder-vm:/home/ubuntu/output.log .
# copy file from host to VM
multipass transfer myfile.txt builder-vm:/home/ubuntu/
```

6. File mounting
```bash
# mount folder on host inside VM
multipass mount /path/on/host <vm-name>:/path/in/vm
# unmount
multipass unmount <vm-name>:/path/in/vm
```
