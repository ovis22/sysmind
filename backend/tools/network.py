class NetworkTools:
    """
    Network Diagnostics (The Titanium Port Scanner).
    """
    def get_active_ports_command(self) -> str:
        """Lists listening ports (TCP/UDP) to detect rogue services."""
        return "ss -tuln"
