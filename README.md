## Context
Testing proposer-builder-separation (PBS) with VM-based builder. [Builder Playground](https://github.com/flashbots/builder-playground) is used to spin a local L1 + L2 environment based on Docker: EL/CL clients, validators, MEV-Boost relay, sequencer components, etc. In addition, it integrates Rollup-Boost which enhances the L2 OP-Stack by enabling external block building or TEE-enabled ordering. Rollup-Boost intercepts Engine API calls (`engine_FCU`, `engine_getPayLoad`) to route them to both the proposer node and a separate builder node, validating the builder's block before consensus. 

[Flashbot's op-rbuilder](https://github.com/flashbots/op-rbuilder.git) is used as the external block builder. This Readme provides setups where all these components run on the same host (could also be a VM) or where the builder runs in a separate (TEE-enabled) VM.

## Part I: L1 + L2 stack and builder on the same host

### Setup builder playgroud
- Install Cargo
```bash
sudo apt update
sudo apt install curl build-essential pkg-config libssl-dev -y
curl https://sh.rustup.rs -sSf | sh
source $HOME/.cargo/env # load cargo into your shell
cargo --version # check version to confirm installation
```
- Install Go
```bash
sudo apt update
sudo apt install golang-go -y
go version # check go version
```

- Install Docker using convenience script
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh ./get-docker.sh --dry-run # shows which instructions are run by the script
sudo sh get-docker.sh
sudo usermod -aG docker $USER # logout and back
```


- Now spin up the L1 + L2 (sequencer + proposer) stack using builder-playground, specifying the RPC endpoint throughwhich the builder will be reached. A rollup-boost instance is (automaticall) lauched by the `cook` command. When sequencer receives `engine_FCU`, Rollup‑Boost mirrors it to the builder; upon `engine_getPayload`, collects the builder block, validates it, and feeds it back to the sequencer if valid. 

```bash
git clone https://github.com/Yuhala/pbs-tee.git && cd pbs-tee
cd builder-playground
go build -o builder-playground . # build builder-playground or use "go run main.go" in the next command
./builder-playground cook opstack --external-builder http://host:8555
```
- Example output in the terminal
```bash
========= Services started =========
- el (authrpc: 8551/8551, http: 8545/8545, metrics: 9090/9090, rpc: 30303/30303, ws: 8546/8546)
- beacon (http: 3500/3500, p2p: 9000/9000/udp, p2p: 9000/9001, quic-p2p: 9100/9100)
- validator ()
- op-geth (authrpc: 8551/8552, http: 8545/8547, metrics: 6061/6061, rpc: 30303/30304, ws: 8546/8548)
- rollup-boost (authrpc: 8551/8553)
- op-node (http: 8549/8549, metrics: 7300/7300, p2p: 9003/9003, p2p: 9003/9004/udp)
- op-batcher ()
```
- Each line in the above output represents a component of the test network, along with the ports it's using for different protocols (HTTP, WebSocket, Auth-RPC, P2P, Metrics, etc.). `el` is the L1 execution engine (like Geth), `beacon + validator` represent the L1 consensus layer, `op-geth` is the L2 execution engine, `op-node` is the rollup node that bridges L1 and L2 state. `rollup-boost` simulates builder separation in L2 and `op-batcher` sends L2 transactions and data to L1 for inclusion.
- See [these notes](./builder-playground/opstack_spinup_output.md) for a more extensive explanation of the output.
- The file `~/.playground/devnet` contains a file `genesis.json` containing information on the initial state of the blockchain network. It also contains information on prefunded accounts which could be used to test blockchain transactions. For example:
``` bash
"14dc79964da2c08b23698b3d3cc7ca32193d9955": {
			"balance": "0x10000000000000000000000",
			"nonce": "0x1"
		},
"15d34aaf54267db7d7c367839aaf71a00a2c6a65": {
			"balance": "0x10000000000000000000000",
			"nonce": "0x1"
		},
```
- The private key used by the batcher to sign transactions in L2 can be found in the file `~/.playground/devnet/docker-compose.yaml`

- Query the testnet with some curl instructions by running the `test-query.sh` script.
```bash
./test-query.sh
```

## Integrating an external builder
- Rollup-Boost serves as a relay between your L2 stack and an external block builder, [Flashbot's op-rbuilder](https://github.com/flashbots/op-rbuilder.git) in this case.
- The `builder-playground cook opstack ... ` command from builder-playground spins up an OP stack including a rollup-boost instance as one of its containers. The `--external-builder` flag you pass to `cook opstack` tells the embedded Rollup-Boost instance:
>When building blocks, call this builder at URL X instead of building locally.
```scss
builder-playground cook opstack ...
     ├── op-geth (L1 execution)
     ├── op-node (L2 node)
     ├── rollup-boost  ← starts automatically here
     ├── relays
     ├── ...
```
However, if you are running Rollup-Boost separately, you will need to point rollup-boost to the `Engine API` of the L2 execution client (`op-geth`). From the builder playground logs, this should be `http://localhost:8551`. See [Rollup-Boost documentation here](https://github.com/flashbots/rollup-boost).

- Clean up any previous builder-playground state from previous runs and re-run builder-playground.
```bash
rm -rf ~/.local/share/reth
sudo rm -rf ~/.playground
./builder-playground cook opstack --external-builder http://host.docker.internal:4444
```
- You can do all of the above by launching the script [start-builder-playground](./builder-playground/start-builder-playground.sh).
- Setup and run `op-rbuilder`:
```bash
git clone https://github.com/flashbots/op-rbuilder.git
cd op-rbuilder
#cargo run --bin op-rbuilder -- node --builder.playground # assuming you used --external-builder http://host.docker.internal:4444 when building op-stack
cargo run -p op-rbuilder --bin op-rbuilder -- node \
    --chain $HOME/.playground/devnet/l2-genesis.json \
    --http --http.port 2222 \
    --authrpc.addr 0.0.0.0 --authrpc.port 4444 --authrpc.jwtsecret $HOME/.playground/devnet/jwtsecret \
    --port 30333 --disable-discovery \
    --metrics 127.0.0.1:9011 \
    --rollup.builder-secret-key ac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80 \
    --trusted-peers enode://79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8@127.0.0.1:30304
```
- Logs from op-rbuilder similar to the following shows the builder is actively receiving blocks from the consensus engine in the L1 + L2 stack.
```bash
...
2025-08-13T08:30:33.959995Z  INFO Received block from consensus engine number=859 hash=0xa5ae15d7e4268686874607f6ee80d6511466e0db91a2e65695dd584460eb99ca
2025-08-13T08:30:35.960807Z  INFO Received block from consensus engine number=860 hash=0xa20f29c307cfb1f9c6bc3aa7d36945a8e09c37a4201a0d1b5defd37562865bab
```

## Kubernetes based setup
- To setup and run all components using Kubernetes (can be done on a regular host or TDX VM), see [this Readme](pbs-tdx/README.md). Note that this is a little different from Claudiu's setup in that we don't use Kata to spin up pods running in a VM. However, we adapt Claudiu's kubernetes configurations to simply run regular pods.

## Part II: L1 + L2 stack and builder on separate machines or VMs
Here we will spin up the L1 + L2 in VMs (TDX enabled or not). The `pbs-tee/native-vms` folder contains scripts used to build and launch such VMs using the `multipass` tool.
- To build a VM (e.g., the `devnet-vm`), run the script `run_devnet_vm.sh`. This will build a VM called `devnet-vm` where you can run the monolythic sequencer. Another script called `run_builder_vm.sh` can be run to build a VM which will run the L2 builder component `op-rbuilder`. We note that these scripts do not (yet) run these componenents and so can be easily modified to run just a regular VM. Nevertheless, their names simply specify what they are meant to run.
- To launch the devnet VM using multipass, do:
```bash
multipass shell devnet-vm
# do multipass list to list all multipass VM information
```
- Once inside a VM, pull this repo and launch the `setup.sh` script to install some useful packages.
```bash
git clone https://github.com/Yuhala/pbs-tee.git && cd pbs-tee
cd native-vms
./setup.sh
```
### Devnet VM 
The `devnet-vm` builds and runs the main local devnet. To launch this devnet, do:
```bash
cd pbs-tee/builder-playground
./start_devnet new # to run a new devnet
./start_devnet # run existing devnet using existing state files in ~/.playground
```
Once the devnet is running (in the VM), you should have a similar output like below:
```bash
========= Services started =========
- el (authrpc: 8551/8551, http: 8545/8545, metrics: 9090/9090, rpc: 30303/30303, ws: 8546/8546)
- beacon (http: 3500/3500, p2p: 9000/9000/udp, p2p: 9000/9001, quic-p2p: 9100/9100)
- validator ()
- op-geth (authrpc: 8551/8552, http: 8545/8547, metrics: 6061/6061, rpc: 30303/30304, ws: 8546/8548)
- op-node (http: 8549/8549, metrics: 7300/7300, p2p: 9003/9003, p2p: 9003/9004/udp)
- op-batcher ()
```

### Benchmarking with contender
[Contender](https://github.com/flashbots/contender) is a tool provided by Flashbots used to simulate MEV/builder-client interactions. We can use it to benchmark and stress-test our local blockchain setup.
- Install Contender CLI on the host machine.
```bash
sudo apt install libsqlite3-dev 
RUSTFLAGS="--cfg tokio_unstable" cargo install --git https://github.com/flashbots/contender --bin contender
```
- We can send transactions to the L2 `op-get` component via its `http` port `8547` (see output above). To successfully do this, we will first have to do some portforwarding from the host machine. A script has been provided to do this already. Open a separate terminal in the host machine and run:
```bash 
./port-forward.sh devnet-vm
```
- Now go the `bench` folder and launch some `contender` scripts. The Python script `bench_devnet.py` runs contender commands like:
```bash
contender spam --tps 10 --min-balance 0.01ETH -r http://localhost:8547 -d 5 fill-block
```
Run the script with `python3 bench_devnet.py`. The script can be modified to send other contender commands. See the contender GitHub page for explanations of these commands. If the devnet is setup correctly, you should see lots of output after running the script. Once the simulation is done, you can run `contender report` which will generate an HTML file with several plots. Open this file in your browser. If on a remote machine, copy it first via SCP to your local machine and open it in the browser.



## Using external builder
This design employs [proposer builder separation]() as explained in our [OPODIS paper](docs/opodis-paper.pdf). Practically speaking, it allows us to point our devnet created above to an external component responsible for building blocks. We integrate this component in a separate VM. 
- To build the builder VM, run `./run_builder.vm`. Similarly, SSH into this VM with:
```bash
multipass shell builder-vm
```
- Similarly, clone this repo and run the setup scripts.
```bash
git clone https://github.com/Yuhala/pbs-tee.git && cd pbs-tee
cd native-vms
./setup.sh
```
- Obtain the builder VM's IP via `multipass list` and update the `BUILDER_IP` variable in the `start_devnet.sh` script to use this IP. Also, use the `--external-builder` option to run the devnet. Save an run the script.

- The builder script: `builder-playground/start_builder.sh` contains the commands to clone, build and start Flashbot's external block builder `op-rbuilder`. Before running the script, we need to copy `l2-genesis.json` file and `jwtsecret` from the devnet VM to this VM. To do this, we have provided some scripts which can be run from the host to first pull these files from the devnet VM, and then push them to the builder-vm. In the host machine do this:
```bash
cd pbs-tee/native-vms
./copy_devnet_data.sh
```
- Verify that these files are indeed in the builder VM's home directory. If the copy is successful, open the `start_builder.sh` file and enter the devnet VM's IP address in the `HOST_IP` shell variable. You can get this IP by running `multipass list` in the host machine: the correct IP is the first in the list in the "IPv4" column for the `devnet-vm`. Save the script and run it with `./start_builder.sh`.

- If you see logs from op-rbuilder similar to the following, this means it is actively receiving blocks from the consensus engine outside. You can confirm by stopping builder playground outside, which will cause these messages to disappear.
```bash
...
2025-08-13T08:30:33.959995Z  INFO Received block from consensus engine number=859 hash=0xa5ae15d7e4268686874607f6ee80d6511466e0db91a2e65695dd584460eb99ca
2025-08-13T08:30:35.960807Z  INFO Received block from consensus engine number=860 hash=0xa20f29c307cfb1f9c6bc3aa7d36945a8e09c37a4201a0d1b5defd37562865bab
```
- Once this is setup, you can also send contender transactions to the devnet's op-geth RPC endpoint and observe the builder output to confirm that it is indeed receiving information from the devnet.


