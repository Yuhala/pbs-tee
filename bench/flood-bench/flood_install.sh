#!/bin/bash

sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-venv

sudo apt install golang-go
go install github.com/tsenart/vegeta/v12@v12.8.4

echo 'export PATH=$PATH:~/go/bin' >> ~/.bashrc
source ~/.bashrc
which vegeta

python3.11 -m venv ~/flood-env
source ~/flood-env/bin/activate
pip install paradigm-flood
pip install "lxml[html_clean]"
# install vegeta


# Expected output: /home/pyuhala/go/bin/vegeta


