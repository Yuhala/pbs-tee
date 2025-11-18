#!/bin/bash

#RPC_URL="http://localhost:8545" 
RPC_URL="http://localhost:8547" 
DURATION=5
MIN_BALANCE="0.5ETH"
GAS_LIMIT=10000000

# reset db
contender db reset

# Run at 10 TPS for 60 seconds
contender spam --tps 10 --min-balance ${MIN_BALANCE} -r $RPC_URL -d ${DURATION} --report fill-block

# Run at 25 TPS
contender spam --tps 25 --min-balance ${MIN_BALANCE} -r $RPC_URL -d ${DURATION} --report fill-block

# Run at 50 TPS
contender spam --tps 50 --min-balance ${MIN_BALANCE} -r $RPC_URL -d ${DURATION} --report fill-block

# Or use per-block mode (e.g., 100 tx per block)
contender spam --tps 100 --min-balance ${MIN_BALANCE} -r $RPC_URL -d ${DURATION} --report fill-block

# Generate report and copy DB
#contender report

cp /home/pyuhala/.contender/contender.db .


#contender spam --tps 50 -r http://localhost:8549 fill-block
