#!/bin/bash
sudo apt update
sudo apt install curl build-essential pkg-config libssl-dev -y
curl https://sh.rustup.rs -sSf | sh
source $HOME/.cargo/env
cargo --version

sudo apt install golang-go -y
go version 
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
sudo usermod -aG docker $USER


