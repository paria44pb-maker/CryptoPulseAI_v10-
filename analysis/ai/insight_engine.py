class ScenarioEngine:

    def __init__(self, logger):
        self.logger = logger
        self.name = "scenario_engine"

    # ======================================================
    # MAIN SCENARIO BUILDER
    # ======================================================
    def build_scenarios(self, aggregated_data):

        if not aggregated_data:
            return {
                "status": "NO_DATA",
                "primary_bias": "UNKNOWN",
                "scenarios": []
            }

        trend = aggregated_data.get("trend", "UNKNOWN")
        momentum = aggregated_data.get("momentum", "UNKNOWN")
        volume = aggregated_data.get("volume", "UNKNOWN")
        volatility = aggregated_data.get("volatility", "UNKNOWN")
        bias = aggregated_data.get("market_bias", "UNKNOWN")

        scenarios = [
            self.bullish_scenario(trend, momentum, volume),
            self.bearish_scenario(trend, momentum, volume),
            self.range_scenario(trend, volatility)
        ]

        return {
            "primary_bias": bias,
            "scenarios": scenarios
        }

    # ======================================================
    # BULLISH SCENARIO
    # ======================================================
    def bullish_scenario(self, trend, momentum, volume):

        score = 0

        if "UP" in str(trend):
            score += 40

        if "POSITIVE" in str(momentum):
            score += 30

        if "INCREASING" in str(volume):
            score += 30

        return {
            "type": "BULLISH",
            "probability": min(score, 100),
            "expectation": "Price continuation upward or breakout continuation"
        }

    # ======================================================
    # BEARISH SCENARIO
    # ======================================================
    def bearish_scenario(self, trend, momentum, volume):

        score = 0

        if "DOWN" in str(trend):
            score += 40

        if "NEGATIVE" in str(momentum):
            score += 30

        if "DECREASING" in str(volume):
            score += 30

        return {
            "type": "BEARISH",
            "probability": min(score, 100),
            "expectation": "Price continuation downward or breakdown continuation"
        }

    # ======================================================
    # RANGE SCENARIO
    # ======================================================
    def range_scenario(self, trend, volatility):

        score = 0

        if "SIDEWAYS" in str(trend):
            score += 50

        if "LOW" in str(volatility):
            score += 50

        return {
            "type": "RANGE",
            "probability": min(score, 100),
            "expectation": "Sideways movement with false breakouts likely"
        }
