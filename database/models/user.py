"""
═══════════════════════════════════════════════════════════════════════
CryptoPulse AI Enterprise
User Model

Responsibilities:
- User management
- Admin / VIP roles
- Trading permissions
═══════════════════════════════════════════════════════════════════════
"""

from sqlalchemy import Column, String, Boolean, Integer, Float

from database.models.base import BaseModel


# ==========================================================
# USER MODEL
# ==========================================================

class User(BaseModel):
    """
    System user model
    """

    # Telegram ID
    telegram_id = Column(String, unique=True, index=True, nullable=False)

    # Basic info
    username = Column(String, nullable=True)
    first_name = Column(String, nullable=True)

    # Roles
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    is_vip = Column(Boolean, default=False)

    # Trading permissions
    can_trade = Column(Boolean, default=False)
    max_risk_percent = Column(Float, default=2.0)

    # Subscription
    vip_expiry = Column(String, nullable=True)  # ISO date string

    # Stats
    total_trades = Column(Integer, default=0)
    winning_trades = Column(Integer, default=0)

    balance = Column(Float, default=0.0)

    # ======================================================
    # HELPERS
    # ======================================================

    def win_rate(self) -> float:
        """
        Calculate user win rate
        """

        if self.total_trades == 0:
            return 0.0

        return (self.winning_trades / self.total_trades) * 100

    def is_vip_active(self) -> bool:
        """
        Check VIP status (simple version)
        """

        if not self.is_vip:
            return False

        if not self.vip_expiry:
            return True

        return True  # (later will connect to datetime logic)
