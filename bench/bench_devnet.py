#!/usr/bin/env python3
import subprocess
import os
import sys
import time

PORT = 2222
#RPC_URL = "http://localhost:8555" # non VM localhost
RPC_URL = "http://localhost:" + str(PORT)


TPS = 10
DURATION = 10

MIN_BALANCE = "0.1eth"
# --- Configuration ---
CONTENDER_CMD = [
    "contender",
    "spam",
    "--tps", str(TPS),
    "--min-balance", str(MIN_BALANCE),
    "-r", RPC_URL,
    "-d", str(DURATION),
    "fill-block"
    
]
#contender setup scenario:stress.toml -r $RPC_URL
CONTENDER_SETUP_SCENARIO = [
    "contender",
    "setup",
    "scenario:stress.toml",
    "-r", RPC_URL,
   
    
]

CONTENDER_SPAM_OP = [
    "contender",
    "spam",
    "--tps", str(TPS),
    "--min-balance", str(MIN_BALANCE),
    "-r", RPC_URL,
    "-d", str(DURATION),
    "--gen-report",
    "--op"  
    
]

#contender spam  scenario:stress.toml -r $RPC_URL --tps 10 -d 3
CONTENDER_RUN_SCENARIO = [
    "contender",
    "spam",
    "scenario:stress.toml",
    "--tps", str(TPS),
    "--min-balance", str(MIN_BALANCE),
    "-r", RPC_URL,
    "-d", str(DURATION),
    "--gen-report",  
    
]


RESET_CONTENDER_DB = [
    "contender",
    "db",
    "reset"
]


# --- Helpers ---
def run_cmd(cmd, sudo=False, wait=True):
    """Run a shell command with optional sudo and error checking."""
    if sudo:
        cmd = ["sudo"] + cmd
    print(f"\n[+] Running: {' '.join(cmd)}")
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    if wait:
        for line in proc.stdout:
            print(line, end="")
        proc.wait()
        if proc.returncode != 0:
            print(f"[!] Command failed: {' '.join(cmd)} (exit {proc.returncode})")
            sys.exit(proc.returncode)
        return proc.returncode
    return proc  # caller will handle async processes


def run_contender_test():
    print("\n=== Running Contender test ===")
    try:
        run_cmd(RESET_CONTENDER_DB)
        run_cmd(CONTENDER_CMD)
    except KeyboardInterrupt:
        print("\n[!] Interrupted, shutting down...")
        
def run_contender_spam_op():
    print("\n=== Running Contender spam with --op ===")
    try:
        run_cmd(RESET_CONTENDER_DB)
        run_cmd(CONTENDER_SPAM_OP)
    except KeyboardInterrupt:
        print("\n[!] Interrupted, shutting down...")

def run_contender_scenario():
    print("\n=== Running Contender scenario bench ===")
    try:
        run_cmd(RESET_CONTENDER_DB)
        run_cmd(CONTENDER_SETUP_SCENARIO)
        run_cmd(CONTENDER_RUN_SCENARIO)
    except KeyboardInterrupt:
        print("\n[!] Interrupted, shutting down...")


def main():
    #run_contender_scenario()   
    run_contender_test()
    #run_contender_spam_op()

    print("\n ---- Contender done -----.")

if __name__ == "__main__":
    main()
