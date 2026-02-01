class FileTools:
    def read_file_head_command(self, path: str, lines: int = 10) -> str:
        return f"head -n {lines} {path}"

    def read_file_tail_command(self, path: str, lines: int = 10) -> str:
        """
        Crucial for Log Analysis (KTH Syllabus)
        """
        return f"tail -n {lines} {path}"

    def check_disk_space_command(self) -> str:
        return "df -h"

    def list_directory_command(self, path: str) -> str:
        return f"ls -la {path}"
