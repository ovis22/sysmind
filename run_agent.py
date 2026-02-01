import os
import sys
from dotenv import load_dotenv

# Path logic for absolute reliability during demo
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from backend.core.agent import SysMindAgent

def main():
    """
    SysMind Agent Runner (Platinum Version).
    Standard entry point for automated SRE remediation.
    """
    print("\n[START] SysMind Agent: Activation Sequence")
    print("-" * 50)
    
    load_dotenv()
    
    try:
        # Defaults to 'sysmind-target' as per Hackathon specs
        agent = SysMindAgent(target_name="sysmind-target")
        
        if agent.connect():
            # Hollywood Scenario: Realistic Remediation
            objective = (
                "CRITICAL ALERT: System is suffering from extreme memory pressure. "
                "1. Investigate the cause using system diagnostic tools (list_processes, grep). "
                "2. Identify and terminate the rogue process to restore stability."
            )
            agent.ooda_loop(objective)
        else:
            print("[FAIL] Aborting: Target environment unreachable.")
            
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")

if __name__ == "__main__":
    main()
