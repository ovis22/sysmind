class ServiceTools:
    """
    Standardized Systemd Service Management (Titanium Edition).
    """
    def get_status_command(self, service_name: str) -> str:
        """Checks if a service is active."""
        return f"systemctl status {service_name} --no-pager"

    def get_restart_command(self, service_name: str) -> str:
        """Restarts a service politely."""
        return f"sudo systemctl restart {service_name}"
