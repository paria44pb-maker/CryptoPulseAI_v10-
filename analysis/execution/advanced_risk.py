import logging


class AdvancedRiskManager:

    def __init__(self):
        self.logger = logging.getLogger("ADV_RISK")

    # ======================================================
    # TRAILING STOP LOGIC
    # ======================================================
    def update_trailing_stop(self, position, current_price, trail_percent=0.8):

        if position.side == "BUY":

            # فقط وقتی سود کرده فعال میشه
            if current_price > position.entry_price:

                new_sl = current_price * (1 - trail_percent / 100)

                if position.trailing_stop is None or new_sl > position.trailing_stop:
                    position.trailing_stop = new_sl
                    self.logger.info(f"TRAILING STOP UPDATED → {new_sl}")

            # چک خروج
            if position.trailing_stop and current_price <= position.trailing_stop:
                return "TRAIL_EXIT"

        else:

            if current_price < position.entry_price:

                new_sl = current_price * (1 + trail_percent / 100)

                if position.trailing_stop is None or new_sl < position.trailing_stop:
                    position.trailing_stop = new_sl

            if position.trailing_stop and current_price >= position.trailing_stop:
                return "TRAIL_EXIT"

        return "HOLD"
