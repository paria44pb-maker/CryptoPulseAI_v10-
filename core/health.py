"""
═══════════════════════════════════════════════════════════════════════
CryptoPulse AI Enterprise
Core Health Monitor

Responsibilities:
- System resource monitoring
- Service health checks
- Runtime diagnostics
═══════════════════════════════════════════════════════════════════════
"""

import time
import platform
import psutil
from dataclasses import dataclass

from core.constants import HealthStatus
from core.logger import Logger
from core.registry import ServiceRegistry


# ==========================================================
# HEALTH DATA MODEL
# ==========================================================

@dataclass
class SystemHealth:
    cpu_usage: float
    memory_usage: float
    disk_usage: float
    uptime: float
    status: HealthStatus


# ==========================================================
# HEALTH MONITOR
# ==========================================================

class HealthMonitor:
    """
    Monitors system health in real-time
    """

    def __init__(self):
        self.logger = Logger("HealthMonitor")
        self._start_time = time.time()

    # ======================================================
    # BASIC SYSTEM INFO
    # ======================================================

    def get_system_info(self) -> dict:
        return {
            "os": platform.system(),
            "os_version": platform.version(),
            "python_version": platform.python_version(),
            "machine": platform.machine(),
        }

    # ======================================================
    # RESOURCE USAGE
    # ======================================================

    def get_cpu_usage(self) -> float:
        return psutil.cpu_percent(interval=1)

    def get_memory_usage(self) -> float:
        return psutil.virtual_memory().percent

    def get_disk_usage(self) -> float:
        return psutil.disk_usage("/").percent

    # ======================================================
    # UPTIME
    # ======================================================

    def get_uptime(self) -> float:
        return time.time() - self._start_time

    # ======================================================
    # SERVICE HEALTH CHECK
    # ======================================================

    def check_services(self) -> dict:
        services_status = {}

        services = ServiceRegistry.all()

        for name, service in services.items():
            try:
                # اگر سرویس متد health داشته باشد
                if hasattr(service, "health"):
                    services_status[name] = service.health()
                else:
                    services_status[name] = "unknown"

            except Exception as e:
                services_status[name] = f"error: {str(e)}"

        return services_status

    # ======================================================
    # FULL HEALTH REPORT
    # ======================================================

    def get_health(self) -> SystemHealth:

        cpu = self.get_cpu_usage()
        memory = self.get_memory_usage()
        disk = self.get_disk_usage()

        # تعیین وضعیت کلی
        if cpu > 85 or memory > 85 or disk > 90:
            status = HealthStatus.CRITICAL
        elif cpu > 70 or memory > 70:
            status = HealthStatus.WARNING
        else:
            status = HealthStatus.HEALTHY

        return SystemHealth(
            cpu_usage=cpu,
            memory_usage=memory,
            disk_usage=disk,
            uptime=self.get_uptime(),
            status=status
        )

    # ======================================================
    # LOG HEALTH
    # ======================================================

    def log_health(self):
        health = self.get_health()

        self.logger.info(
            f"🩺 CPU:{health.cpu_usage:.1f}% | "
            f"RAM:{health.memory_usage:.1f}% | "
            f"DISK:{health.disk_usage:.1f}% | "
            f"STATUS:{health.status.value}"
        )
