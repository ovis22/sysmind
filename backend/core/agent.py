import json
import os
import subprocess
from google import genai
from dotenv import load_dotenv

# Import our new modules
from ..strategies.base import OSStrategy
from ..strategies.ubuntu import UbuntuStrategy
from ..tools.process import ProcessTools
from ..tools.files import FileTools

load_dotenv()

class SysMindAgent:
    def __init__(self, target_name: str = "sysmind-target"):
        self.target_name = target_name
        self.strategy: OSStrategy = None
        self.process_tools: ProcessTools = None
        self.file_tools: FileTools = None
        
        # Brain (Placeholder for OODA in Step 7)
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("⚠️ WARNING: GEMINI_API_KEY not found in .env")
        else:
            self.client = genai.Client(api_key=api_key)
            self.model_id = "gemini-2.0-flash"

    def connect(self):
        """Verifies target accessibility using the new transport layer"""
        print(f"🔌 Testing connection to target '{self.target_name}' via docker-exec...")
        self._detect_os()

    def _detect_os(self):
        """Self-Discovery Phase: Use docker exec to check os-release"""
        print("🕵️ Analyzing Host OS...")
        os_info = self._execute("cat /etc/os-release").lower()
        
        if "ubuntu" in os_info or "debian" in os_info:
            print("✅ Detected: Ubuntu/Debian. Loading UbuntuStrategy.")
            self.strategy = UbuntuStrategy()
        else:
            print(f"⚠️ Unknown OS. Defaulting to UbuntuStrategy.")
            self.strategy = UbuntuStrategy()
            
        # Initialize Tools with the selected Strategy
        self.process_tools = ProcessTools(self.strategy)
        self.file_tools = FileTools()

    def _execute(self, command: str) -> str:
        """
        THE REALIZATION: Using subprocess to bypass SSH restrictions.
        Executes command directly via docker exec.
        """
        env = os.environ.copy()
        env["MSYS_NO_PATHCONV"] = "1" # Fix for Git Bash path conversion
        
        full_cmd = ["docker", "exec", self.target_name, "bash", "-c", command]
        try:
            result = subprocess.run(full_cmd, capture_output=True, text=True, env=env)
            if result.returncode != 0:
                return f"Error: {result.stderr or result.stdout}"
            return result.stdout
        except Exception as e:
            return f"Error executing command: {str(e)}"

    def run_tool(self, tool_name: str, **kwargs) -> str:
        command = None
        if tool_name == "list_processes":
            command = self.process_tools.list_processes_command()
        elif tool_name == "kill_process":
            command = self.process_tools.kill_process_command(kwargs.get("pid"), kwargs.get("force", False))
        elif tool_name == "read_log":
            command = self.file_tools.read_file_tail_command(kwargs.get("path"), kwargs.get("lines", 20))
            
        if command:
            return self._execute(command)
        return "ERROR: Unknown tool."
