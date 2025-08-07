## Breakdown of Each Component
- **el (Execution Layer – Geth or similar)**
authrpc: 8551/8551 – Authenticated RPC for engine API (used by consensus layer like beacon)

http: 8545/8545 – Standard JSON-RPC HTTP (wallets/dapps connect here)

metrics: 9090/9090 – Prometheus metrics

rpc: 30303/30303 – Ethereum P2P protocol port (TCP)

ws: 8546/8546 – WebSocket endpoint

- **beacon (Consensus Layer – Lighthouse or similar)**
http: 3500/3500 – Beacon REST API

p2p: 9000/9000/udp – Libp2p/Discovery UDP

p2p: 9000/9001 – TCP Libp2p communication

quic-p2p: 9100/9100 – QUIC-based libp2p communication

**validator**
Empty here (()) – No external ports exposed, likely configured internally in beacon

**op-geth (Execution Layer for L2 – Optimism Geth)**
authrpc: 8551/8552 – Authenticated RPC for L2 engine API

http: 8545/8547 – Standard JSON-RPC HTTP for L2

metrics: 6061/6061 – Prometheus metrics for L2 geth

rpc: 30303/30304 – P2P port for L2 node

ws: 8546/8548 – WebSocket endpoint for L2

**rollup-boost (MEV-Boost for rollup builder separation)**
authrpc: 8551/8553 – Endpoint used for communication with builder/proposer API

**op-node (L2 Rollup node – syncs with L1 and batches data)**
http: 8549/8549 – JSON-RPC or internal HTTP API

metrics: 7300/7300 – Prometheus metrics

p2p: 9003/9003 – TCP p2p connection

p2p: 9003/9004/udp – UDP p2p/discovery

**op-batcher**
No ports shown – typically sends batches to L1, likely configured via internal gRPC or IPC