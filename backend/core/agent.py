import json
import os
import subprocess
import time
import functools
from google import genai
from dotenv import load_dotenv

# Import our new modules
from ..strategies.base import OSStrategy
from ..strategies.ubuntu import UbuntuStrategy
from ..tools.process import ProcessTools
from ..tools.files import FileTools

load_dotenv()

def exponential_backoff(max_retries=3):
    """Decorator for retrying API calls with exponential wait times."""
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            retries = 0
            while retries < max_retries:
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if "429" in str(e):
                        wait_time = 2 ** retries
                        print(f"⚠️ Quota exceeded (429). Backing off for {wait_time}s...")
                        time.sleep(wait_time)
                        retries += 1
                    else:
                        raise e
            return func(*args, **kwargs)
        return wrapper
    return decorator

class SysMindAgent:
    def __init__(self, target_name: str = "sysmind-target"):
        self.target_name = target_name
        self.strategy: OSStrategy = None
        self.process_tools: ProcessTools = None
        self.file_tools: FileTools = None
        
        # Brain
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("⚠️ WARNING: GEMINI_API_KEY not found in .env")
            self.client = None
        else:
            self.client = genai.Client(api_key=api_key)
            self.model_id = "gemini-2.0-flash"

    def connect(self):
        """Verifies target accessibility"""
        print(f"🔌 Connecting to target '{self.target_name}'...")
        self._detect_os()

    def _detect_os(self):
        """Self-Discovery Phase"""
        os_info = self._execute("cat /etc/os-release").lower()
        if "ubuntu" in os_info or "debian" in os_info:
            print("✅ Detected: Ubuntu/Debian.")
            self.strategy = UbuntuStrategy()
        else:
            self.strategy = UbuntuStrategy()
            
        self.process_tools = ProcessTools(self.strategy)
        self.file_tools = FileTools()

    def _execute(self, command: str) -> str:
        """Executes command directly via docker exec."""
        env = os.environ.copy()
        env["MSYS_NO_PATHCONV"] = "1"
        
        full_cmd = ["docker", "exec", self.target_name, "bash", "-c", command]
        try:
            result = subprocess.run(full_cmd, capture_output=True, text=True, env=env)
            if result.returncode != 0:
                return f"Error: {result.stderr or result.stdout}"
            return result.stdout
        except Exception as e:
            return f"Error executing command: {str(e)}"

    def _safety_check(self, command: str) -> bool:
        """SAFETY LAYER: Intercept dangerous commands."""
        dangerous_patterns = ["kill -9", "rm -rf", "format", "> /dev/sda"]
        if any(pattern in command for pattern in dangerous_patterns):
            print(f"\n🛑 SAFETY ALERT: Agent wants to run: '{command}'")
            choice = input("Proceed? (y/N): ").strip().lower()
            return choice == 'y'
        return True

    def run_tool(self, tool_name: str, **kwargs) -> str:
        """The 'Hand' of the Agent."""
        command = None
        if tool_name == "list_processes":
            command = self.process_tools.list_processes_command()
        elif tool_name == "kill_process":
            command = self.process_tools.kill_process_command(kwargs.get("pid"), kwargs.get("force", False))
        elif tool_name == "read_log":
            command = self.file_tools.read_file_tail_command(kwargs.get("path"), kwargs.get("lines", 20))
            
        if command:
            if self._safety_check(command):
                return self._execute(command)
            else:
                return "ERROR: User denied dangerous command."
        return "ERROR: Unknown tool."

    @exponential_backoff(max_retries=3)
    def _think(self, prompt: str):
        """Internal method to call Gemini API with backoff."""
        if not self.client:
            return '{"thought": "API Client not initialized.", "tool": "DONE"}'
        
        print("🧠 Thinking...")
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt
        )
        return response.text.replace("```json", "").replace("```", "").strip()

    def ooda_loop(self, objective: str):
        """The core OODA Cycle implementation."""
        print(f"\n🧠 BRAIN ACTIVATED. Objective: {objective}")
        history = []
        
        for step in range(5):
            print(f"\n--- OODA Step {step + 1} ---")
            
            # ORIENT & DECIDE (The Cognitive Phase)
            prompt = f"""
            You are SysMind, an autonomous SRE agent.
            Objective: {objective}
            Available Tools: list_processes, kill_process, read_log.
            History of actions: {json.dumps(history, indent=2)}
            Respond with JSON ONLY: {{"thought": "reasoning", "tool": "tool_name", "args": {{...}}}}
            If objective is met, use tool "DONE".
            """
            
            try:
                decision_text = self._think(prompt)
                decision = json.loads(decision_text)
                
                print(f"🤔 Thought: {decision.get('thought')}")
                tool = decision.get("tool")
                args = decision.get("args", {})
                
                if tool == "DONE":
                    print("🏆 Mission Accomplished.")
                    break
                    
                # ACT (The Execution Phase)
                result = self.run_tool(tool, **args)
                
                # OBSERVE (Feedback Loop)
                print(f"📄 Output (truncated): {result[:100]}...")
                history.append({"step": step, "tool": tool, "args": args, "result": result[:300]})
                
            except Exception as e:
                print(f"💥 Brain Error: {e}")
                break
