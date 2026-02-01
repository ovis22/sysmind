import os
import subprocess
import time
import functools
from google import genai
from google.genai import types
from backend.strategies.ubuntu import UbuntuStrategy
from backend.tools.process import ProcessTools
from backend.tools.files import FileTools

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
                        print(f"[RETRY] Quota exceeded (429). Backing off for {wait_time}s...")
                        time.sleep(wait_time)
                        retries += 1
                    else:
                        raise e
            return func(*args, **kwargs)
        return wrapper
    return decorator

class SysMindAgent:
    """
    SysMind: An autonomous SRE Agent for Linux Systems. (Platinum Version)
    Powered by Gemini 3 Flash.
    """
    
    def __init__(self, target_name: str = "sysmind-target"):
        self.target_name = target_name
        self.strategy = None
        self.process_tools = None
        self.file_tools = None
        
        # Identity Policy
        self.identity = (
            "You are SysMind, an elite Autonomous SRE Agent. "
            "Your objective is to diagnose and repair Linux systems with precision. "
            "You have access to native tools. Use them logically. "
            "Always verify the state of the system before and after actions. "
            "If you find a rogue process, kill it. If a log is missing, explore the directory."
        )

        # Brain Check
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("[CRITICAL] GEMINI_API_KEY not found in .env")
            self.client = None
        else:
            self.client = genai.Client(api_key=api_key)
            # Using Gemini 3 Flash for the Hackathon
            self.model_id = "gemini-3-flash-preview" 

    def connect(self):
        """Verifies target accessibility with safety timeout."""
        print(f"[CONN] Connecting to target container: '{self.target_name}'...")
        try:
            # Added timeout=10 to prevent hanging during demo
            check = subprocess.run(
                ["docker", "inspect", "-f", "{{.State.Running}}", self.target_name],
                capture_output=True, text=True, timeout=10
            )
            if "true" not in check.stdout.lower():
                print(f"[FAIL] Target '{self.target_name}' is not running.")
                return False
        except subprocess.TimeoutExpired:
             print("[FAIL] Connection timed out (Docker unresponsive).")
             return False
        except FileNotFoundError:
             print("[FAIL] Docker CLI not found.")
             return False

        self._detect_os()
        return True

    def _detect_os(self):
        """Self-Discovery Phase"""
        print("[OS] Fingerprinting OS...")
        os_info = self._execute("cat /etc/os-release").lower()
        if "ubuntu" in os_info or "debian" in os_info:
            print("[OS] Detected: Ubuntu/Debian Ecosystem.")
            self.strategy = UbuntuStrategy()
        else:
            print(f"[OS] Defaulting to UbuntuStrategy.")
            self.strategy = UbuntuStrategy()
            
        self.process_tools = ProcessTools(self.strategy)
        self.file_tools = FileTools()

    def _execute(self, command: str) -> str:
        """Executes command via docker exec with safety timeout."""
        env = os.environ.copy()
        env["MSYS_NO_PATHCONV"] = "1"
        
        full_cmd = ["docker", "exec", self.target_name, "bash", "-c", command]
        try:
            # Added timeout=10 to prevent hanging during execution
            result = subprocess.run(full_cmd, capture_output=True, text=True, env=env, timeout=10)
            if result.returncode != 0:
                return f"Error (Code {result.returncode}): {result.stderr.strip() or result.stdout.strip()}"
            return result.stdout
        except subprocess.TimeoutExpired:
            return "Error: Execution timed out (10s limit exceeded)."
        except Exception as e:
            return f"Error: {str(e)}"

    def _safety_check(self, command: str) -> bool:
        """Context-Aware Safety Guardrails."""
        cmd_lower = command.lower()
        
        # Hard Blacklist
        critical = ["mkfs", "dd if=", ":(){:|:&};:", "reboot", "shutdown", "init 0"]
        if any(p in cmd_lower for p in critical):
            print(f"\n[SAFETY] Blocked destructive system command: '{command}'")
            return False

        # Contextual 'rm'
        if "rm " in cmd_lower:
            if not ("/tmp/" in cmd_lower or ".log" in cmd_lower):
                print(f"\n[SAFETY] 'rm' restricted to /tmp/ or *.log. Blocked: '{command}'")
                return False
            if "rm -rf /" in cmd_lower or cmd_lower.strip().endswith("/"):
                print(f"\n[SAFETY] Blocked potential root-level deletion.")
                return False

        return True

    def _get_tools_config(self):
        """Definitions for Gemini 3 Native Tool Use (Platinum)."""
        return [
            types.FunctionDeclaration(
                name="list_processes",
                description="Check running processes for resource usage.",
                parameters=types.Schema(type="OBJECT", properties={})
            ),
            types.FunctionDeclaration(
                name="list_directory",
                description="List contents of a directory to explore the system (The Eyes).",
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "path": types.Schema(type="STRING", description="Directory path (default /).")
                    }
                )
            ),
            types.FunctionDeclaration(
                name="kill_process",
                description="Terminate a process by its PID.",
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "pid": types.Schema(type="INTEGER", description="The Process ID to kill."),
                        "force": types.Schema(type="BOOLEAN", description="Forcefully terminate.")
                    },
                    required=["pid"]
                )
            ),
            types.FunctionDeclaration(
                name="read_log",
                description="Examine system or application logs.",
                parameters=types.Schema(
                    type="OBJECT",
                    properties={
                        "path": types.Schema(type="STRING", description="Log path."),
                        "lines": types.Schema(type="INTEGER", description="Number of lines.")
                    },
                    required=["path"]
                )
            ),
            types.FunctionDeclaration(
                name="mission_complete",
                description="Finalize mission with a summary.",
                parameters=types.Schema(
                    type="OBJECT",
                    properties={"summary": types.Schema(type="STRING")},
                    required=["summary"]
                )
            )
        ]

    def run_tool(self, name: str, **kwargs) -> str:
        """Routes tool calls to actual system implementations."""
        if name == "list_processes":
            cmd = self.process_tools.get_list_command()
            return self._execute(cmd)
            
        elif name == "list_directory":
            path = kwargs.get("path", "/")
            # Use -F to distinguish file types visually for the model
            return self._execute(f"ls -F {path}")
            
        elif name == "kill_process":
            pid = kwargs.get("pid")
            force = kwargs.get("force", False)
            if pid:
                cmd = self.process_tools.get_kill_command(pid, force)
                if self._safety_check(cmd):
                    return self._execute(cmd)
                return "Safety Violation: Command blocked."
            return "Error: Missing PID."

        elif name == "read_log":
            path = kwargs.get("path")
            lines = kwargs.get("lines", 20)
            if path:
                cmd = self.file_tools.get_read_command(path, lines)
                return self._execute(cmd)
            return "Error: Missing path."

        return f"Error: Tool '{name}' not implemented."

    @exponential_backoff(max_retries=3)
    def _think(self, prompt: str):
        """Native Tool Calling with Platinum Configuration."""
        if not self.client: return "ERROR", "Offline"
        
        print("[BRAIN] Processing...")
        tools = [types.Tool(function_declarations=self._get_tools_config())]
        
        # Gemini 3 Platinum: Using native system_instruction for persona
        response = self.client.models.generate_content(
            model=self.model_id,
            contents=prompt,
            config=types.GenerateContentConfig(
                tools=tools,
                system_instruction=self.identity
            )
        )
        print("[BRAIN] Insight generated.")
        
        if not response.candidates or not response.candidates[0].content.parts:
            return "THOUGHT", "The model returned an empty response (possible safety trigger)."

        for part in response.candidates[0].content.parts:
            if part.function_call:
                # Convert Protobuf/MapComposite to DICT for Python
                args = {}
                if part.function_call.args:
                    args = {k: v for k, v in part.function_call.args.items()}
                return part.function_call.name, args
        
        return "THOUGHT", response.candidates[0].content.parts[0].text

    def ooda_loop(self, objective: str):
        """OODA Loop with Persistence and Robustness."""
        print(f"\n[AGENT] SYS_MIND ACTIVATED (PLATINUM)\n[TARGET] OBJECTIVE: {objective}")
        print("="*60)
        
        history = []
        max_steps = 10
        
        for step in range(max_steps):
            print(f"\n[Cycle {step + 1}/{max_steps}]")
            
            # Reconstruct stateless context
            context = f"OBJECTIVE: {objective}\n\nHISTORY:\n"
            for h in history:
                context += f"- Step {h['step']}: {h['tool']}({h['args']}) -> {h['result']}\n"

            try:
                tool_name, tool_args = self._think(context)
                
                # Persistence Fix: Save 'THOUGHT' to history to avoid loops
                if tool_name == "THOUGHT":
                    print(f"[BRAIN] Thought: {tool_args}")
                    history.append({
                        "step": step + 1,
                        "tool": "THOUGHT",
                        "args": {},
                        "result": tool_args
                    })
                    continue

                if tool_name == "mission_complete":
                    print(f"\n[SUCCESS] MISSION ACCOMPLISHED: {tool_args.get('summary')}")
                    break
                    
                print(f"[ACTION] {tool_name} {tool_args}")
                result = self.run_tool(tool_name, **tool_args)
                
                print(f"[OUTPUT] {result[:100]}...")
                history.append({
                    "step": step + 1,
                    "tool": tool_name,
                    "args": tool_args,
                    "result": result[:500]
                })
                
            except Exception as e:
                print(f"[ERROR] Brain Failure: {e}")
                time.sleep(1)
