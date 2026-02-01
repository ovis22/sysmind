import os
import sys
from dotenv import load_dotenv

# Robustly add the project root to sys.path
# This ensures it works even if run from a different directory
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

from backend.core.agent import SysMindAgent

def main():
    print("\n🚀 SysMind Agent: Activation Sequence")
    print("---------------------------------------")
    
    load_dotenv()
    
    try:
        # Initialize Agent targeting the local Docker container
        agent = SysMindAgent(target_name="sysmind-target")
        
        if agent.connect():
            # Start the Brain
            objective = "Logs show occasional errors. Analyze /var/log/syslog and check running processes to find the root cause."
            agent.ooda_loop(objective)
        else:
            print("❌ Aborting: Could not connect to target.")
            
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")

if __name__ == "__main__":
    main()
