# Intel confidential containers (CoCo)
- This readme helps in setting up and testing Intel confidential containers: lightweight VMs secured with TEEs like TDX or SEV-SNP
- In the below, use either minikube or microk8s for managing kubernetes clusters.

## Using minikube
- Minikube is a tool used to create and manage kubernetes containers. 
- Install minikube with: https://minikube.sigs.k8s.io/docs/start/?arch=%2Flinux%2Fx86-64%2Fstable%2Fbinary+download
- Sometimes minikube has issues reading "system" folders, so create a folder in your home and set as minikube home
```sh
mkdir -p minikube-home
export MINIKUBE_HOME=/home/<your-user>/minikube-home/
```

- Create minikube cluster for CoCo: https://github.com/kata-containers/kata-containers/blob/main/docs/install/minikube-installation-guide.md
```bash
minikube start --vm-driver docker --memory 6144 --network-plugin=cni --enable-default-cni --container-runtime=cri-o --bootstrapper=kubeadm
```
- In the above guide, the `kvm2` driver is used but it causes errors on my system so I replaced with the docker driver

- To delete all minikube clusters, do
```bash
minikube delete --all 
```

## Using microk8s
- An alternative to minikube is microk8s which can be used to creating kubernetes containers. 
- Install it as follows
```bash
sudo snap install microk8s --classic
```
- Add your user to microk8s group

```bash
sudo usermod -a -G microk8s $USER
sudo chown -f -R $USER ~/.kube
newgrp microk8s
```
- Launch microk8s with:
```bash
microk8s status --wait-ready
```
- Create and test a simple microk8s helloworld pod.
```bash 
microk8s kubectl run hello --image=busybox --command -- sh -c "echo Hello, MicroK8s! && sleep 3600"
microk8s kubectl get pods
microk8s kubectl logs hello
```
- Create an alias to facilitate your work
```bash
echo "alias mkubectl='microk8s kubectl'" >> ~/.bashrc
source ~/.bashrc
```
- NB: we can also enter the information to create the pod in a yaml file, as will be seen subsequently.



## Installing confidential containers 
- See guide here: https://cc-enabling.trustedservices.intel.com/intel-confidential-containers-guide/02/infrastructure_setup/
- At step 6, do this `kubectl get pods -n confidential-containers-system --watch` and wait until all the pods have a status of `Running`.
- Verify the CoCo installation by printing the runtime classes with:
```bash
kubectl get runtimeclass
```de
- The output should be similar to below
```bash
NAME                 HANDLER              AGE
kata                 kata-qemu            8d
kata-clh             kata-clh             8d
kata-qemu            kata-qemu            8d
kata-qemu-coco-dev   kata-qemu-coco-dev   8d
kata-qemu-sev        kata-qemu-sev        8d
kata-qemu-snp        kata-qemu-snp        8d
kata-qemu-tdx        kata-qemu-tdx        8d
```
- See the following readme to understand each runtime class: https://github.com/confidential-containers/confidential-containers/blob/main/quickstart.md#verify-installation

### CoCo with microk8s
- The above guide works Ok for minikube. For microk8s, see Claudiu's readme: https://github.com/cbarbieru/builder-playground-opstack-k8s/tree/main
- Some useful commands
```bash
mkubectl get pods -n confidential-containers-system -o wide # or kubectl depending on your config

```

## Creating Pods
- Start by creating a very simple Pod by defining its architecture in a YAML file `hellopod.yaml` as such:

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: helloworld
spec:
  containers:
  - name: hello
    image: busybox
    command: ["sh", "-c", "echo Hello, World! && sleep 3600"]
```
- Build the pod with
```bash
kubectl apply -f hellopod.yaml
```
- Check all pods with 
```bash
kubectl get pods
kubectl describe pod helloworld
```
- After the pod is successfully created, you should see its status as `RUNNING
- To see results from the pod, do.
```bash
kubectl logs helloworld
```
- To create a pod secured with confidential computing, you need to provide a CoCo runtime class. Example: `kata-qemu-tdx`. So we can redo the above helloworld pod but this time with TDX security.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: helloworld
  annotations:
    io.containerd.cri.runtime-handler: kata-qemu-tdx
spec:
  runtimeClassName: kata-qemu-tdx
  containers:
  - name: hello
    image: busybox
    command: ["sh", "-c", "echo Hello, World from TDX CoCo! && sleep 3600"]
```
- Pods with the `kata-` runtime classes seem to take longer to create. To watch see the status in "real time" do 
```bash
kubectl get pods --watch
```
- You can stop with `Ctrl+C` once you see the required pod in "Running" state.
- Delete pod with
```bash
kubectl delete pod <name>
```
- Delete all pods
```bash
kubectl delete pods --all
```
- Restarting microk8s containerd
```bash
sudo systemctl restart snap.microk8s.daemon-containerd.service
```

## Temp testing minikube with kata
```bash
minikube start --vm-driver=docker --container-runtime=containerd --memory 6144
minikube start --vm-driver=docker --memory 6144 --container-runtime=containerd --bootstrapper=kubeadm
```
```bash
kubectl get nodes
```
- Label node
```bash
kubectl label node "minikube" "node.kubernetes.io/worker="
```
- Check with this
```bash
minikube profile list
```
- Positive result should look like: 
```bash
|----------|-----------|------------|--------------|------|---------|--------|-------|----------------|--------------------|
| Profile  | VM Driver |  Runtime   |      IP      | Port | Version | Status | Nodes | Active Profile | Active Kubecontext |
|----------|-----------|------------|--------------|------|---------|--------|-------|----------------|--------------------|
| minikube | docker    | containerd | 192.168.49.2 | 8443 | v1.33.1 | OK     |     1 | *              | *                  |
|----------|-----------|------------|--------------|------|---------|--------|-------|----------------|--------------------|
```
- Continue from step 1 here: https://cc-enabling.trustedservices.intel.com/intel-confidential-containers-guide/02/infrastructure_setup/
- The following repo is also worth looking at: https://github.com/kata-containers/kata-containers/blob/main/docs/install/minikube-installation-guide.md#check-minikube-is-running
- Update kata-qemu-tdx config file to point to correct qemu image
```bash
sudo vim /opt/kata/share/defaults/kata-containers/configuration-qemu-tdx.toml 
# change hypervisor.qemu path to "/opt/kata/bin/qemu-system-x86_64-tdx-experimental
sudo systemctl restart containerd
# view logs with
sudo journalctl -xeu containerd
```

```bash
sudo /opt/kata/bin/kata-runtime kata-check # should say system is capable of running kata containers
sudo /opt/kata/bin/kata-runtime kata-env
sudo /opt/kata/bin/kata-runtime exec <id> # get id of pod from ps -ef | grep qemu
```
sudo /opt/kata/bin/kata-runtime exec 5072b77e6ea7052a67d8ff7dcab3eab257c670ed0be82d3d1b826ca639020c67
- To delete all kata runtime classes
```bash
kubectl get runtimeclass -o name | grep kata | xargs -r kubectl delete
```

## Debugging
```bash 
ps aux | grep /opt/kata/bin/qemu-system-x86_64
```

## Documentation
- [Confidential containers explained](https://confidentialcontainers.org/blog/2024/12/03/confidential-containers-without-confidential-hardware/)