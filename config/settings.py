"""
═══════════════════════════════════════════════════════════════════════
CryptoPulse AI Enterprise
Configuration System (Settings Manager)

Responsibilities:
- Load environment variables safely
- Centralized config management
- Type-safe configuration access
═══════════════════════════════════════════════════════════════════════
"""

from dataclasses import dataclass
from typing import Optional
import os


# ==========================================================
# SETTINGS CLASS
# ==========================================================

@dataclass
class Settings:
    """
    Central configuration container
    """

    # =========================
    # CORE
    # =========================
    PROJECT_NAME: str = "CryptoPulse AI"
    DEBUG: bool = False
    TEST_MODE: bool = False
    TIMEZONE: str = "UTC"

    # =========================
    # TELEGRAM
    # =========================
    TELEGRAM_BOT_TOKEN: Optional[str] = None
    ADMIN_IDS: str = ""
    CHANNEL_ID: str = ""

    # =========================
    # AI
    # =========================
    GROQ_API_KEY: Optional[str] = None

    # =========================
    # EXCHANGE (CoinEx)
    # =========================
    COINEX_API_KEY: Optional[str] = None
    COINEX_SECRET_KEY: Optional[str] = None

    # =========================
    # DATABASE
    # =========================
    DATABASE_URL: str = "sqlite:///bot.db"

    # =========================
    # SERVER
    # =========================
    PORT: int = 8080
    WEBHOOK_URL: Optional[str] = None

    # =========================
    # TRADING
    # =========================
    DEFAULT_COIN: str = "BTCUSDT"
    DEFAULT_TIMEFRAME: str = "1h"
    SIGNAL_INTERVAL: int = 60

    # =========================
    # RISK
    # =========================
    MAX_RETRIES: int = 3
    TIMEOUT_SECONDS: int = 30
    MAX_DAILY_LOSS: float = 10.0

    # =========================
    # PERFORMANCE
    # =========================
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60

    # ======================================================
    # LOAD ENV
    # ======================================================

    @classmethod
    def load(cls) -> "Settings":
        """
        Load settings from environment variables
        """

        return cls(
            TELEGRAM_BOT_TOKEN=os.getenv("TELEGRAM_BOT_TOKEN"),
            ADMIN_IDS=os.getenv("ADMIN_IDS", ""),
            CHANNEL_ID=os.getenv("CHANNEL_ID", ""),
            GROQ_API_KEY=os.getenv("GROQ_API_KEY"),
            COINEX_API_KEY=os.getenv("COINEX_API_KEY"),
            COINEX_SECRET_KEY=os.getenv("COINEX_SECRET_KEY"),
            DATABASE_URL=os.getenv("DATABASE_URL", "sqlite:///bot.db"),
            WEBHOOK_URL=os.getenv("WEBHOOK_URL"),
            DEBUG=os.getenv("DEBUG", "False").lower() == "true",
            TEST_MODE=os.getenv("TEST_MODE", "False").lower() == "true",
            TIMEZONE=os.getenv("TIMEZONE", "UTC"),
            PORT=int(os.getenv("PORT", "8080")),
            DEFAULT_COIN=os.getenv("DEFAULT_COIN", "BTCUSDT"),
            DEFAULT_TIMEFRAME=os.getenv("DEFAULT_TIMEFRAME", "1h"),
            SIGNAL_INTERVAL=int(os.getenv("SIGNAL_INTERVAL", "60")),
            MAX_RETRIES=int(os.getenv("MAX_RETRIES", "3")),
            TIMEOUT_SECONDS=int(os.getenv("TIMEOUT_SECONDS", "30")),
            MAX_DAILY_LOSS=float(os.getenv("MAX_DAILY_LOSS", "10.0")),
            RATE_LIMIT_REQUESTS=int(os.getenv("RATE_LIMIT_REQUESTS", "100")),
            RATE_LIMIT_PERIOD=int(os.getenv("RATE_LIMIT_PERIOD", "60")),
        )

    # ======================================================
    # VALIDATION
    # ======================================================

    def validate(self) -> None:
        """
        Validate required configs
        """

        required = [
            self.TELEGRAM_BOT_TOKEN,
            self.COINEX_API_KEY,
            self.COINEX_SECRET_KEY,
        ]

        missing = [r for r in required if not r]

        if missing:
            raise ValueError(
                f"Missing required configuration values: {len(missing)}"
            )
