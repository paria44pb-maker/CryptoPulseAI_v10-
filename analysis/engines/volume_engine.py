class VolumeEngine:

    def __init__(self, logger):
        self.logger = logger
        self.name = "volume"

    def analyze(self, context):

        candles = context.get("candles", [])

        if not candles or len(candles) < 10:
            return {
                "volume_trend": "UNKNOWN",
                "volume_strength": 0,
                "volume_quality": "LOW"
            }

        volumes = [c["volume"] for c in candles[-20:]]

        return {
            "volume_trend": self.detect_volume_trend(volumes),
            "volume_strength": self.calculate_volume_strength(volumes),
            "volume_quality": self.evaluate_volume_quality(volumes)
        }

    # ======================================================
    # VOLUME TREND
    # ======================================================
    def detect_volume_trend(self, volumes):

        up = 0
        down = 0

        for i in range(1, len(volumes)):
            if volumes[i] > volumes[i - 1]:
                up += 1
            else:
                down += 1

        if up > down:
            return "INCREASING"

        if down > up:
            return "DECREASING"

        return "STABLE"

    # ======================================================
    # VOLUME STRENGTH
    # ======================================================
    def calculate_volume_strength(self, volumes):

        avg_volume = sum(volumes) / len(volumes)
        last_volume = volumes[-1]

        if avg_volume == 0:
            return 0

        strength = (last_volume / avg_volume) * 100

        return round(strength, 2)

    # ======================================================
    # VOLUME QUALITY
    # ======================================================
    def evaluate_volume_quality(self, volumes):

        avg_volume = sum(volumes) / len(volumes)
        max_volume = max(volumes)
        min_volume = min(volumes)

        if avg_volume == 0:
            return "LOW"

        volatility = (max_volume - min_volume) / avg_volume

        if volatility > 2:
            return "HIGH"

        if volatility > 1:
            return "MEDIUM"

        return "LOW"
