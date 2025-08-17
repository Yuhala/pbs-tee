## Deploying smart contracts on the L1 + L2 stack
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