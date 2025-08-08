## Context
TODO

We use [Builder Playground](https://github.com/flashbots/builder-playground) and [Rollup-Boost](https://github.com/flashbots/rollup-boost) from Flashbots. Builder-playground is used to spin up L1 or L2 environments using Docker: EL/CL clients, validators, MEV-Boost relay, sequencer components, etc. Rollup-Boost enhances the L2 OP-Stack by enabling external block building or TEE-enabled ordering. It intercepts Engine API calls (`engine_FCU`, `engine_getPayLoad`) to route them to both the proposer node and a separate builder node, validating the builder's block before consensus.


## Builder playgroud setup 
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

## Testing smart contract deployment
- The tests folder contains some scripts on building and testing simply smart contracts on our local devnet. We use Hardhat for contract dev.
- Install and initialize Hardhat and deps

```bash
cd tests
mkdir builder-contract && cd builder-contract
curl -fsSL https://deb.nodesource.com/setup_lts.x | sudo -E bash -
sudo apt-get install -y nodejs
npm init -y
npm install --save-dev hardhat 
npm hardhat init 
```
- Replace the `contracts/Lock.sol` with your solidity contract. For example `Helloworld.sol` as follows
```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract HelloWorld {
    string public message;

    constructor(string memory initMessage) {
        message = initMessage;
    }

    function setMessage(string memory newMessage) public {
        message = newMessage;
    }
}
```
- Add your devnet information to the `hardhat.config.js` file.
```js
const PRIVATE_KEY = "0x2a871d0798f97d79848a013d4936a73bf4cc922c825d33c1cf7073dff6d409c6"; // Replace with your testnet private key


/** @type import('hardhat/config').HardhatUserConfig */
module.exports = {
  solidity: "0.8.28",
  networks: {
    builderplayground: {
      url: "http://localhost:8545",  // or your builder playground L2 RPC endpoint
      accounts: [PRIVATE_KEY]
    }
  }
};
```
- Compile and deploy the smart contract on the devnet
```bash
npx hardhat compile
npx hardhat run --network builderplayground scripts/deploy.js
```

- Using foundry
```bash
forge init hello-foundry
# add code in src/Helloworld.sol
```
- Write deploy script as in `script/DeployHelloworld.s.sol`
- Deploy the contract with:
```bash
forge script script/DeployHelloWorld.s.sol:DeployHelloWorld --fork-url <RPC_URL> --broadcast
# Example: forge script script/DeployHelloWorld.s.sol:DeployHelloWorld --fork-url  http://localhost:8545 --broadcast
# RPC_URL = http://localhost:8545
```
- To avoid entering rpc url and other constants, enter them in the `.env` file and source this file before running.
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
- Testing transaction (after deploying SendHello)
```bash
cast send 0xA7e3FFB41Db860Fd0D97186e0c3De1E424c96C9f \
    "setMessage(string)" "Hello from L2 sequencer!" \
    --rpc-url $RPC_URL \
    --private-key $PRIVATE_KEY
	--gas-price 2000000000000 # increase if it fails
```
Results should look like
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

## Integrating Rollup-Boost for external block building




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