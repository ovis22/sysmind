import os
import sys
from dotenv import load_dotenv

# Ensure we can import the backend package
sys.path.append(os.getcwd())

from backend.core.agent import SysMindAgent

def main():
    print("\n🚀 SysMind Agent: Activation Sequence")
    print("---------------------------------------")
    
    load_dotenv()
    
    try:
        # Initialize Agent
        agent = SysMindAgent(target_name="sysmind-target")
        agent.connect()
        
        # Start the Brain
        objective = "Logs show occasional errors. Analyze /var/log/syslog and check running processes to find the root cause."
        agent.ooda_loop(objective)
            
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")

if __name__ == "__main__":
    main()
