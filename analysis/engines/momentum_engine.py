class MomentumEngine:

    def __init__(self, logger):
        self.logger = logger
        self.name = "momentum"

    def analyze(self, context):

        candles = context.get("candles", [])

        if not candles or len(candles) < 10:
            return {
                "momentum": "UNKNOWN",
                "strength": 0,
                "direction": "NEUTRAL"
            }

        closes = [c["close"] for c in candles[-20:]]

        momentum = self.calculate_momentum(closes)
        strength = self.calculate_strength(closes)
        direction = self.detect_direction(closes)

        return {
            "momentum": momentum,
            "strength": strength,
            "direction": direction
        }

    # ======================================================
    # MOMENTUM CALCULATION
    # ======================================================
    def calculate_momentum(self, closes):

        if len(closes) < 2:
            return "UNKNOWN"

        change = closes[-1] - closes[0]
        percent = (change / closes[0]) * 100

        if percent > 1.5:
            return "HIGH_POSITIVE"

        if percent > 0.5:
            return "POSITIVE"

        if percent < -1.5:
            return "HIGH_NEGATIVE"

        if percent < -0.5:
            return "NEGATIVE"

        return "NEUTRAL"

    # ======================================================
    # MOMENTUM STRENGTH
    # ======================================================
    def calculate_strength(self, closes):

        if len(closes) < 3:
            return 0

        changes = []

        for i in range(1, len(closes)):
            changes.append(abs(closes[i] - closes[i - 1]))

        if not changes:
            return 0

        avg_change = sum(changes) / len(changes)
        last_change = abs(closes[-1] - closes[-2])

        if avg_change == 0:
            return 0

        strength = (last_change / avg_change) * 100

        return round(strength, 2)

    # ======================================================
    # MOMENTUM DIRECTION
    # ======================================================
    def detect_direction(self, closes):

        up = 0
        down = 0

        for i in range(1, len(closes)):
            if closes[i] > closes[i - 1]:
                up += 1
            else:
                down += 1

        if up > down:
            return "BULLISH"

        if down > up:
            return "BEARISH"

        return "SIDEWAYS"
