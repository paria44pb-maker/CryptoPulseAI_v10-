class ContextBuilder:

    def __init__(self, logger):
        self.logger = logger
        self.name = "context_builder"

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
