class FileTools:
    def get_read_command(self, path: str, lines: int = 10) -> str:
        """
        Standardized log reading command.
        """
        return f"tail -n {lines} {path}"

    def get_list_command(self, path: str = "/") -> str:
        """
        Standardized directory listing.
        """
        return f"ls -F {path}"

    def check_disk_space_command(self) -> str:
        return "df -h"
