import subprocess
import time

TARGET = "sysmind-target"

def setup_chaos():
    """
    Grand Prize Chaos Injector.
    Generates REAL system pressure instead of faking logs.
    """
    print(f"[TEST] Preparing REAL chaos in '{TARGET}'...")
    
    # 1. Start the "Villain" - a real memory/CPU stressor
    # --vm 1: Spin 1 worker
    # --vm-bytes 80%: Consume 80% of available memory
    # --vm-hang 0: Continuous pressure
    # --timeout 15m: Run for 15 minutes or until killed
    subprocess.run(
        f"docker exec -d {TARGET} stress-ng --vm 1 --vm-bytes 80% --vm-hang 0 --timeout 15m", 
        shell=True
    )
    print("[OK] Real resource pressure (stress-ng) initiated in background.")
    
    # 2. Add a hint to syslog (Real SREs check logs first)
    # But now it's just a hint, the Agent must confirm with 'top' or 'ps'
    oom_hint = "Feb 2 00:00:00 server kernel: [1234.56] lowmemorykiller: Killing 'stress-ng-vm' due to memory pressure."
    subprocess.run(f"docker exec {TARGET} bash -c 'echo \"{oom_hint}\" >> /var/log/syslog'", shell=True)
    
    print("\n[CHAOS] SYSTEM IS NOW UNDER HEAVY LOAD. PROCEED TO RECORDING.")
    print("[RUN] COMMAND: python run_agent.py")

if __name__ == "__main__":
    setup_chaos()
