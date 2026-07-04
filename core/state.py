"""
═══════════════════════════════════════════════════════════════════════
CryptoPulse AI Enterprise
Core State Manager

Responsibilities:
- Track system state in real-time
- Provide safe state transitions
- Centralized status control
═══════════════════════════════════════════════════════════════════════
"""

from threading import Lock

from core.constants import AppState
from core.logger import Logger


# ==========================================================
# STATE MANAGER
# ==========================================================

class StateManager:
    """
    Thread-safe system state controller
    """

    def __init__(self):
        self.logger = Logger("StateManager")
        self._lock = Lock()
        self._state: AppState = AppState.STARTING

    # ======================================================
    # GET STATE
    # ======================================================

    def get_state(self) -> AppState:
        return self._state

    def is_running(self) -> bool:
        return self._state == AppState.RUNNING

    def is_healthy(self) -> bool:
        return self._state in [
            AppState.RUNNING,
            AppState.INITIALIZING
        ]

    # ======================================================
    # SET STATE (SAFE)
    # ======================================================

    def set_state(self, new_state: AppState) -> None:
        """
        Safe state transition
        """

        with self._lock:

            if self._state == new_state:
                return

            self.logger.info(
                f"🔄 State change: {self._state.value} → {new_state.value}"
            )

            self._state = new_state

    # ======================================================
    # FORCE STATE (DANGEROUS)
    # ======================================================

    def force_state(self, new_state: AppState) -> None:
        """
        Force state change (use only in emergency)
        """

        self.logger.warning(
            f"⚠️ FORCE STATE CHANGE: {self._state.value} → {new_state.value}"
        )

        self._state = new_state
