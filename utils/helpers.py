"""
═══════════════════════════════════════════════════════════════════════
CryptoPulse AI Enterprise
Utility Helpers

Responsibilities:
- Common helper functions
- Time utilities
- Formatting tools
- Data validation helpers
═══════════════════════════════════════════════════════════════════════
"""

import re
from datetime import datetime, timezone


# ==========================================================
# TIME HELPERS
# ==========================================================

def utc_now() -> datetime:
    """
    Get current UTC time
    """
    return datetime.now(timezone.utc)


def timestamp() -> float:
    """
    Get current timestamp
    """
    return datetime.utcnow().timestamp()


def iso_now() -> str:
    """
    Get ISO formatted current time
    """
    return utc_now().isoformat()


# ==========================================================
# STRING HELPERS
# ==========================================================

def clean_text(text: str) -> str:
    """
    Clean and sanitize text input
    """
    if not text:
        return ""

    return text.strip()


def normalize_symbol(symbol: str) -> str:
    """
    Normalize trading symbol (BTC -> BTCUSDT)
    """
    symbol = symbol.upper().strip()

    if symbol.endswith("USDT"):
        return symbol

    return f"{symbol}USDT"


def extract_numbers(text: str) -> list[float]:
    """
    Extract numbers from string
    """
    return [float(x) for x in re.findall(r"[-+]?\d*\.\d+|\d+", text)]


# ==========================================================
# VALIDATION HELPERS
# ==========================================================

def is_valid_symbol(symbol: str) -> bool:
    """
    Basic symbol validation
    """
    return bool(re.match(r"^[A-Z0-9]{3,15}$", symbol.upper()))


def is_positive_number(value: float) -> bool:
    """
    Check if number is positive
    """
    return isinstance(value, (int, float)) and value > 0


# ==========================================================
# FORMAT HELPERS
# ==========================================================

def format_price(price: float) -> str:
    """
    Format price for display
    """
    return f"{price:,.2f}"


def format_percent(value: float) -> str:
    """
    Format percentage
    """
    return f"{value:.2f}%"
