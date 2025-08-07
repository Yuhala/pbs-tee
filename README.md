## Integrating TEE into blockchain PBS framework
TODO

We use [Builder Playground](https://github.com/flashbots/builder-playground) and [Rollup-Boost](https://github.com/flashbots/rollup-boost) from Flashbots. Builder-playground is used to spin up L1 or L2 environments using Docker: EL/CL clients, validators, MEV-Boost relay, sequencer components, etc. Rollup-Boost enhances the L2 OP-Stack by enabling external block building or TEE-enabled ordering. It intercepts Engine API calls (`engine_FCU`, `engine_getPayLoad`) to route them to both the proposer node and a separate builder node, validating the builder's block before consensus.


## Setup and testing
We first bring up the L1 + L2 (sequencer + proposer) stack using builder-playground. We then configure a separate builder instance with rollup-boost and point it to both the OP stack proposer and a local builder node. When sequencer receives `engine_FCU`, Rollup‑Boost mirrors it to the builder; upon `engine_getPayload`, collects the builder block, validates it, and feeds it back to the sequencer if valid. In certain configurations, the builder will be run in an Intel TDX VM.


