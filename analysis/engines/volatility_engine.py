class VolatilityEngine:

    def __init__(self, logger):
        self.logger = logger
        self.name = "volatility"

    def analyze(self, context):

        candles = context.get("candles", [])

        if not candles or len(candles) < 10:
            return {
                "volatility": "UNKNOWN",
                "volatility_score": 0,
                "market_state": "UNSTABLE"
            }

        highs = [c["high"] for c in candles[-20:]]
        lows = [c["low"] for c in candles[-20:]]
        closes = [c["close"] for c in candles[-20:]]

        volatility_score = self.calculate_volatility(highs, lows)
        state = self.detect_market_state(volatility_score)
        range_type = self.detect_range_type(highs, lows, closes)

        return {
            "volatility": state,
            "volatility_score": round(volatility_score, 2),
            "market_state": range_type
        }

    # ======================================================
    # VOLATILITY SCORE
    # ======================================================
    def calculate_volatility(self, highs, lows):

        if len(highs) < 2 or len(lows) < 2:
            return 0

        ranges = []

        for i in range(len(highs)):
            ranges.append(highs[i] - lows[i])

        avg_range = sum(ranges) / len(ranges)
        max_range = max(ranges)

        if avg_range == 0:
            return 0

        volatility = (max_range / avg_range) * 100

        return volatility

    # ======================================================
    # MARKET STATE
    # ======================================================
    def detect_market_state(self, volatility_score):

        if volatility_score > 150:
            return "HIGH_VOLATILITY"

        if volatility_score > 80:
            return "MEDIUM_VOLATILITY"

        return "LOW_VOLATILITY"

    # ======================================================
    # RANGE TYPE
    # ======================================================
    def detect_range_type(self, highs, lows, closes):

        price_range = max(highs) - min(lows)
        avg_price = sum(closes) / len(closes)

        if avg_price == 0:
            return "UNKNOWN"

        range_ratio = price_range / avg_price

        if range_ratio < 0.01:
            return "TIGHT_RANGE"

        if range_ratio < 0.03:
            return "NORMAL_RANGE"

        return "WIDE_RANGE"
