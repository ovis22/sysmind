from abc import ABC, abstractmethod

class OSStrategy(ABC):
    """
    Abstract interface for OS-specific operations.
    This ensures the Agent is agnostic and can swap strategies at runtime.
    """

    @abstractmethod
    def install_package(self, package_name: str) -> str:
        """Returns command to install a package"""
        pass

    @abstractmethod
    def check_service_status(self, service_name: str) -> str:
        """Returns command to check service status"""
        pass

    @abstractmethod
    def restart_service(self, service_name: str) -> str:
        """Returns command to restart a service"""
        pass

    @abstractmethod
    def get_system_stats_command(self) -> str:
        """Returns the command to get CPU/RAM usage"""
        pass
