import shlex

class FileTools:
    """
    Titanium File Diagnostics & Reporting Tools.
    """
    def get_read_command(self, path: str, lines: int = None) -> str:
        """
        Read log file with optional line limit.
        
        Args:
            path: Path to file
            lines: Number of lines to read from end. If None, reads ENTIRE file.
                   This leverages Gemini 3's massive context window (1M+ tokens).
        """
        safe_path = shlex.quote(path)
        if lines is None:
            # LONG CONTEXT SHOWCASE: Read entire file for Gemini 3
            return f"cat {safe_path}"
        return f"tail -n {lines} {safe_path}"

    def get_grep_command(self, pattern: str, path: str) -> str:
        """Smart grep with context (2 lines before/after)."""
        # Using shlex.quote to prevent shell injection (Grand Prize Hardening)
        safe_pattern = shlex.quote(pattern)
        safe_path = shlex.quote(path)
        return f"grep -nC 2 {safe_pattern} {safe_path}"

    def get_list_command(self, path: str = "/") -> str:
        safe_path = shlex.quote(path)
        return f"ls -F {safe_path}"
        
    def get_write_command(self, path: str, content: str) -> str:
        """Writes content to a file safely."""
        safe_content = shlex.quote(content)
        safe_path = shlex.quote(path)
        return f"printf %s {safe_content} > {safe_path}"

    def check_disk_space_command(self) -> str:
        return "df -h"
