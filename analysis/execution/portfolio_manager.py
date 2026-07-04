import logging
from datetime import datetime


class Position:
    def __init__(self, symbol, side, entry_price, amount):
        self.symbol = symbol
        self.side = side  # BUY / SELL
        self.entry_price = entry_price
        self.amount = amount

        self.tp = None
        self.sl = None
        self.trailing_stop = None

        self.pnl = 0
        self.open_time = datetime.now()


class PortfolioManager:

    def __init__(self):
        self.positions = {}
        self.logger = logging.getLogger("PORTFOLIO")

    # ======================================================
    # OPEN POSITION
    # ======================================================
    def open_position(self, symbol, side, price, amount):

        pos = Position(symbol, side, price, amount)
        self.positions[symbol] = pos

        self.logger.info(f"POSITION OPENED: {symbol} {side} @ {price}")

        return pos

    # ======================================================
    # SET TP / SL
    # ======================================================
    def set_risk(self, symbol, tp_percent=2, sl_percent=1):

        pos = self.positions.get(symbol)
        if not pos:
            return

        if pos.side == "BUY":
            pos.tp = pos.entry_price * (1 + tp_percent / 100)
            pos.sl = pos.entry_price * (1 - sl_percent / 100)

        else:
            pos.tp = pos.entry_price * (1 - tp_percent / 100)
            pos.sl = pos.entry_price * (1 + sl_percent / 100)

        self.logger.info(f"TP/SL SET for {symbol} → TP:{pos.tp} SL:{pos.sl}")

    # ======================================================
    # UPDATE PRICE
    # ======================================================
    def update_price(self, symbol, current_price):

        pos = self.positions.get(symbol)
        if not pos:
            return None

        # PNL CALC
        if pos.side == "BUY":
            pos.pnl = (current_price - pos.entry_price) * pos.amount
        else:
            pos.pnl = (pos.entry_price - current_price) * pos.amount

        # TP HIT
        if pos.tp:
            if (pos.side == "BUY" and current_price >= pos.tp) or \
               (pos.side == "SELL" and current_price <= pos.tp):

                self.close_position(symbol, "TP HIT")
                return "CLOSED_TP"

        # SL HIT
        if pos.sl:
            if (pos.side == "BUY" and current_price <= pos.sl) or \
               (pos.side == "SELL" and current_price >= pos.sl):

                self.close_position(symbol, "SL HIT")
                return "CLOSED_SL"

        return "OPEN"

    # ======================================================
    # CLOSE POSITION
    # ======================================================
    def close_position(self, symbol, reason="MANUAL"):

        pos = self.positions.pop(symbol, None)

        if pos:
            self.logger.info(
                f"CLOSED {symbol} | PnL={pos.pnl:.2f} | Reason={reason}"
            )

        return pos
