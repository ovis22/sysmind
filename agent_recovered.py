import json
import paramiko
from google import genai
import os
from dotenv import load_dotenv

# Import our new modules
from ..strategies.base import OSStrategy
from ..strategies.ubuntu import UbuntuStrategy
from ..tools.process import ProcessTools
from ..tools.files import FileTools

load_dotenv()

class SysMindAgent:
    def __init__(self, host: str, user: str, key_path: str = None, password: str = None):
        self.host = host
        self.user = user
        self.ssh_client = paramiko.SSHClient()
        self.ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        self.key_path = key_path
        self.password = password
        
        # Components
        self.strategy: OSStrategy = None
        self.process_tools: ProcessTools = None
        self.file_tools: FileTools = None
        
        # Brain
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            print("⚠️ WARNING: GEMINI_API_KEY not found in .env")
        else:
            self.client = genai.Client(api_key=api_key)
            self.chat = self.client.chats.create(model="gemini-2.0-flash-exp")

    def connect(self):
        print(f"🔌 Connecting to {self.host}...")
        connect_kwargs = {"hostname": self.host, "username": self.user}
        if self.key_path:
            connect_kwargs["key_filename"] = self.key_path
        if self.password:
            connect_kwargs["password"] = self.password
            
        self.ssh_client.connect(**connect_kwargs)
        self._detect_os()

    def _detect_os(self):
        """Self-Discovery Phase: Load the correct strategy"""
        print("🕵️ Analyzing Host OS...")
        stdin, stdout, stderr = self.ssh_client.exec_command("cat /etc/os-release")
        os_info = stdout.read().decode().lower()
        
        if "ubuntu" in os_info or "debian" in os_info:
            print("✅ Detected: Ubuntu/Debian. Loading UbuntuStrategy.")
            self.strategy = UbuntuStrategy()
        else:
            # Fallback or Error
            print(f"⚠️ Unknown OS. Defaulting to UbuntuStrategy (Risky). Raw: {os_info[:50]}...")
            self.strategy = UbuntuStrategy()
            
        # Initialize Tools with the selected Strategy
        self.process_tools = ProcessTools(self.strategy)
        self.file_tools = FileTools()

    def run_tool(self, tool_name: str, **kwargs) -> str:
        """
        The 'Hand' of the Agent. Executes a mapped tool.
        This is what the LLM will call via Function Calling.
        """
        command = None
        
        # Map logical tool names to actual python methods
        if tool_name == "list_processes":
            command = self.process_tools.list_processes_command()
        elif tool_name == "kill_process":
            command = self.process_tools.kill_process_command(kwargs.get("pid"), kwargs.get("force", False))
        elif tool_name == "check_service":
            command = self.strategy.check_service_status(kwargs.get("service"))
        elif tool_name == "restart_service":
            command = self.strategy.restart_service(kwargs.get("service"))
        elif tool_name == "read_log":
            command = self.file_tools.read_file_tail_command(kwargs.get("path"), kwargs.get("lines", 20))
            
        if command:
            return self._exec_ssh(command)
        return "ERROR: Unknown tool."

    def _exec_ssh(self, command: str) -> str:
        print(f"⚡ RUN: {command}")
        stdin, stdout, stderr = self.ssh_client.exec_command(command)
        out = stdout.read().decode()
        err = stderr.read().decode()
        if err and not out: return f"Error: {err}"
        return out
