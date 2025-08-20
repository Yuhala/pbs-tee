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

- Now spin up the L1 + L2 (sequencer + proposer) stack using builder-playground, specifying the RPC endpoint throughwhich the builder will be reached. A rollup-boost instance is (automaticall) lauched by the `cook` command. When sequencer receives `engine_FCU`, Rollup‑Boost mirrors it to the builder; upon `engine_getPayload`, collects the builder block, validates it, and feeds it back to the sequencer if valid. 

```bash
git clone https://github.com/Yuhala/vm-playground.git && cd vm-playground
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
Here we will spin up the L1 + L2 stack on the host machine and run the builder in a VM (TDX enabled or not)

- First configure libvirt for correct VM setup and management
```bash
sudo virsh net-start default
# verify the state is active
sudo virsh net-list --all
```
- Launch a VM with qemu and connect to it. For a TDX VM, simply follow the instructions in [this Readme](./pbs-tdx/README.md) (section **Setup and run VM**). For a regular (no TDX) VM, you can use a script like `pbs-tdx/boot_normal_vm.sh`. 
- I use the `virbr0` interface for the VMs, so their IPs will be `192.168.122.xxx`. To get all IPs attached to this bridge, do `ip neigh show dev virbr0`. Your VM's IP will be one of them.
- If it's a TDX VM, connect to it with:
```bash
ssh tdx@vm-IP
# example: ssh tdx@192.168.122.100
# default passworld: 123456
```
- If the above SSH fails, you may have to flush the SSH config of any previous VM with the same IP. For example below. Follow the instructions `remove with ...` from the resulting SSH error and redo the SSH login.
```bash
# example below; adapt with the right IP
ssh-keygen -f '/home/pyuhala/.ssh/known_hosts' -R '192.168.122.100'
```
- If it's a regular VM lauched with the above script `boot_normal_vm.sh`, connect to it with:
```bash
ssh -p 2223 ubuntu@IP
# default password: 123456
```

- Once in the VM, install necessary packages.
```bash
# install packages
sudo apt update
sudo apt install build-essential clang libclang-dev
sudo apt install pkg-config
```

- Start builder-playground on host with the option `--external-builder http://<VM-IP>:4444`. 
```bash
# first clean previous states
rm -rf ~/.local/share/reth
sudo rm -rf ~/.playground
# start builder playground
./builder-playground cook opstack --external-builder http://192.168.122.100:4444
```
- Copy builder playground l2-genesis file and jwtsecret to the VM. You can then create an `.env` file containing the paths to these and source it.
```bash
# do this on the host: change IP to your VM's IP
scp ~/.playground/devnet/l2-genesis.json tdx@192.168.122.100:~
scp ~/.playground/devnet/jwtsecret tdx@192.168.122.100:~
```

- In the VM, create an .env file defining the paths to these files.
```bash
L2_GENESIS="$HOME/l2-genesis.json"
JWT_SECRET="$HOME/jwtsecret"
```
```bash
source .env
```
- Then download and run op-rbuilder in the VM.
```bash
git clone https://github.com/flashbots/op-rbuilder.git
cd op-rbuilder
# rm old reth if present
rm -rf ~/.local/share/reth
# run op-rbuilder
cargo run -p op-rbuilder --bin op-rbuilder -- node \
    --chain $L2_GENESIS \
    --http --http.port 2222 \
    --authrpc.addr 0.0.0.0 --authrpc.port 4444 --authrpc.jwtsecret $JWT_SECRET \
    --port 30333 --disable-discovery \
    --metrics 0.0.0.0:9011 \
    --rollup.builder-secret-key ac0974bec39a17e36ba4a6b4d238ff944bacb478cbed5efcae784d7bf4f2ff80 \
    --trusted-peers enode://79be667ef9dcbbac55a06295ce870b07029bfcdb2dce28d959f2815b16f81798483ada7726a3c4655da4fbfc0e1108a8fd17b448a68554199c47d08ffb10d4b8@<host IP>:30304
```
- If you see logs from op-rbuilder similar to the following, this means it is actively receiving blocks from the consensus engine outside. You can confirm by stopping builder playground outside, which will cause these messages to disappear.
```bash
...
2025-08-13T08:30:33.959995Z  INFO Received block from consensus engine number=859 hash=0xa5ae15d7e4268686874607f6ee80d6511466e0db91a2e65695dd584460eb99ca
2025-08-13T08:30:35.960807Z  INFO Received block from consensus engine number=860 hash=0xa20f29c307cfb1f9c6bc3aa7d36945a8e09c37a4201a0d1b5defd37562865bab
```

## Benchmarking with contender
[Contender]() is a tool provided by Flashbots used to simulate MEV/builder-client interactions. We can use it to benchmark and stress-test our local blockchain setup.
- Install Contender CLI
```bash
sudo apt install libsqlite3-dev 
RUSTFLAGS="--cfg tokio_unstable" cargo install --git https://github.com/flashbots/contender --bin contender
```
- Send some transactions to the builder. Observe the output from op-rbuilder.
```bash
contender spam --tpb 50 -r <builder endpoint> fill-block
# Example: contender spam --tpb 50 -r http://192.168.122.100:4444 fill-block
```
```bash
contender spam scenario:stress.toml \
  -r http://localhost:8545 \
  --auth http://192.168.122.100:4444 \
  --jwt ~/.playground/devnet/jwtsecret \
  --fcu \
  --op \
  --tps 200 -d 2 -w 3
```
- See [Contender Readme](https://github.com/flashbots/contender/blob/main/README.md) for more examples and options.

contender spam scenario:stress.toml \
  -r http://localhost:8545 \
  --auth http://192.168.122.100:4444 \
  --jwt ~/.playground/devnet/jwtsecret \
  --fcu \
  --op \
  --tps 200 -d 2 -w 3

## Testing smart contract deployment (optional)
- See this 

## Viewing metrics
- The builder playground output specifies Prometheus metrics can be obtained at port `7300`. To view from a local PC, SSH as follows:
```bash
ssh -L <port>:localhost:<port> <username@remote-hostname>
```

