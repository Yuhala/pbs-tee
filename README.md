## Context
Testing proposer-builder-separation (PBS) with VM-based builder. [Builder Playground](https://github.com/flashbots/builder-playground) is used to spin a local L1 + L2 environment based on Docker: EL/CL clients, validators, MEV-Boost relay, sequencer components, and Rollup-Boost enhances the L2 OP-Stack by enabling external block building or TEE-enabled ordering. It intercepts Engine API calls (`engine_FCU`, `engine_getPayLoad`) to route them to both the proposer node and a separate builder node, validating the builder's block before consensus. 

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
- Rollup-Boost serves as a relay between your L2 stack and an external block builder. So first we need to configure an external block builder and then use rollup boost to link them. We use [Flashbot's op-rbuilder](https://github.com/flashbots/op-rbuilder.git).
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
So we don't need to run it separately. However, if you are running rollup-boost separately, you will need to point rollup-boost to the `Engine API` of the L2 execution client (`op-geth`). From the builder playground logs, this should be `http://localhost:8551`. See [Rollup-Boost documentation here](https://github.com/flashbots/rollup-boost).

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


## Part II: L1 + L2 stack and builder on separate machines or VMs
Here we will spin up the L1 + L2 stack on the host machine and run the builder in a VM (TDX enabled or not)

- First configure libvirt for correct VM setup and management
```bash
sudo virsh net-start default
# verify the state is active
sudo virsh net-list --all
```
- Launch a VM with qemu and connect to it. For a regular (no TDX) VM, you can use a script like `pbs-tdx/boot_normal_vm.sh`. For a TDX VM, simply follow the instructions in [this Readme](./pbs-tdx/README.md).
- I use the `virbr0` interface for the VMs, so their IPs will be `192.168.122.xxx`. To get all IPs attached to this bridge, do `ip neigh show dev virbr0`. Your VM's IP will be one of them.
- Connect to the VM with
```bash
ssh -p 2223 ubuntu@IP
# default password: 123456
```
- If it's a TDX VM, connect to it with
```bash
ssh tdx@vm-ip
# default passworld: 123456
```
- Setup VM
Install the following packages in the VM
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
- Copy builder playground l2-genesis file and jwtsecret to VM. You can then create an `.env` file containing the paths to these and source it.
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

## Testing smart contract deployment (optional)
> This section is not complete yet, but some of the tests work
- The tests folder contains some scripts on building and testing simply smart contracts on our local devnet. We use Foundry for contract dev.

```bash
curl -L https://foundry.paradigm.xyz | bash
foundryup
forge init hello-foundry
# add code in src/Helloworld.sol
```
- Write example smart contract, example in `src/HelloWorld.sol`

- To avoid entering rpc url and other constants, enter them in the [.env](./builder-playground/.env) file and source this file before running.
- Another way to deploy contract:
```bash
forge create --rpc-url $RPC_URL --private-key $PRIVATE_KEY src/HelloWorld.sol:HelloWorld --legacy --broadcast
```
- Results should look like.
```bash
Deployer: 0xa0Ee7A142d267C1f36714E4a8F75612F20a79720
Deployed to: 0xc4De0f5aB3C6EA3882C39BD356d2c4C1D4B0B6Ea
Transaction hash: 0x3324264a1984aab7996c65f287a5b3dac06d4788a5fe8a1fa66b485c3cfdd011
```
- If you have error `...transaction underpriced`, redo `forge create` with gas price option: `--gas-price 20000000000`

- Use `cast` to check contract code at an address
```bash
cast code 0xc4De0f5aB3C6EA3882C39BD356d2c4C1D4B0B6Ea --rpc-url $RPC_URL
```
- Call contract.
```bash
cast call 0xc4De0f5aB3C6EA3882C39BD356d2c4C1D4B0B6Ea "sayHello()" --rpc-url $RPC_URL | cast --to-ascii
```
- Build and deploy the `SendHello` transaction which is state-changing and invokes the block builder.
```bash
# Build first with forge create
forge create --rpc-url $RPC_URL --private-key $PRIVATE_KEY src/SendHello.sol:SendHello --legacy --broadcast
# send transaction
cast send 0xA7e3FFB41Db860Fd0D97186e0c3De1E424c96C9f \
    "setMessage(string)" "Hello from L2 sequencer!" \
    --rpc-url $RPC_URL \
    --private-key $PRIVATE_KEY
	--gas-price 2000000000000 # increase if it fails
```
Results should look like below: we can see block hash and number, indicating a block is created. 
```bash
blockHash            0x118dd2e2daf61cea406c18c869fa13fc3a364eb266a6bd9469f97b18713d896d
blockNumber          313
contractAddress      
cumulativeGasUsed    28282
effectiveGasPrice    1000000007
from                 0xa0Ee7A142d267C1f36714E4a8F75612F20a79720
gasUsed              28282
logs                 []
logsBloom            0x00000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000000
root                 
status               1 (success)
transactionHash      0xaf994f415cec563aacff311145959ece7c519733010dac5ca9c42b5ae6502d93
transactionIndex     0
type                 2
blobGasPrice         
blobGasUsed          
to                   0xA7e3FFB41Db860Fd0D97186e0c3De1E424c96C9f

```
- Verify the message
```bash
cast call $CONTRACT_ADDRESS "message()(string)" --rpc-url $RPC_URL
# Example: cast call 0xA7e3FFB41Db860Fd0D97186e0c3De1E424c96C9f "message()(string)" --rpc-url $RPC_URL
```
- Check latest block with 
```bash
cast block latest --rpc-url http://localhost:8545
```

## Viewing metrics
- The builder playground output specifies Prometheus metrics can be obtained at port `7300`. To view from a local PC, SSH as follows:
```bash
ssh -L <port>:localhost:<port> <username@remote-hostname>
```