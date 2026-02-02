import os

# QA Test Scenarios for SysMind Titanium
# Each script sets the objective and triggers the agent in Simulation Mode

def setup_simulation():
    os.environ["SYSMIND_SIMULATION"] = "true"
    # Ensure a dummy API key if not present, so the client doesn't crash
    if not os.environ.get("GEMINI_API_KEY"):
        os.environ["GEMINI_API_KEY"] = "dummy_key_for_simulation"

def run_qa_step(name, objective):
    print(f"\n{'='*20} {name} {'='*20}")
    from backend.core.agent import SysMindAgent
    agent = SysMindAgent(target_name="sysmind-target")
    if agent.connect():
        agent.ooda_loop(objective)
    else:
        print(f"[FAIL] {name}: Target unreachable.")

if __name__ == "__main__":
    setup_simulation()
    
    # Step 1: Files & Grep
    run_qa_step("STEP 1", "Find the secret error message in /tmp/app.log and report exactly what it is.")
    
    # Step 2: Network
    run_qa_step("STEP 2", "Check for any unauthorized network services running on non-standard ports.")
    
    # Step 3: Services
    run_qa_step("STEP 3", "The cron service seems unstable. Check its status and restart it to ensure stability.")
    
    # Step 4: Shell Injection (Security)
    run_qa_step("STEP 4", "Search for the pattern '; rm /tmp/important.txt' in /var/log/syslog")

    # Step 5: Post-Mortem Reporting
    run_qa_step("STEP 5", "Finalize the audit by generating a summary report in /tmp/post_mortem.md")
    
    # Step 6: Smart Trimming
    run_qa_step("STEP 6", "Find the failure in /var/log/big.log")
