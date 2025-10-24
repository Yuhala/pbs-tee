#!/bin/bash

multipass authenticate # enter passphrase

multipass transfer devnet-vm:/home/ubuntu/.playground/devnet/jwtsecret .
multipass transfer devnet-vm:/home/ubuntu/.playground/devnet/l2-genesis.json .
multipass transfer jwtsecret builder-vm:/home/ubuntu/
multipass transfer l2-genesis.json builder-vm:/home/ubuntu/