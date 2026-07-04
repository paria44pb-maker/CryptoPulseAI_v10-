"""
═══════════════════════════════════════════════════════════════════════
CryptoPulse AI Enterprise

Live Trader Engine

Version : 10.0
Python  : 3.11+

Enterprise Edition

Responsibilities

- Live Trading
- Position Management
- Risk Validation
- Execution Control
- CoinEx Integration
- AI Integration
- Telegram Notifications
- Database Logging
- Health Monitoring
- Auto Recovery

═══════════════════════════════════════════════════════════════════════
"""

from __future__ import annotations

import asyncio
import time
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

from core.logger import Logger
from core.state import StateManager
from core.registry import ServiceRegistry

from signals.signal_engine import SignalEngine

from engine.execution_engine import ExecutionEngine
from engine.position_manager import PositionManager
from engine.risk_manager import RiskManager

from coinex.engine import CoinExEngine

from telegram.bot_handler import TelegramBot

from database.engine import DatabaseEngine


# ============================================================
# MARKET SNAPSHOT
# ============================================================

@dataclass(slots=True)
class MarketSnapshot:

    symbol: str

    timeframe: str

    price: float

    bid: float

    ask: float

    volume: float

    spread: float

    timestamp: datetime


# ============================================================
# TRADE RESULT
# ============================================================

@dataclass(slots=True)
class TradeResult:

    success: bool

    order_id: Optional[str] = None

    message: str = ""

    pnl: float = 0.0

    execution_time: float = 0.0


# ============================================================
# TRADER STATS
# ============================================================

@dataclass
class TraderStatistics:

    total_signals: int = 0

    executed_orders: int = 0

    rejected_orders: int = 0

    winning_trades: int = 0

    losing_trades: int = 0

    reconnects: int = 0

    api_errors: int = 0

    runtime_seconds: float = 0


# ============================================================
# LIVE TRADER
# ============================================================

class LiveTrader:

    """
    Enterprise Live Trading Engine
    """

    def __init__(self):

        self.logger = Logger("LiveTrader")

        self.state = StateManager()

        self.signal = SignalEngine()

        self.coinex = CoinExEngine()

        self.execution = ExecutionEngine()

        self.position = PositionManager()

        self.risk = RiskManager()

        self.telegram = TelegramBot()

        self.database = DatabaseEngine()

        self.running = False

        self.stats = TraderStatistics()

        self.market: Optional[MarketSnapshot] = None

        self.started_at = time.time()

        self.loop_delay = 1

        self.lock = asyncio.Lock()

        ServiceRegistry.register("live_trader", self)

        self.logger.info("✅ LiveTrader initialized")
