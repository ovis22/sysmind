from .base import OSStrategy

class UbuntuStrategy(OSStrategy):
    """
    Implementation for Debian/Ubuntu systems.
    Uses: apt-get, systemctl, /proc
    """

    def install_package(self, package_name: str) -> str:
        # Non-interactive installation
        return f"DEBIAN_FRONTEND=noninteractive apt-get install -y {package_name}"

    def check_service_status(self, service_name: str) -> str:
        return f"systemctl is-active {service_name}"

    def restart_service(self, service_name: str) -> str:
        return f"systemctl restart {service_name}"

    def get_system_stats_command(self) -> str:
        # One-liner to get CPU and RAM usage
        return "top -b -n 1 | head -n 5"
