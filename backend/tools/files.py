class FileTools:
    """
    Titanium File Diagnostics & Reporting Tools.
    """
    def get_read_command(self, path: str, lines: int = 10) -> str:
        return f"tail -n {lines} {path}"

    def get_grep_command(self, pattern: str, path: str) -> str:
        """Smart grep with context (2 lines before/after)."""
        # Escape pattern to prevent shell injection
        safe_pattern = pattern.replace('"', '\\"')
        return f"grep -nC 2 \"{safe_pattern}\" {path}"

    def get_list_command(self, path: str = "/") -> str:
        return f"ls -F {path}"
        
    def get_write_command(self, path: str, content: str) -> str:
        """Writes content to a file (for reports)."""
        clean_content = content.replace("'", "'\\''")
        return f"printf '{clean_content}' > {path}"

    def check_disk_space_command(self) -> str:
        return "df -h"
