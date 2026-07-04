class Aggregator:

    def __init__(self, logger):
        self.logger = logger
        self.name = "aggregator"

    # ======================================================
    # MAIN MERGE FUNCTION
    # ======================================================
    def merge(self, results):

        if not results:
            return {
                "status": "NO_DATA",
                "market_bias": "UNKNOWN"
            }

        return {
            "trend": self.safe_get(results, "trend"),
            "momentum": self.safe_get(results, "momentum"),
            "volume": self.safe_get(results, "volume"),
            "volatility": self.safe_get(results, "volatility"),
            "structure": self.safe_get(results, "structure"),
            "price_action": self.safe_get(results, "price_action"),
            "market_bias": self.calculate_bias(results)
        }

    # ======================================================
    # SAFE GET
    # ======================================================
    def safe_get(self, results, key):

        value = results.get(key, None)

        if value is None:
            return "UNKNOWN"

        return value

    # ======================================================
    # MARKET BIAS CALCULATION
    # ======================================================
    def calculate_bias(self, results):

        bullish = 0
        bearish = 0

        # ---------------- Trend ----------------
        trend = results.get("trend", "")
        if "UP" in str(trend):
            bullish += 1
        elif "DOWN" in str(trend):
            bearish += 1

        # ---------------- Momentum ----------------
        momentum = results.get("momentum", "")
        if "POSITIVE" in str(momentum):
            bullish += 1
        elif "NEGATIVE" in str(momentum):
            bearish += 1

        # ---------------- Volume ----------------
        volume = results.get("volume", "")
        if "INCREASING" in str(volume):
            bullish += 1
        elif "DECREASING" in str(volume):
            bearish += 1

        # ---------------- Structure ----------------
        structure = results.get("structure", "")
        if "BULLISH" in str(structure):
            bullish += 1
        elif "BEARISH" in str(structure):
            bearish += 1

        # ---------------- Final Decision ----------------
        if bullish > bearish:
            return "BULLISH_BIAS"

        if bearish > bullish:
            return "BEARISH_BIAS"

        return "NEUTRAL_BIAS"
