"""
═══════════════════════════════════════════════════════════════════════
CryptoPulse AI Enterprise
Signal Engine

Responsibilities:
- Combine AI + Technical indicators
- Generate final trading signal
- Compute confidence score
═══════════════════════════════════════════════════════════════════════
"""

from typing import Dict, Any

from core.logger import Logger
from core.constants import SignalType
from ai.base_engine import AIBaseEngine


# ==========================================================
# SIGNAL ENGINE
# ==========================================================

class SignalEngine:
    """
    Core decision-making engine for trading signals
    """

    def __init__(self, ai_engine: AIBaseEngine):
        self.logger = Logger("SignalEngine")
        self.ai = ai_engine

    # ======================================================
    # MAIN SIGNAL GENERATION
    # ======================================================

    def generate_signal(self, market_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate final trading signal
        """

        self.logger.info("📊 Generating trading signal...")

        # =========================
        # STEP 1 - AI ANALYSIS
        # =========================
        ai_result = self.ai.generate(
            message="Analyze market and give trading decision",
            context=market_data
        )

        ai_signal = ai_result.get("signal", "HOLD")
        confidence = ai_result.get("confidence", 0.0)

        # =========================
        # STEP 2 - TECHNICAL FILTER
        # =========================
        technical_score = self._technical_filter(market_data)

        # =========================
        # STEP 3 - FINAL DECISION
        # =========================
        final_signal = self._combine_signals(ai_signal, technical_score)

        # =========================
        # STEP 4 - CONFIDENCE SCORING
        # =========================
        final_confidence = self._calculate_confidence(
            confidence,
            technical_score
        )

        result = {
            "signal": final_signal,
            "ai_signal": ai_signal,
            "technical_score": technical_score,
            "confidence": final_confidence,
        }

        self.logger.info(
            f"📡 Signal: {final_signal} | Confidence: {final_confidence:.2f}"
        )

        return result

    # ======================================================
    # TECHNICAL FILTER
    # ======================================================

    def _technical_filter(self, data: Dict[str, Any]) -> float:
        """
        Simplified technical analysis score
        (will expand in indicators/ module)
        """

        price_change = data.get("price_change", 0)

        if price_change > 2:
            return 0.8
        elif price_change < -2:
            return -0.8

        return 0.0

    # ======================================================
    # SIGNAL COMBINATION
    # ======================================================

    def _combine_signals(self, ai_signal: str, technical_score: float) -> str:
        """
        Merge AI + technical analysis
        """

        if ai_signal == "BUY" and technical_score >= 0:
            return SignalType.BUY

        if ai_signal == "SELL" and technical_score <= 0:
            return SignalType.SELL

        return SignalType.HOLD

    # ======================================================
    # CONFIDENCE ENGINE
    # ======================================================

    def _calculate_confidence(
        self,
        ai_conf: float,
        tech_score: float
    ) -> float:
        """
        Weighted confidence calculation
        """

        return round((ai_conf * 0.7) + (abs(tech_score) * 30), 2)
