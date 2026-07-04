class StructureEngine:

    def __init__(self, logger):
        self.logger = logger
        self.name = "structure"

    def analyze(self, context):

        candles = context.get("candles", [])

        if not candles or len(candles) < 10:
            return {
                "structure": "UNKNOWN",
                "break_structure": False,
                "market_bias": "NEUTRAL"
            }

        highs = [c["high"] for c in candles]
        lows = [c["low"] for c in candles]
        closes = [c["close"] for c in candles]

        structure = self.detect_structure(highs, lows)
        break_structure = self.detect_break_of_structure(highs, lows, closes)
        bias = self.detect_bias(highs, lows, closes)

        return {
            "structure": structure,
            "break_structure": break_structure,
            "market_bias": bias
        }

    # ======================================================
    # STRUCTURE DETECTION
    # ======================================================
    def detect_structure(self, highs, lows):

        if highs[-1] > max(highs[:-1]):
            return "BULLISH_STRUCTURE"

        if lows[-1] < min(lows[:-1]):
            return "BEARISH_STRUCTURE"

        return "RANGE_STRUCTURE"

    # ======================================================
    # BREAK OF STRUCTURE
    # ======================================================
    def detect_break_of_structure(self, highs, lows, closes):

        prev_high = max(highs[:-1])
        prev_low = min(lows[:-1])
        last_close = closes[-1]

        if last_close > prev_high:
            return True

        if last_close < prev_low:
            return True

        return False

    # ======================================================
    # MARKET BIAS
    # ======================================================
    def detect_bias(self, highs, lows, closes):

        up_moves = 0
        down_moves = 0

        for i in range(1, len(closes)):
            if closes[i] > closes[i - 1]:
                up_moves += 1
            else:
                down_moves += 1

        if up_moves > down_moves * 1.1:
            return "BULLISH_BIAS"

        if down_moves > up_moves * 1.1:
            return "BEARISH_BIAS"

        return "NEUTRAL_BIAS"
