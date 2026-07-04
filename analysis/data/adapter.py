class MarketDataAdapter:

    def __init__(self):
        pass

    def normalize(self, raw):

        return {
            "symbol": raw.get("symbol", "BTCUSDT"),
            "price": raw.get("last", 0),
            "volume": raw.get("volume", 0),
            "timestamp": raw.get("ts", None)
        }
