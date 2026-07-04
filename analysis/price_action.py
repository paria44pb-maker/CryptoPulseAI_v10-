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
