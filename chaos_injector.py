import subprocess
import time
import sys
import argparse
from datetime import datetime

import os
from dotenv import load_dotenv

# Load env vars first
load_dotenv()

# Allow overriding target for flexibility
TARGET = os.getenv("TARGET_CONTAINER", "sysmind-target")

def check_target_running():
    """Ensure target container is running."""
    res = subprocess.run(
        f"docker inspect -f '{{{{.State.Running}}}}' {TARGET}", 
        shell=True, capture_output=True, text=True
    )
    if "true" not in res.stdout.lower():
        print(f"[ERROR] Target container '{TARGET}' is not running. Start it first!")
        sys.exit(1)

def inject_cpu_stress():
    """SCENARIO 1: High Memory/CPU Load (The Brute Force Attack)"""
    print(f"\n[SCENARIO: CPU/MEM STRESS] simulating resource exhaustion...")
    
    # --vm 1: Spin 1 worker
    # --vm-bytes 80%: Consume 80% of available memory
    # --vm-hang 0: Continuous pressure
    # --timeout 15m: Run for 15 minutes or until killed
    cmd = f"docker exec -d {TARGET} stress-ng --vm 1 --vm-bytes 80% --vm-hang 0 --timeout 15m"
    subprocess.run(cmd, shell=True)
    
    # Grand Prize: Dynamic Timestamping for live demos
    current_date = datetime.now().strftime("%b %d %H:%M:%S")
    
    # Add a hint log with CURRENT timestamp
    oom_hint = f"{current_date} server kernel: [1234.56] lowmemorykiller: Killing 'stress-ng-vm' (1234), adj 0, caused by 'high-load-scenario'"
    subprocess.run(f"docker exec {TARGET} bash -c 'echo \"{oom_hint}\" >> /var/log/syslog'", shell=True)
    
    print("[OK] stress-ng initiated. RAM usage should spike to >80%.")
    print("OBJECTIVE: Agent must identify 'stress-ng-vm' utilizing high resources and terminate it.")

def inject_unknown_process():
    """SCENARIO 2: Port Hijack (The Silent Killer)"""
    print(f"\n[SCENARIO: PORT HIJACK] simulating zombie process blocking production port...")
    
    # 1. Start a "rogue" python server on port 8080
    # This simulates a zombie process or a developer testing in prod that forgot to kill a process
    cmd = f"docker exec -d {TARGET} python3 -m http.server 8080"
    subprocess.run(cmd, shell=True)
    
    print("[OK] Rogue 'python3' process started on port 8080.")
    print("OBJECTIVE: Agent must detect port 8080 is occupied, find the PID, and kill the zombie process.")

def main():
    parser = argparse.ArgumentParser(description="SysMind Chaos Injector (Grand Prize Edition)")
    parser.add_argument("mode", choices=["cpu", "zombie"], help="Chaos mode to inject")
    args = parser.parse_args()

    check_target_running()

    if args.mode == "cpu":
        inject_cpu_stress()
    elif args.mode == "zombie":
        inject_unknown_process()

    print(f"\n[CHAOS INJECTED] Proceed to run agent: python run_agent.py")

if __name__ == "__main__":
    main()
