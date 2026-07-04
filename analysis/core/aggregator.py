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
                "status": "NO_DATA"
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
