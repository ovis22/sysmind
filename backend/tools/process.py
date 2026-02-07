from typing import List, Dict
from ..strategies.base import OSStrategy

class ProcessTools:
    def __init__(self, strategy: OSStrategy):
        self.strategy = strategy

    def list_processes_command(self) -> str:
        """
        Returns command to list top resource-consuming processes.
        Updated for CPU-heavy scenarios (Grand Prize Demo Optimization).
        """
        # Changed to %cpu because the demo involves a CPU stress test!
        return "ps aux --sort=-%cpu | head -n 15"

    def kill_process_command(self, pid: int, force: bool = False) -> str:
        """
        Returns command to kill a process.
        Safe wrapper around kill with Shell Injection Protection.
        """
        import shlex
        sig = "-9" if force else "-15"
        # Force string conversion and quote to prevent any edge-case injection
        safe_pid = shlex.quote(str(pid))
        return f"kill {sig} {safe_pid}"

    def get_process_details_command(self, pid: int) -> str:
        """
        Deep inspection of a process (Aalto OS Syllabus: /proc analysis)
        """
        import shlex
        # Safety first: sanitize input here too
        safe_pid = shlex.quote(str(pid))
        return f"cat /proc/{safe_pid}/status"
