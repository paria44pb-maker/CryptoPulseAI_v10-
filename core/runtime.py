"""
═══════════════════════════════════════════════════════════════════════
CryptoPulse AI Enterprise
Core Runtime Engine

Responsibilities:
- Async event loop management
- Background task handling
- System lifecycle integration
- Graceful task shutdown
═══════════════════════════════════════════════════════════════════════
"""

import asyncio
from typing import Callable, List, Optional

from core.logger import Logger
from core.lifecycle import LifecycleManager


# ==========================================================
# TASK MANAGER
# ==========================================================

class TaskManager:
    """
    Manages all background async tasks
    """

    def __init__(self):
        self.logger = Logger("TaskManager")
        self.tasks: List[asyncio.Task] = []

    def create_task(self, coro) -> asyncio.Task:
        """
        Create and track async task
        """
        task = asyncio.create_task(coro)
        self.tasks.append(task)
        return task

    async def cancel_all(self):
        """
        Cancel all running tasks gracefully
        """
        self.logger.warning("🧹 Cancelling all tasks...")

        for task in self.tasks:
            if not task.done():
                task.cancel()

        await asyncio.gather(*self.tasks, return_exceptions=True)

        self.logger.info("✅ All tasks cancelled")


# ==========================================================
# RUNTIME ENGINE
# ==========================================================

class RuntimeEngine:
    """
    Core runtime controller of entire system
    """

    def __init__(self):
        self.logger = Logger("Runtime")
        self.lifecycle = LifecycleManager()
        self.task_manager = TaskManager()

        self._main_loop_running = False

    # ======================================================
    # REGISTER HOOKS
    # ======================================================

    def on_startup(self, func: Callable):
        self.lifecycle.on_startup(func)

    def on_shutdown(self, func: Callable):
        self.lifecycle.on_shutdown(func)

    def on_restart(self, func: Callable):
        self.lifecycle.on_restart(func)

    # ======================================================
    # RUN SYSTEM
    # ======================================================

    async def run(self):
        """
        Start full system runtime
        """
        self.logger.info("🚀 Runtime starting...")

        await self.lifecycle.startup()

        self._main_loop_running = True

        try:
            while self._main_loop_running:

                # Main heartbeat
                self.logger.info("💓 System heartbeat")

                await asyncio.sleep(5)

        except asyncio.CancelledError:
            self.logger.warning("⚠️ Runtime cancelled")

        except Exception as e:
            self.logger.error(f"❌ Runtime error: {e}")
            raise

        finally:
            await self.shutdown()

    # ======================================================
    # STOP SYSTEM
    # ======================================================

    async def shutdown(self):
        """
        Shutdown runtime safely
        """
        self.logger.warning("🛑 Runtime shutting down...")

        self._main_loop_running = False

        await self.lifecycle.shutdown()
        await self.task_manager.cancel_all()

        self.logger.info("✅ Runtime stopped cleanly")

    # ======================================================
    # RESTART SYSTEM
    # ======================================================

    async def restart(self):
        """
        Restart full system
        """
        self.logger.warning("🔄 Runtime restarting...")

        await self.lifecycle.restart()

    # ======================================================
    # CREATE BACKGROUND TASK
    # ======================================================

    def create_task(self, coro) -> asyncio.Task:
        """
        Shortcut to task manager
        """
        return self.task_manager.create_task(coro)
