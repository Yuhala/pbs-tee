## Context
TODO

We use [Builder Playground](https://github.com/flashbots/builder-playground) and [Rollup-Boost](https://github.com/flashbots/rollup-boost) from Flashbots. Builder-playground is used to spin up L1 or L2 environments using Docker: EL/CL clients, validators, MEV-Boost relay, sequencer components, etc. Rollup-Boost enhances the L2 OP-Stack by enabling external block building or TEE-enabled ordering. It intercepts Engine API calls (`engine_FCU`, `engine_getPayLoad`) to route them to both the proposer node and a separate builder node, validating the builder's block before consensus.


## Setup and testing
We first bring up the L1 + L2 (sequencer + proposer) stack using builder-playground. We then configure a separate builder instance with rollup-boost and point it to both the OP stack proposer and a local builder node. When sequencer receives `engine_FCU`, Rollup‑Boost mirrors it to the builder; upon `engine_getPayload`, collects the builder block, validates it, and feeds it back to the sequencer if valid. In certain configurations, the builder will be run in an Intel TDX VM.

- Setup Cargo
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

- Setup OP-stack (L1 + L2)
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
- Query the testnet with some curl instructions by running the `test-query.sh` script.
```bash
./test-query.sh
```

- Generate JSON web tokens (JWT). Do this once and copy tokens if components are on different systems. 
```bash
mkdir -p tokens && cd tokens
openssl rand -hex 32 > builder-jwt.hex # generate builder token
openssl rand -hex 32 > l2-jwt.hex # generate builder token
```
- The actual JWTs will be generated internally using these 32-byte hex strings.

- Setup Rollup-Boost
```bash
cargo run --bin rollup-boost -- \
 --l2-url http://localhost:8545 \
 --l2-jwt-path tokens/l2-jwt.hex \
 --builder-jwt-path tokens/builder-jwt.hex \
 --builder-url http://localhost:8546
```