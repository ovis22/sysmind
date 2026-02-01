from typing import List, Dict
from ..strategies.base import OSStrategy

class ProcessTools:
    def __init__(self, strategy: OSStrategy):
        self.strategy = strategy

    def list_processes_command(self) -> str:
        """
        Returns command to list top resource-consuming processes.
        """
        # Using generic PS/TOP, but strategy could override if needed
        return "ps aux --sort=-%mem | head -n 10"

    def kill_process_command(self, pid: int, force: bool = False) -> str:
        """
        Returns command to kill a process.
        Safe wrapper around kill.
        """
        sig = "-9" if force else "-15"
        return f"kill {sig} {pid}"

    def get_process_details_command(self, pid: int) -> str:
        """
        Deep inspection of a process (Aalto OS Syllabus: /proc analysis)
        """
        return f"cat /proc/{pid}/status"
