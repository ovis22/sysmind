import subprocess
import time

TARGET = "sysmind-target"

def setup_chaos():
    print(f"[TEST] Preparing chaos in '{TARGET}'...")
    
    # 1. Ensure syslog exists
    subprocess.run(f"docker exec {TARGET} bash -c 'touch /var/log/syslog'", shell=True)
    
    # 2. Inject the "Hook" - a fake OOM error
    oom_log = "Feb 1 20:00:00 server kernel: [1234.56] Out of memory: Kill process 1337 (python3) score 999 or sacrifice child"
    subprocess.run(f"docker exec {TARGET} bash -c 'echo \"{oom_log}\" >> /var/log/syslog'", shell=True)
    print("[OK] Logic bomb injected into syslog (OOM error).")

    # 3. Start the "Villain" - an infinite rogue process that must be killed
    subprocess.run(f"docker exec -d {TARGET} python3 -c 'import time; print(\"I am the villain\"); while True: [x**2 for x in range(1000)]'", shell=True)
    print("[OK] Rogue process 'python3' started in background.")
    
    print("\n[CHAOS] SYSTEM IS NOW UNSTABLE. PROCEED TO RECORDING.")
    print("[RUN] COMMAND: python run_agent.py")

if __name__ == "__main__":
    setup_chaos()
