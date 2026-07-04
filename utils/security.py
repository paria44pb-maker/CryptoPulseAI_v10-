"""
═══════════════════════════════════════════════════════════════════════
CryptoPulse AI Enterprise
Security Utilities

Responsibilities:
- Input sanitization
- Basic injection prevention
- Access control helpers
═══════════════════════════════════════════════════════════════════════
"""

import re
from typing import Any, Dict

from core.logger import Logger


logger = Logger("Security")


# ==========================================================
# BLACKLIST PATTERNS
# ==========================================================

BLACKLIST_PATTERNS = [
    r"rm\s+-rf",
    r"shutdown",
    r"format",
    r"DROP\s+TABLE",
    r"DELETE\s+FROM",
    r"<script.*?>",
]


# ==========================================================
# SANITIZE INPUT
# ==========================================================

def sanitize_input(data: str) -> str:
    """
    Clean dangerous patterns from input
    """

    if not isinstance(data, str):
        return ""

    original = data

    for pattern in BLACKLIST_PATTERNS:
        data = re.sub(pattern, "***", data, flags=re.IGNORECASE)

    if original != data:
        logger.warning("⚠️ Malicious input sanitized")

    return data.strip()


# ==========================================================
# STRICT VALIDATION
# ==========================================================

def is_safe_text(text: str) -> bool:
    """
    Check if input contains suspicious patterns
    """

    if not text:
        return True

    for pattern in BLACKLIST_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return False

    return True


# ==========================================================
# ACCESS CONTROL
# ==========================================================

def check_admin(user_id: int, admin_list: str) -> bool:
    """
    Check if user is admin
    """

    try:
        admins = [x.strip() for x in admin_list.split(",") if x.strip()]
        return str(user_id) in admins
    except Exception:
        return False


# ==========================================================
# MASK SENSITIVE DATA
# ==========================================================

def mask_secret(value: str, show: int = 4) -> str:
    """
    Mask sensitive values (API keys, tokens)
    """

    if not value:
        return ""

    if len(value) <= show:
        return "*" * len(value)

    return value[:show] + "*" * (len(value) - show)
