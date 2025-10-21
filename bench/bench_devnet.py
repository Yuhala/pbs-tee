#!/usr/bin/env python3
import subprocess
import os
import sys
import time

TPS = 10
#RPC_URL = "http://localhost:8555" # non VM localhost
RPC_URL = "http://localhost:8547" 
DURATION = 5
MIN_BALANCE = "0.05 ETH"
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


def main():
    
    print("\n=== Running Contender spammer ===")
    try:
        run_cmd(RESET_CONTENDER_DB)
        run_cmd(CONTENDER_CMD)
    except KeyboardInterrupt:
        print("\n[!] Interrupted, shutting down...")
  

    print("\n ---- Contender done -----.")

if __name__ == "__main__":
    main()
