#!/bin/bash

rm -rf ~/.local/share/reth
sudo rm -rf ~/.playground
#./builder-playground cook opstack --external-builder http://host.docker.internal:4444
./builder-playground cook opstack --external-builder http://192.168.122.100:4444
