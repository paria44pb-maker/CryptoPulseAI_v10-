"""
═══════════════════════════════════════════════════════════════════════
CryptoPulse AI Enterprise
AI Base Engine

Responsibilities:
- Core AI interface
- Prompt handling
- Response generation layer
- Ready for Groq / LLM integration
═══════════════════════════════════════════════════════════════════════
"""

from typing import Optional, Dict, Any

from core.logger import Logger
from config.settings import Settings


# ==========================================================
# AI BASE ENGINE
# ==========================================================

class AIBaseEngine:
    """
    Base class for all AI engines (Groq, OpenAI, etc.)
    """

    def __init__(self, settings: Settings):
        self.settings = settings
        self.logger = Logger("AIEngine")

    # ======================================================
    # BUILD PROMPT
    # ======================================================

    def build_prompt(self, message: str, context: Optional[Dict[str, Any]] = None) -> str:
        """
        Construct structured prompt
        """

        base_prompt = (
            "You are CryptoPulse AI, a professional trading assistant.\n"
            "You analyze crypto markets using technical indicators, price action, and risk management.\n"
        )

        if context:
            base_prompt += f"\nContext:\n{context}\n"

        base_prompt += f"\nUser Input:\n{message}\n"

        return base_prompt

    # ======================================================
    # PROCESS RESPONSE
    # ======================================================

    def process_response(self, response: str) -> Dict[str, Any]:
        """
        Normalize AI output
        """

        return {
            "raw": response,
            "signal": self._extract_signal(response),
            "confidence": self._extract_confidence(response)
        }

    # ======================================================
    # SIGNAL EXTRACTION
    # ======================================================

    def _extract_signal(self, text: str) -> str:
        """
        Extract BUY / SELL / HOLD from response
        """

        text = text.upper()

        if "BUY" in text:
            return "BUY"
        elif "SELL" in text:
            return "SELL"
        else:
            return "HOLD"

    # ======================================================
    # CONFIDENCE EXTRACTION
    # ======================================================

    def _extract_confidence(self, text: str) -> float:
        """
        Simple confidence detection (placeholder logic)
        """

        import re

        match = re.search(r"(\d{1,3})\s?%", text)

        if match:
            return min(float(match.group(1)), 100.0)

        return 50.0
