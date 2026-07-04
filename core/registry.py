"""
═══════════════════════════════════════════════════════════════════════
CryptoPulse AI Enterprise
Core Registry (Dependency Injection System)

Purpose:
- Central service container
- Manage global instances
- Avoid tight coupling between modules
═══════════════════════════════════════════════════════════════════════
"""

from typing import Any, Dict, Optional


# ==========================================================
# SERVICE REGISTRY
# ==========================================================

class ServiceRegistry:
    """
    Global service container for all system components
    """

    _services: Dict[str, Any] = {}

    # =========================
    # REGISTER SERVICE
    # =========================
    @staticmethod
    def register(name: str, service: Any) -> None:
        """
        Register a service in the container
        """
        ServiceRegistry._services[name] = service

    # =========================
    # GET SERVICE
    # =========================
    @staticmethod
    def get(name: str) -> Optional[Any]:
        """
        Retrieve a registered service
        """
        return ServiceRegistry._services.get(name)

    # =========================
    # CHECK SERVICE
    # =========================
    @staticmethod
    def has(name: str) -> bool:
        """
        Check if service exists
        """
        return name in ServiceRegistry._services

    # =========================
    # REMOVE SERVICE
    # =========================
    @staticmethod
    def remove(name: str) -> None:
        """
        Remove a service from registry
        """
        if name in ServiceRegistry._services:
            del ServiceRegistry._services[name]

    # =========================
    # CLEAR ALL
    # =========================
    @staticmethod
    def clear() -> None:
        """
        Clear all services (used in restart/shutdown)
        """
        ServiceRegistry._services.clear()

    # =========================
    # LIST SERVICES
    # =========================
    @staticmethod
    def all() -> Dict[str, Any]:
        """
        Return all registered services
        """
        return ServiceRegistry._services.copy()
