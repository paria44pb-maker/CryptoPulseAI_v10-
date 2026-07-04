"""
═══════════════════════════════════════════════════════════════════════
CryptoPulse AI Enterprise
Core Lifecycle Manager

Responsibilities:
- System startup orchestration
- Graceful shutdown
- Restart handling
- State transitions
═══════════════════════════════════════════════════════════════════════
"""

import asyncio
from typing import Callable, Optional

from core.constants import AppState
from core.logger import Logger
from core.registry import ServiceRegistry


# ==========================================================
# LIFECYCLE MANAGER
# ==========================================================

class LifecycleManager:
    """
    Controls full lifecycle of the application
    """

    def __init__(self):
        self.logger = Logger("Lifecycle")
        self.state: AppState = AppState.STARTING

        self._on_startup_hooks: list[Callable] = []
        self._on_shutdown_hooks: list[Callable] = []
        self._on_restart_hooks: list[Callable] = []

    # ======================================================
    # HOOK REGISTRATION
    # ======================================================

    def on_startup(self, func: Callable):
        self._on_startup_hooks.append(func)

    def on_shutdown(self, func: Callable):
        self._on_shutdown_hooks.append(func)

    def on_restart(self, func: Callable):
        self._on_restart_hooks.append(func)

    # ======================================================
    # STARTUP
    # ======================================================

    async def startup(self):
        self.logger.info("🚀 System starting up...")
        self.state = AppState.INITIALIZING

        try:
            for hook in self._on_startup_hooks:
                result = hook()
                if asyncio.iscoroutine(result):
                    await result

            self.state = AppState.RUNNING
            self.logger.info("✅ System is now RUNNING")

        except Exception as e:
            self.state = AppState.CRASHED
            self.logger.error(f"❌ Startup failed: {e}")
            raise

    # ======================================================
    # SHUTDOWN
    # ======================================================

    async def shutdown(self):
        self.logger.info("🛑 System shutting down...")
        self.state = AppState.STOPPING

        try:
            for hook in self._on_shutdown_hooks:
                result = hook()
                if asyncio.iscoroutine(result):
                    await result

            self.state = AppState.STOPPED
            self.logger.info("✅ System stopped cleanly")

        except Exception as e:
            self.logger.error(f"❌ Shutdown error: {e}")
            self.state = AppState.CRASHED
            raise

    # ======================================================
    # RESTART
    # ======================================================

    async def restart(self):
        self.logger.warning("🔄 System restarting...")

        try:
            for hook in self._on_restart_hooks:
                result = hook()
                if asyncio.iscoroutine(result):
                    await result

            await self.shutdown()
            await asyncio.sleep(1)
            await self.startup()

            self.logger.info("♻️ Restart completed")

        except Exception as e:
            self.logger.error(f"❌ Restart failed: {e}")
            self.state = AppState.CRASHED
            raise

    # ======================================================
    # STATE CHECK
    # ======================================================

    def get_state(self) -> AppState:
        return self.state

    def is_running(self) -> bool:
        return self.state == AppState.RUNNING
