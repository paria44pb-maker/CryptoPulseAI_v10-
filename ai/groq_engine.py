"""
═══════════════════════════════════════════════════════════════════════
CryptoPulse AI Enterprise
Groq AI Engine

Responsibilities:
- Connect to Groq API
- Send prompts
- Receive AI responses
- Handle retry & errors
═══════════════════════════════════════════════════════════════════════
"""

import time
import requests
from typing import Optional, Dict, Any

from core.logger import Logger
from config.settings import Settings
from ai.base_engine import AIBaseEngine


# ==========================================================
# GROQ AI ENGINE
# ==========================================================

class GroqAI(AIBaseEngine):
    """
    Groq AI integration layer
    """

    def __init__(self, settings: Settings):
        super().__init__(settings)
        self.logger = Logger("GroqAI")

        self.api_url = "https://api.groq.com/openai/v1/chat/completions"
        self.api_key = settings.GROQ_API_KEY

    # ======================================================
    # GENERATE RESPONSE
    # ======================================================

    def generate(self, message: str, context: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        Send request to Groq API and return AI response
        """

        if not self.api_key:
            self.logger.error("❌ Missing Groq API Key")
            return {
                "raw": "",
                "signal": "HOLD",
                "confidence": 0.0
            }

        prompt = self.build_prompt(message, context)

        payload = {
            "model": "llama3-70b-8192",
            "messages": [
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            "temperature": self.settings.AI_TEMPERATURE,
            "max_tokens": self.settings.AI_MAX_TOKENS,
            "top_p": self.settings.AI_TOP_P,
        }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }

        for attempt in range(self.settings.MAX_RETRIES):

            try:
                response = requests.post(
                    self.api_url,
                    json=payload,
                    headers=headers,
                    timeout=self.settings.TIMEOUT_SECONDS
                )

                if response.status_code == 200:

                    data = response.json()
                    content = data["choices"][0]["message"]["content"]

                    processed = self.process_response(content)

                    self.logger.info("🤖 AI response generated successfully")

                    return processed

                else:
                    self.logger.warning(
                        f"⚠️ Groq API error: {response.status_code}"
                    )

            except Exception as e:
                self.logger.error(f"❌ AI request failed: {e}")

                time.sleep(self.settings.RETRY_DELAY)

        self.logger.error("❌ AI failed after max retries")

        return {
            "raw": "",
            "signal": "HOLD",
            "confidence": 0.0
        }
