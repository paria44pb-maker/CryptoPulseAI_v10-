"""
═══════════════════════════════════════════════════════════════════════
CryptoPulse AI Enterprise
Core Exceptions

Centralized exception system for the entire platform.
Helps with debugging, logging, and system stability.
═══════════════════════════════════════════════════════════════════════
"""


# ==========================================================
# BASE EXCEPTION
# ==========================================================

class CryptoPulseError(Exception):
    """
    Base exception for all project errors.
    """
    def __init__(self, message: str, code: str | None = None):
        super().__init__(message)
        self.message = message
        self.code = code

    def __str__(self):
        if self.code:
            return f"[{self.code}] {self.message}"
        return self.message


# ==========================================================
# CONFIG ERRORS
# ==========================================================

class ConfigError(CryptoPulseError):
    """Raised when configuration is invalid or missing."""


class MissingEnvironmentVariable(ConfigError):
    """Required environment variable is missing."""


# ==========================================================
# MARKET ERRORS
# ==========================================================

class MarketDataError(CryptoPulseError):
    """Raised when market data fetch fails."""


class InvalidSymbolError(MarketDataError):
    """Symbol is not supported or invalid."""


class DataFeedDisconnected(MarketDataError):
    """WebSocket or data feed is disconnected."""


# ==========================================================
# EXCHANGE ERRORS
# ==========================================================

class ExchangeError(CryptoPulseError):
    """Base exchange error."""


class OrderPlacementError(ExchangeError):
    """Failed to place order."""


class OrderCancelError(ExchangeError):
    """Failed to cancel order."""


class InsufficientBalanceError(ExchangeError):
    """Not enough balance to execute trade."""


# ==========================================================
# AI / ANALYSIS ERRORS
# ==========================================================

class AIEngineError(CryptoPulseError):
    """AI engine failure."""


class IndicatorCalculationError(CryptoPulseError):
    """Technical indicator calculation failed."""


class SignalGenerationError(CryptoPulseError):
    """Failed to generate trading signal."""


# ==========================================================
# RISK ERRORS
# ==========================================================

class RiskViolationError(CryptoPulseError):
    """Trade violates risk management rules."""


class MaxDrawdownExceeded(RiskViolationError):
    """Maximum allowed drawdown exceeded."""


class PositionLimitExceeded(RiskViolationError):
    """Too many open positions."""


# ==========================================================
# TELEGRAM ERRORS
# ==========================================================

class TelegramError(CryptoPulseError):
    """Telegram API error."""


class MessageTooLong(TelegramError):
    """Telegram message exceeds allowed limit."""


# ==========================================================
# SYSTEM ERRORS
# ==========================================================

class SystemShutdown(CryptoPulseError):
    """System is shutting down."""


class ServiceUnavailable(CryptoPulseError):
    """Required service is not available."""
