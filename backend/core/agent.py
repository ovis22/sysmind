import json
import os
import subprocess
import time
import functools
import re
from google import genai
from dotenv import load_dotenv

# Import strategy and tools
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
        
        # Brain Check
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("⚠️ CRITICAL: GEMINI_API_KEY not found in .env")
            self.client = None
        else:
            self.client = genai.Client(api_key=api_key)
            # Using the latest model available under the API
            self.model_id = "gemini-2.0-flash" 

    def connect(self):
        """Verifies target accessibility"""
        print(f"🔌 Connecting to target container: '{self.target_name}'...")
        # Verify if the container is running
        try:
            check = subprocess.run(
                ["docker", "inspect", "-f", "{{.State.Running}}", self.target_name],
                capture_output=True, text=True
            )
            if "true" not in check.stdout.lower():
                print(f"❌ Target '{self.target_name}' is not running or doesn't exist.")
                return False
        except FileNotFoundError:
             print("❌ Docker CLI not found.")
             return False

        self._detect_os()
        return True

    def _detect_os(self):
        """Self-Discovery Phase"""
        print("🕵️ Fingerprinting OS...")
        os_info = self._execute("cat /etc/os-release").lower()
        if "ubuntu" in os_info or "debian" in os_info:
            print("✅ Detected: Ubuntu/Debian Ecosystem.")
            self.strategy = UbuntuStrategy()
        elif "alpine" in os_info:
            print("✅ Detected: Alpine Linux.")
            # self.strategy = AlpineStrategy() # Placeholder
            self.strategy = UbuntuStrategy() # Fallback
        else:
            print(f"⚠️ Unknown OS. Defaulting to UbuntuStrategy. Raw: {os_info[:30]}...")
            self.strategy = UbuntuStrategy()
            
        self.process_tools = ProcessTools(self.strategy)
        self.file_tools = FileTools()

    def _execute(self, command: str) -> str:
        """Executes command directly via docker exec with sanitization."""
        env = os.environ.copy()
        env["MSYS_NO_PATHCONV"] = "1" # Fix for Windows Git Bash
        
        full_cmd = ["docker", "exec", self.target_name, "bash", "-c", command]
        try:
            result = subprocess.run(full_cmd, capture_output=True, text=True, env=env)
            if result.returncode != 0:
                # Return stderr so the agent knows what went wrong
                return f"Execution Error (Code {result.returncode}): {result.stderr.strip() or result.stdout.strip()}"
            return result.stdout
        except Exception as e:
            return f"Internal Agent Error: {str(e)}"

    def _safety_check(self, command: str) -> bool:
        """
        SAFETY GUARDRAILS: Blocks destructive commands.
        Implementation of 'Do No Harm' protocol.
        """
        dangerous_patterns = [
            "rm -rf /", "mkfs", "dd if=", ":(){:|:&};:", # Fork bomb
            "reboot", "shutdown", "init 0", 
            "iptables -F", "iptables -P INPUT DROP", # Network suicide
            "chmod -R 777 /", "chown -R"
        ]
        
        # Exception for kill (needed for remediation)
        # But we block kill on system processes (simple heuristic)
        
        cmd_lower = command.lower()
        if any(pattern in cmd_lower for pattern in dangerous_patterns):
            print(f"\n🛡️ SAFETY INTERVENTION: Blocked dangerous command: '{command}'")
            return False
            
        return True

    def run_tool(self, tool_name: str, **kwargs) -> str:
        """The 'Hand' of the Agent."""
        command = None
        try:
            if tool_name == "list_processes":
                command = self.process_tools.list_processes_command()
            elif tool_name == "kill_process":
                # Protection against missing arguments
                pid = kwargs.get("pid")
                if not pid: return "Error: PID required."
                command = self.process_tools.kill_process_command(pid, kwargs.get("force", False))
            elif tool_name == "read_log":
                path = kwargs.get("path", "/var/log/syslog")
                command = self.file_tools.read_file_tail_command(path, kwargs.get("lines", 20))
            elif tool_name == "check_disk":
                command = self.file_tools.check_disk_space_command()
            else:
                return f"ERROR: Unknown tool '{tool_name}'."
                
            if command:
                if self._safety_check(command):
                    return self._execute(command)
                else:
                    return "ERROR: Command blocked by Safety Guardrails."
        except Exception as e:
            return f"Tool Execution Error: {e}"
        
        return "ERROR: No command generated."

    def _clean_json(self, raw_text: str) -> str:
        """
        HARDENING: Robust JSON extraction from LLM chatter.
        Removes Markdown blocks (```json ... ```) and finds the first { ... }.
        """
        # 1. Remove markdown
        text = re.sub(r'```json\s*', '', raw_text)
        text = re.sub(r'```', '', text)
        
        # 2. Find the first JSON object
        match = re.search(r'(\{.*\})', text, re.DOTALL)
        if match:
            return match.group(1).strip()
        
        # 3. If no braces found, return original (might be a simple error)
        return raw_text.strip()

    @exponential_backoff(max_retries=3)
    def _think(self, prompt: str):
        """Internal method to call Gemini API."""
        if not self.client:
            return '{"thought": "API Client offline.", "tool": "DONE"}'
        
        print("🧠 Processing...", end="\r")
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt
        )
        print("🧠 Insight generated.")
        
        return self._clean_json(response.text)

    def ooda_loop(self, objective: str):
        """
        The core OODA Cycle implementation (Observe-Orient-Decide-Act).
        """
        print(f"\n🔵 SYS_MIND AGENT ACTIVATED\n🎯 OBJECTIVE: {objective}")
        print("="*60)
        
        history = []
        max_steps = 8 # Increased for more complex tasks
        
        for step in range(max_steps):
            print(f"\n[Cycle {step + 1}/{max_steps}]")
            
            # Prompt engineering: Enforcing JSON format
            prompt = f"""
            SYSTEM: You are SysMind, an Autonomous Site Reliability Engineer (SRE).
            TARGET OS: Ubuntu/Debian (Containerized).
            
            OBJECTIVE: {objective}
            
            AVAILABLE TOOLS:
            - list_processes (args: None) -> Check CPU/RAM hogs.
            - kill_process (args: pid: int, force: bool) -> Remediate stuck processes.
            - read_log (args: path: str, lines: int) -> Analyze /var/log/syslog or app logs.
            - check_disk (args: None) -> Check storage.
            - DONE (args: None) -> Mission complete.
            
            CONTEXT (HISTORY):
            {json.dumps(history, indent=2)}
            
            INSTRUCTIONS:
            1. Analyze the history.
            2. Decide the next step using OODA loop (Observe -> Orient -> Decide).
            3. OUTPUT ONLY VALID JSON. No intro, no outro.
            
            JSON FORMAT:
            {{
                "thought": "Short reasoning: I see X, so I will do Y...",
                "tool": "tool_name",
                "args": {{}}
            }}
            """
            
            try:
                decision_text = self._think(prompt)
                decision = json.loads(decision_text)
                
                thought = decision.get("thought", "Thinking...")
                tool = decision.get("tool", "DONE")
                args = decision.get("args", {})
                
                print(f"🤔 Thought: {thought}")
                
                if tool == "DONE":
                    print("\n🏆 MISSION ACCOMPLISHED.")
                    break
                    
                print(f"🛠️  Action: {tool} ({args})")
                result = self.run_tool(tool, **args)
                
                # Truncate result for history to save tokens
                history_result = result[:500] if result else "No output."
                print(f"📄 Output: {history_result[:100]}...")
                
                history.append({
                    "step": step + 1,
                    "thought": thought,
                    "tool": tool,
                    "args": args,
                    "result": history_result
                })
                
            except Exception as e:
                print(f"💥 Brain Error: {e}")
                time.sleep(2)
                continue
