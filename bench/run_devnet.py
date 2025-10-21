#!/usr/bin/env python3
import subprocess
import os
import sys
import time

# --- Configuration ---
USE_EXTERNAL_BUILDER=False
TPS = 10
BUILDER_URL = "http://192.168.122.100:4444"
DURATION = 5
PLAYGROUND_BINARY = "/home/pyuhala/pbs-tee/builder-playground/builder-playground"


PLAYGROUND_CMD = [
    PLAYGROUND_BINARY,
    "cook",
    "opstack"
]

if (USE_EXTERNAL_BUILDER == True):
    PLAYGROUND_CMD.append("--external-builder")
    PLAYGROUND_CMD.append(BUILDER_URL)

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
    print("\n=== Cleaning up old devnet state ===")
    run_cmd(["rm", "-rf", os.path.expanduser("~/.local/share/reth")])
    run_cmd(["sudo", "rm", "-rf", os.path.expanduser("~/.playground")])

    print("\n=== Launching Builder Playground Devnet ===")
    playground_proc = run_cmd(PLAYGROUND_CMD, wait=False)
    time.sleep(8)  # Give it a few seconds to initialize



if __name__ == "__main__":
    main()
