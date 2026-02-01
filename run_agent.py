import os
import sys
import subprocess
from dotenv import load_dotenv

# Ensure we can import the backend package
sys.path.append(os.getcwd())

# Dependency check
try:
    from google import genai
    from backend.core.agent import SysMindAgent
except ImportError:
    print("Installing missing dependencies...")
    subprocess.check_call([sys.executable, "-m", "pip", "install", "google-genai", "python-dotenv"])
    from google import genai
    from backend.core.agent import SysMindAgent

def main():
    print("\n🚀 SysMind Agent: Starting (Subprocess/Docker Mode)")
    print("--------------------------------------------------")
    
    load_dotenv()
    if not os.getenv("GEMINI_API_KEY") or "tu_wklej" in os.getenv("GEMINI_API_KEY"):
        print("⚠️ GEMINI_API_KEY is not set correctly in .env")
        # Continue anyway, agent.py handles it
    
    try:
        # Initialize Agent targeting the 'sysmind-target' container
        agent = SysMindAgent(target_name="sysmind-target")
        agent.connect()
        
        # Test Objective
        objective = "Sprawdź listę procesów i powiedz mi, który z nich zajmuje najwięcej pamięci (RAM)."
        print(f"\n🧠 Starting Reasoning for: '{objective}'")
        
        agent.ooda_loop(objective)
            
    except Exception as e:
        print(f"\n❌ FATAL ERROR: {e}")

if __name__ == "__main__":
    main()
