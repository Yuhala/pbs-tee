#!/bin/bash

# connect to TDX VM
ssh -L 8547:localhost:8547 -p 10022 tdx@localhost

# connect to Ubuntu VM
ssh -L 8547:localhost:8547 -p 2223 ubuntu@localhost
