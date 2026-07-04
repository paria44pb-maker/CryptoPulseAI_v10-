"""
═══════════════════════════════════════════════════════════════════════
CryptoPulse AI Enterprise
Core Logger System

Features:
- Structured logging
- Console + File output
- Daily log rotation
- Error tracking support
- Production-ready design
═══════════════════════════════════════════════════════════════════════
"""

import logging
import os
from datetime import datetime
from pathlib import Path

from core.constants import LOG_DIR, LOG_FORMAT, LOG_DATE_FORMAT


# ==========================================================
# LOGGER MANAGER
# ==========================================================

class LoggerManager:
    """
    Central logging system for entire project
    """

    _loggers: dict[str, logging.Logger] = {}

    @staticmethod
    def get_logger(name: str = "CryptoPulseAI") -> logging.Logger:
        """
        Returns a configured logger instance.
        """

        if name in LoggerManager._loggers:
            return LoggerManager._loggers[name]

        logger = logging.getLogger(name)
        logger.setLevel(logging.INFO)

        # Avoid duplicate handlers
        if not logger.handlers:

            # Ensure log directory exists
            Path(LOG_DIR).mkdir(parents=True, exist_ok=True)

            # =========================
            # FILE HANDLER
            # =========================
            log_file = LOG_DIR / f"{name}_{datetime.utcnow().date()}.log"

            file_handler = logging.FileHandler(log_file, encoding="utf-8")
            file_handler.setLevel(logging.INFO)

            file_formatter = logging.Formatter(
                LOG_FORMAT,
                datefmt=LOG_DATE_FORMAT
            )

            file_handler.setFormatter(file_formatter)

            # =========================
            # CONSOLE HANDLER
            # =========================
            console_handler = logging.StreamHandler()
            console_handler.setLevel(logging.INFO)

            console_formatter = logging.Formatter(
                LOG_FORMAT,
                datefmt=LOG_DATE_FORMAT
            )

            console_handler.setFormatter(console_formatter)

            # =========================
            # ATTACH HANDLERS
            # =========================
            logger.addHandler(file_handler)
            logger.addHandler(console_handler)

        LoggerManager._loggers[name] = logger

        return logger


# ==========================================================
# SIMPLE LOGGER WRAPPER
# ==========================================================

class Logger:
    """
    Simple wrapper for easy use across project
    """

    def __init__(self, name: str = "CryptoPulseAI"):
        self.logger = LoggerManager.get_logger(name)

    def info(self, message: str):
        self.logger.info(message)

    def warning(self, message: str):
        self.logger.warning(message)

    def error(self, message: str):
        self.logger.error(message)

    def debug(self, message: str):
        self.logger.debug(message)


# ==========================================================
# LOG UTILITY FUNCTIONS
# ==========================================================

def get_logger(name: str = "CryptoPulseAI") -> logging.Logger:
    """
    Quick access function for logger
    """
    return LoggerManager.get_logger(name)
