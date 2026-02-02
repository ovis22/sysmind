import os
import sys
from dotenv import load_dotenv

# Path logic for absolute reliability during demo
PROJECT_ROOT = os.path.dirname(os.path.abspath(__file__))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from rich import print
from backend.core.agent import SysMindAgent

def main():
    """
    SysMind Agent Runner (Platinum Version).
    Standard entry point for automated SRE remediation.
    """
    import sys
    import io
    # Grand Prize Hardening: Force UTF-8 for Windows Terminal stability
    if sys.platform == "win32":
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

    print("\n[bold blue]SYS_MIND ACTIVATED[/bold blue] (TITANIUM EDITION)")
    print("-" * 50)
    
    load_dotenv()
    
    try:
        # Defaults to 'sysmind-target' as per Hackathon specs
        agent = SysMindAgent(target_name="sysmind-target")
        
        if agent.connect():
            # QA KROK 1: Files & Grep Precision
            objective = "Find the secret error message in /tmp/app.log and report exactly what it is."
            agent.ooda_loop(objective)
        else:
            print("[FAIL] Aborting: Target environment unreachable.")
            
    except Exception as e:
        print(f"\n[FATAL ERROR] {e}")

if __name__ == "__main__":
    main()
