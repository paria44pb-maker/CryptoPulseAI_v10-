class PriceAction:

    def __init__(self, logger):
        self.logger = logger
        self.name = "price_action"

    def analyze(self, context):

        candles = context.get("candles", [])

        structure = self.detect_structure(candles)
        breaks = self.detect_breakouts(candles)
        rejections = self.detect_rejections(candles)
        trend = self.detect_trend(candles)

        return {
            "structure": structure,
            "breakouts": breaks,
            "rejections": rejections,
            "trend": trend
        }

    # ======================================================
    # STRUCTURE
    # ======================================================
    def detect_structure(self, candles):

        highs = [c["high"] for c in candles]
        lows = [c["low"] for c in candles]

        if highs[-1] > max(highs[:-1]):
            return "BULLISH_STRUCTURE"

        if lows[-1] < min(lows[:-1]):
            return "BEARISH_STRUCTURE"

        return "RANGE"

    # ======================================================
    # TREND
    # ======================================================
    def detect_trend(self, candles):

        closes = [c["close"] for c in candles[-10:]]

        up = 0
        down = 0

        for i in range(1, len(closes)):
            if closes[i] > closes[i - 1]:
                up += 1
            else:
                down += 1

        if up > down:
            return "UPTREND"

        if down > up:
            return "DOWNTREND"

        return "SIDEWAYS"

    # ======================================================
    # BREAKOUTS
    # ======================================================
    def detect_breakouts(self, candles):

        last_close = candles[-1]["close"]
        prev_high = max(c["high"] for c in candles[:-1])
        prev_low = min(c["low"] for c in candles[:-1])

        breakouts = []

        if last_close > prev_high:
            breakouts.append("UP_BREAKOUT")

        if last_close < prev_low:
            breakouts.append("DOWN_BREAKOUT")

        return breakouts

    # ======================================================
    # REJECTIONS
    # ======================================================
    def detect_rejections(self, candles):

        results = []

        for c in candles[-10:]:

            body = abs(c["close"] - c["open"])
            upper_wick = c["high"] - max(c["open"], c["close"])
            lower_wick = min(c["open"], c["close"]) - c["low"]

            if upper_wick > body * 2:
                results.append("BEARISH_REJECTION")

            if lower_wick > body * 2:
                results.append("BULLISH_REJECTION")

        return results
