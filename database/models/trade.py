"""
═══════════════════════════════════════════════════════════════════════
CryptoPulse AI Enterprise
Trade Model

Responsibilities:
- Store trade history
- Track entry/exit
- PnL calculation support
- Strategy logging
═══════════════════════════════════════════════════════════════════════
"""

from sqlalchemy import Column, String, Float, Boolean

from database.models.base import BaseModel


# ==========================================================
# TRADE MODEL
# ==========================================================

class Trade(BaseModel):
    """
    Represents a single trading operation
    """

    # User reference
    user_id = Column(String, index=True, nullable=False)

    # Market data
    symbol = Column(String, index=True, nullable=False)
    timeframe = Column(String, nullable=False)

    # Direction
    side = Column(String, nullable=False)  # BUY / SELL

    # Prices
    entry_price = Column(Float, nullable=False)
    exit_price = Column(Float, nullable=True)

    # Quantity
    quantity = Column(Float, nullable=False)

    # PnL
    profit_loss = Column(Float, default=0.0)
    profit_percent = Column(Float, default=0.0)

    # Status
    is_open = Column(Boolean, default=True)
    is_win = Column(Boolean, default=False)

    # Strategy info
    strategy = Column(String, nullable=True)
    signal_source = Column(String, nullable=True)

    # Risk
    risk_percent = Column(Float, default=0.0)

    # ======================================================
    # HELPERS
    # ======================================================

    def calculate_pnl(self):
        """
        Calculate profit/loss
        """

        if not self.exit_price:
            return 0.0

        if self.side == "BUY":
            pnl = (self.exit_price - self.entry_price) * self.quantity
        else:
            pnl = (self.entry_price - self.exit_price) * self.quantity

        self.profit_loss = pnl
        return pnl

    def calculate_profit_percent(self):
        """
        Calculate percentage profit
        """

        if not self.exit_price:
            return 0.0

        if self.side == "BUY":
            pct = ((self.exit_price - self.entry_price) / self.entry_price) * 100
        else:
            pct = ((self.entry_price - self.exit_price) / self.entry_price) * 100

        self.profit_percent = pct
        return pct

    def close_trade(self, exit_price: float):
        """
        Close trade and calculate results
        """

        self.exit_price = exit_price
        self.is_open = False

        pnl = self.calculate_pnl()
        self.calculate_profit_percent()

        self.is_win = pnl > 0

        return {
            "pnl": self.profit_loss,
            "percent": self.profit_percent,
            "win": self.is_win
        }
