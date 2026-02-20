#!/bin/bash

python3 get_cumulative_tx.py no_pbs_no_tee/no-pbs_no-tee_270_tx.csv
python3 get_cumulative_tx.py no_pbs_no_tee/no-pbs_no-tee_30_tx.csv
python3 get_cumulative_tx.py no_pbs_tee/no-pbs_tee_270_tx.csv 
python3 get_cumulative_tx.py no_pbs_tee/no-pbs_tee_30_tx.csv
python3 get_cumulative_tx.py pbs_no_tee/pbs_rbuilder_no-tee_30_tx.csv
python3 get_cumulative_tx.py pbs_no_tee/pbs_rbuilder_no-tee_270_tx.csv
python3 get_cumulative_tx.py pbs_tee/pbs_rbuilder_tee_30_tx.csv
python3 get_cumulative_tx.py pbs_tee/pbs_rbuilder_tee_270_tx.csv