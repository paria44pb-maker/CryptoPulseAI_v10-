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
        # ============================================================
# CONNECTION MANAGEMENT
# ============================================================

    async def connect(self) -> bool:
        """
        Initialize exchange connection
        """

        self.logger.info("Connecting to CoinEx...")

        try:

            connected = await self.coinex.connect()

            if connected:

                self.logger.info("CoinEx connected successfully")

                return True

            self.logger.error("CoinEx connection failed")

            return False

        except Exception as e:

            self.logger.error(f"Connection error : {e}")

            return False


# ============================================================
# DISCONNECT
# ============================================================

    async def disconnect(self):

        self.logger.info("Disconnecting exchange...")

        try:

            await self.coinex.disconnect()

        except Exception as e:

            self.logger.error(e)


# ============================================================
# RECONNECT
# ============================================================

    async def reconnect(self):

        self.logger.warning("Reconnecting...")

        self.stats.reconnects += 1

        await self.disconnect()

        await asyncio.sleep(3)

        return await self.connect()


# ============================================================
# HEARTBEAT
# ============================================================

    async def heartbeat(self):

        while self.running:

            try:

                latency = await self.coinex.ping()

                self.logger.info(
                    f"Heartbeat OK | latency={latency:.2f} ms"
                )

            except Exception:

                self.logger.warning("Heartbeat failed")

                await self.reconnect()

            await asyncio.sleep(30)


# ============================================================
# MARKET UPDATE
# ============================================================

    async def update_market(self):

        ticker = await self.coinex.get_ticker("BTCUSDT")

        self.market = MarketSnapshot(

            symbol=ticker["symbol"],

            timeframe="1m",

            price=float(ticker["last"]),

            bid=float(ticker["buy"]),

            ask=float(ticker["sell"]),

            volume=float(ticker["vol"]),

            spread=float(ticker["sell"])
            - float(ticker["buy"]),

            timestamp=datetime.utcnow()

        )


# ============================================================
# MARKET WATCHER
# ============================================================

    async def market_watcher(self):

        while self.running:

            try:

                await self.update_market()

            except Exception as e:

                self.logger.error(e)

            await asyncio.sleep(1)


# ============================================================
# CONNECTION MONITOR
# ============================================================

    async def connection_monitor(self):

        while self.running:

            try:

                status = await self.coinex.connection_status()

                if not status:

                    self.logger.warning(
                        "Exchange disconnected"
                    )

                    await self.reconnect()

            except Exception as e:

                self.logger.error(e)

            await asyncio.sleep(10)
            # ============================================================
# SIGNAL ANALYSIS PIPELINE
# ============================================================

    async def analyze_market(self):

        if not self.market:
            return None

        self.logger.info("🧠 Running full market analysis...")

        data = {
            "symbol": self.market.symbol,
            "price": self.market.price,
            "volume": self.market.volume,
            "spread": self.market.spread,
            "timeframe": self.market.timeframe,
            "timestamp": self.market.timestamp.isoformat(),
        }

        # ============================================
        # INDICATORS
        # ============================================

        indicators = await self.state.indicator_engine.run(data)

        # ============================================
        # PRICE ACTION
        # ============================================

        price_action = await self.state.price_action_engine.analyze(data)

        # ============================================
        # SMART MONEY CONCEPTS
        # ============================================

        smc = await self.state.smart_money_engine.analyze(data)

        # ============================================
        # CANDLE PATTERNS
        # ============================================

        candles = await self.state.candlestick_engine.detect(data)

        # ============================================
        # VOLUME ANALYSIS
        # ============================================

        volume = await self.state.volume_engine.analyze(data)

        # ============================================
        # MULTI TIMEFRAME
        # ============================================

        mtf = await self.state.mtf_engine.analyze(data)

        # ============================================
        # AI ANALYSIS
        # ============================================

        ai_analysis = self.signal.generate_signal({
            "market": data,
            "indicators": indicators,
            "price_action": price_action,
            "smc": smc,
            "candles": candles,
            "volume": volume,
            "mtf": mtf,
        })

        # ============================================
        # FINAL RAW SIGNAL PACKAGE
        # ============================================

        signal_package = {
            "market": data,
            "indicators": indicators,
            "price_action": price_action,
            "smart_money": smc,
            "candles": candles,
            "volume": volume,
            "multi_timeframe": mtf,
            "ai": ai_analysis,
        }

        self.stats.total_signals += 1

        self.logger.info(
            f"📊 Analysis completed | Signal: {ai_analysis['signal']} | Confidence: {ai_analysis['confidence']}"
        )

        return signal_package
        # ============================================================
# RISK EVALUATION PIPELINE
# ============================================================

    async def evaluate_risk(self, signal_package: dict):

        self.logger.info("⚠️ Evaluating risk conditions...")

        market = signal_package["market"]
        indicators = signal_package["indicators"]
        smc = signal_package["smart_money"]

        risk_score = 0

        # ============================================
        # VOLATILITY CHECK (ATR-based)
        # ============================================

        atr = indicators.get("atr", 0)

        if atr > 2:
            risk_score += 30
        elif atr > 1:
            risk_score += 15
        else:
            risk_score += 5

        # ============================================
        # TREND STRENGTH
        # ============================================

        adx = indicators.get("adx", 0)

        if adx < 15:
            risk_score += 25  # weak market = risky
        elif adx > 25:
            risk_score -= 10  # strong trend = safer

        # ============================================
        # SPREAD CHECK
        # ============================================

        spread = market["spread"]

        if spread > 0.5:
            risk_score += 20
        elif spread > 0.2:
            risk_score += 10

        # ============================================
        # VOLUME VALIDATION
        # ============================================

        volume = market["volume"]

        if volume < 100:
            risk_score += 20
        elif volume > 1000:
            risk_score -= 10

        # ============================================
        # SMART MONEY FILTER
        # ============================================

        if smc.get("liquidity_sweep"):
            risk_score += 20

        if smc.get("order_block_zone"):
            risk_score -= 10

        # ============================================
        # FINAL RISK DECISION
        # ============================================

        if risk_score >= 60:
            decision = "HIGH_RISK"
        elif risk_score >= 30:
            decision = "MEDIUM_RISK"
        else:
            decision = "LOW_RISK"

        result = {
            "risk_score": risk_score,
            "risk_level": decision,
            "approved": risk_score < 60
        }

        self.logger.info(
            f"🛡 Risk Result: {decision} | Score: {risk_score}"
        )

        return result
        
# ============================================================
# FINAL SIGNAL DECISION ENGINE
# ============================================================

    async def build_final_signal(self, analysis: dict, risk: dict):

        self.logger.info("🧩 Building final decision signal...")

        ai_signal = analysis["ai"]["signal"]
        ai_confidence = analysis["ai"]["confidence"]

        technical_bias = 0

        # ============================================
        # PRICE ACTION BIAS
        # ============================================

        pa = analysis["price_action"]

        if pa.get("trend") == "UP":
            technical_bias += 1
        elif pa.get("trend") == "DOWN":
            technical_bias -= 1

        # ============================================
        # SMART MONEY BIAS
        # ============================================

        smc = analysis["smart_money"]

        if smc.get("bullish_structure"):
            technical_bias += 1

        if smc.get("bearish_structure"):
            technical_bias -= 1

        # ============================================
        # FINAL DECISION LOGIC
        # ============================================

        final_signal = "HOLD"

        if ai_signal == "BUY" and technical_bias > 0:
            final_signal = "BUY"

        elif ai_signal == "SELL" and technical_bias < 0:
            final_signal = "SELL"

        # ============================================
        # CONFIDENCE CALCULATION
        # ============================================

        risk_factor = 1.0

        if risk["risk_level"] == "HIGH_RISK":
            risk_factor = 0.4
        elif risk["risk_level"] == "MEDIUM_RISK":
            risk_factor = 0.7
        else:
            risk_factor = 1.0

        confidence = (
            ai_confidence * 0.6 +
            abs(technical_bias) * 20 +
            (100 - risk["risk_score"]) * 0.2
        ) * risk_factor

        confidence = max(0, min(100, confidence))

        result = {
            "signal": final_signal,
            "confidence": round(confidence, 2),
            "risk_level": risk["risk_level"],
            "technical_bias": technical_bias,
        }

        self.logger.info(
            f"📡 FINAL SIGNAL: {final_signal} | Confidence: {confidence:.2f}"
        )

        return result
        # ============================================================
# POSITION MANAGEMENT LAYER (NO EXECUTION)
# ============================================================

    def update_position(self, signal_result: dict):

        self.logger.info("📌 Updating virtual position state...")

        signal = signal_result["signal"]

        price = self.market.price if self.market else 0

        # ============================================
        # OPEN POSITION (SIMULATION ONLY)
        # ============================================

        if signal == "BUY":

            position = {
                "side": "LONG",
                "entry_price": price,
                "status": "OPEN",
                "time": datetime.utcnow(),
                "confidence": signal_result["confidence"]
            }

            self.state.set("position", position)

        elif signal == "SELL":

            position = {
                "side": "SHORT",
                "entry_price": price,
                "status": "OPEN",
                "time": datetime.utcnow(),
                "confidence": signal_result["confidence"]
            }

            self.state.set("position", position)

        # ============================================
        # CLOSE LOGIC (SIMULATION ONLY)
        # ============================================

        existing = self.state.get("position")

        if existing:

            if signal == "HOLD":

                self.logger.info("⏸ Holding current position")

            else:

                pnl = self.calculate_virtual_pnl(existing, price)

                self.logger.info(
                    f"📊 Virtual PnL: {pnl:.2f}"
                )

                existing["status"] = "CLOSED"
                existing["pnl"] = pnl

                self.state.set("position", None)

    # ============================================================
    # VIRTUAL PNL CALCULATION
    # ============================================================

    def calculate_virtual_pnl(self, position: dict, current_price: float):

        entry = position["entry_price"]

        if position["side"] == "LONG":

            return current_price - entry

        elif position["side"] == "SHORT":

            return entry - current_price

        return 0.0
        # ============================================================
# TELEGRAM REPORTING LAYER
# ============================================================

    async def send_report(self, analysis: dict, signal: dict, risk: dict):

        self.logger.info("📨 Sending Telegram report...")

        market = analysis["market"]

        text = f"""
📊 CryptoPulse AI Report

━━━━━━━━━━━━━━━━━━
💰 Symbol: {market['symbol']}
💵 Price: {market['price']}
📈 Volume: {market['volume']}
📉 Spread: {market['spread']}
━━━━━━━━━━━━━━━━━━

🧠 SIGNAL
→ Direction: {signal['signal']}
→ Confidence: {signal['confidence']}%
→ Technical Bias: {signal['technical_bias']}

⚠️ RISK
→ Level: {risk['risk_level']}
→ Score: {risk['risk_score']}

━━━━━━━━━━━━━━━━━━
📡 AI STATUS: ACTIVE
🕒 {market['timestamp']}
"""

        try:

            await self.telegram.send_message(text)

        except Exception as e:

            self.logger.error(f"Telegram error: {e}")


# ============================================================
# ALERT SYSTEM
# ============================================================

    async def send_alert(self, message: str, level: str = "INFO"):

        icon = "ℹ️"

        if level == "WARNING":
            icon = "⚠️"
        elif level == "ERROR":
            icon = "❌"
        elif level == "SUCCESS":
            icon = "✅"

        text = f"{icon} {message}"

        try:

            await self.telegram.send_message(text)

        except Exception as e:

            self.logger.error(e)


# ============================================================
# POSITION REPORT
# ============================================================

    async def send_position_report(self):

        position = self.state.get("position")

        if not position:
            return

        text = f"""
📌 Position Report

━━━━━━━━━━━━━━
Side: {position.get('side')}
Entry: {position.get('entry_price')}
Status: {position.get('status')}
Confidence: {position.get('confidence')}
━━━━━━━━━━━━━━
"""

        await self.telegram.send_message(text)
        # ============================================================
# HEALTH MONITOR SYSTEM
# ============================================================

    async def health_check(self):

        self.logger.info("🩺 Running system health check...")

        health = {
            "cpu": self.get_cpu_usage(),
            "ram": self.get_ram_usage(),
            "api": await self.coinex.connection_status(),
            "time": datetime.utcnow().isoformat()
        }

        self.logger.info(f"🖥 Health: {health}")

        return health


# ============================================================
# CPU USAGE
# ============================================================

    def get_cpu_usage(self):

        try:
            import psutil
            return psutil.cpu_percent(interval=1)
        except:
            return 0


# ============================================================
# RAM USAGE
# ============================================================

    def get_ram_usage(self):

        try:
            import psutil
            return psutil.virtual_memory().percent
        except:
            return 0


# ============================================================
# AUTO RECOVERY SYSTEM
# ============================================================

    async def auto_recover(self, error: Exception):

        self.logger.error(f"⚠️ System error detected: {error}")

        self.stats.api_errors += 1

        await self.send_alert(
            f"System error detected: {str(error)}",
            level="ERROR"
        )

        try:

            self.logger.info("♻️ Attempting recovery...")

            await self.reconnect()

            await asyncio.sleep(2)

            self.logger.info("✅ Recovery successful")

            await self.send_alert(
                "System recovered successfully",
                level="SUCCESS"
            )

        except Exception as e:

            self.logger.error(f"❌ Recovery failed: {e}")

            await self.send_alert(
                "CRITICAL: System recovery failed",
                level="ERROR"
            )


# ============================================================
# SAFE EXECUTION WRAPPER
# ============================================================

    async def safe_run(self, coro):

        try:

            return await coro

        except Exception as e:

            await self.auto_recover(e)

            return None
            # ============================================================
# MAIN RUNTIME LOOP
# ============================================================

    async def run(self):

        self.logger.info("🚀 LiveTrader started")

        self.running = True

        # اتصال اولیه
        await self.connect()

        # استارت بک‌گراند مانیتورینگ
        asyncio.create_task(self.market_watcher())
        asyncio.create_task(self.connection_monitor())
        asyncio.create_task(self.heartbeat())

        last_health_check = time.time()

        # =====================================================
        # MAIN LOOP
        # =====================================================

        while self.running:

            try:

                # --------------------------------------------
                # 1. MARKET ANALYSIS
                # --------------------------------------------

                analysis = await self.analyze_market()

                if not analysis:
                    await asyncio.sleep(1)
                    continue

                # --------------------------------------------
                # 2. RISK EVALUATION
                # --------------------------------------------

                risk = await self.evaluate_risk(analysis)

                # اگر ریسک خیلی بالا باشد → رد کن
                if not risk["approved"]:

                    await self.send_alert(
                        "Signal rejected due to high risk",
                        level="WARNING"
                    )

                    await asyncio.sleep(2)
                    continue

                # --------------------------------------------
                # 3. SIGNAL DECISION
                # --------------------------------------------

                signal = await self.build_final_signal(
                    analysis,
                    risk
                )

                # --------------------------------------------
                # 4. POSITION UPDATE (VIRTUAL ONLY)
                # --------------------------------------------

                self.update_position(signal)

                # --------------------------------------------
                # 5. TELEGRAM REPORT
                # --------------------------------------------

                await self.send_report(
                    analysis,
                    signal,
                    risk
                )

                # --------------------------------------------
                # 6. HEALTH CHECK (EVERY 60s)
                # --------------------------------------------

                if time.time() - last_health_check > 60:

                    await self.health_check()

                    last_health_check = time.time()

                # --------------------------------------------
                # 7. STATS UPDATE
                # --------------------------------------------

                self.stats.runtime_seconds = time.time() - self.started_at

                # --------------------------------------------
                # 8. LOOP DELAY
                # --------------------------------------------

                await asyncio.sleep(self.loop_delay)

            except Exception as e:

                await self.auto_recover(e)

                await asyncio.sleep(2)


# ============================================================
# STOP SYSTEM
# ============================================================

    async def stop(self):

        self.logger.info("🛑 Stopping LiveTrader...")

        self.running = False

        await self.disconnect()

        await self.send_alert(
            "LiveTrader stopped safely",
            level="INFO"
        )
        
