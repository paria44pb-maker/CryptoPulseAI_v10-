class ContextBuilder:

    def __init__(self, logger):
        self.logger = logger
        self.name = "context_builder"

    # ======================================================
    # BUILD CONTEXT
    # ======================================================
    def build(self, market_data):

        if not market_data:
            self.logger.warning("Empty market data received")
            return None

        candles = market_data.get("candles", [])

        cleaned_candles = self.clean_candles(candles)

        context = {
            "symbol": market_data.get("symbol"),
            "timeframe": market_data.get("timeframe"),
            "candles": cleaned_candles,
            "timestamp": market_data.get("timestamp")
        }

        return context

    # ======================================================
    # CLEAN CANDLES
    # ======================================================
    def clean_candles(self, candles):

        if not candles:
            return []

        valid = []

        for c in candles:
            if self.is_valid_candle(c):
                valid.append(c)

        return valid

    # ======================================================
    # VALIDATE CANDLE
    # ======================================================
    def is_valid_candle(self, candle):

        required_fields = ["open", "high", "low", "close"]

        for field in required_fields:
            if field not in candle:
                return False

        if candle["high"] < candle["low"]:
            return False

        if candle["close"] == 0:
            return False

        return True

    # ======================================================
    # OPTIONAL NORMALIZE (future use)
    # ======================================================
    def normalize(self, candles):

        return candles
