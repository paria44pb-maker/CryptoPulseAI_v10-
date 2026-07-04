class IndicatorEngine:

    def __init__(self, modules, storage, cache, logger):
        self.modules = modules
        self.storage = storage
        self.cache = cache
        self.logger = logger

    def initialize(self):
        self.logger.info("IndicatorEngine initialized")

    def build_context(self, market_data):
        return market_data

    def validate(self, context):
        return True

    def run_modules(self, context):
        results = {}

        for module in self.modules:
            try:
                results[module.name] = module.analyze(context)
            except Exception as e:
                self.logger.error(f"Module error: {module.name} -> {e}")
                results[module.name] = None

        return results

    def aggregate(self, results):
        return {
            "trend": results.get("trend"),
            "momentum": results.get("momentum"),
            "volume": results.get("volume"),
            "volatility": results.get("volatility"),
            "structure": results.get("structure"),
        }

    def build_report(self, context, aggregated):
        return {
            "symbol": context.get("symbol"),
            "timeframe": context.get("timeframe"),
            "data": aggregated,
            "timestamp": context.get("timestamp"),
        }

    def save(self, report):
        self.storage.save(report)

    def analyze(self, market_data):

        context = self.build_context(market_data)

        if not self.validate(context):
            return None

        results = self.run_modules(context)

        aggregated = self.aggregate(results)

        report = self.build_report(context, aggregated)

        self.save(report)

        return report
      
