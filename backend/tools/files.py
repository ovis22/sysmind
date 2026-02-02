import shlex

class FileTools:
    """
    Titanium File Diagnostics & Reporting Tools.
    """
    def get_read_command(self, path: str, lines: int = 10) -> str:
        return f"tail -n {lines} {path}"

    def get_grep_command(self, pattern: str, path: str) -> str:
        """Smart grep with context (2 lines before/after)."""
        # Using shlex.quote to prevent shell injection (Grand Prize Hardening)
        safe_pattern = shlex.quote(pattern)
        safe_path = shlex.quote(path)
        return f"grep -nC 2 {safe_pattern} {safe_path}"

    def get_list_command(self, path: str = "/") -> str:
        return f"ls -F {path}"
        
    def get_write_command(self, path: str, content: str) -> str:
        """Writes content to a file safely."""
        safe_content = shlex.quote(content)
        safe_path = shlex.quote(path)
        return f"printf %s {safe_content} > {safe_path}"

    def check_disk_space_command(self) -> str:
        return "df -h"
