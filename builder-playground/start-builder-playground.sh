#!/bin/bash

rm -rf ~/.local/share/reth
sudo rm -rf ~/.playground
./builder-playground cook opstack --external-builder http://host.docker.internal:4444