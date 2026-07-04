class TrendEngine:

    def __init__(self, logger):
        self.logger = logger
        self.name = "trend"

    def analyze(self, context):

        candles = context.get("candles", [])

        if not candles or len(candles) < 10:
            return {
                "trend": "UNKNOWN",
                "strength": "UNKNOWN",
                "phase": "UNSTABLE"
            }

        closes = [c["close"] for c in candles[-20:]]

        trend = self.detect_trend(closes)
        strength = self.calculate_strength(closes)
        phase = self.detect_phase(closes)

        return {
            "trend": trend,
            "strength": strength,
            "phase": phase
        }

    # ======================================================
    # TREND DIRECTION
    # ======================================================
    def detect_trend(self, closes):

        up = 0
        down = 0

        for i in range(1, len(closes)):
            if closes[i] > closes[i - 1]:
                up += 1
            else:
                down += 1

        if up > down * 1.2:
            return "UPTREND"

        if down > up * 1.2:
            return "DOWNTREND"

        return "SIDEWAYS"

    # ======================================================
    # TREND STRENGTH
    # ======================================================
    def calculate_strength(self, closes):

        changes = []

        for i in range(1, len(closes)):
            changes.append(abs(closes[i] - closes[i - 1]))

        if not changes:
            return "UNKNOWN"

        avg_change = sum(changes) / len(changes)
        last_change = abs(closes[-1] - closes[-2])

        if avg_change == 0:
            return "UNKNOWN"

        strength = (last_change / avg_change) * 100

        if strength > 120:
            return "STRONG"

        if strength > 80:
            return "MEDIUM"

        return "WEAK"

    # ======================================================
    # MARKET PHASE
    # ======================================================
    def detect_phase(self, closes):

        mid = len(closes) // 2

        first_half = closes[:mid]
        second_half = closes[mid:]

        if not first_half or not second_half:
            return "UNSTABLE"

        first_avg = sum(first_half) / len(first_half)
        second_avg = sum(second_half) / len(second_half)

        diff = abs(second_avg - first_avg)

        if diff < first_avg * 0.002:
            return "RANGE"

        if second_avg > first_avg:
            return "ACCUMULATION"

        return "DISTRIBUTION"
