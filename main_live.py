import asyncio
import logging
import time

# ======================================================
# CORE
# ======================================================
from analysis.core.context_builder import ContextBuilder
from analysis.core.aggregator import Aggregator

# ======================================================
# ENGINES
# ======================================================
from analysis.engines.trend_engine import TrendEngine
from analysis.engines.momentum_engine import MomentumEngine
from analysis.engines.volume_engine import VolumeEngine
from analysis.engines.volatility_engine import VolatilityEngine
from analysis.engines.structure_engine import StructureEngine
from analysis.price_action import PriceAction

# ======================================================
# AI LAYER
# ======================================================
from analysis.ai.insight_engine import InsightEngine
from analysis.ai.scenario_engine import ScenarioEngine
from analysis.ai.risk_engine import RiskEngine

# ======================================================
# EXECUTION
# ======================================================
from analysis.execution.execution_router import ExecutionRouter


# ======================================================
# GLOBAL LIVE DATA HOLDER
# ======================================================
latest_market_data = {}


# ======================================================
# SYSTEM SETUP
# ======================================================
def setup_system():

    logger = logging.getLogger("LIVE_TRADING")
    logging.basicConfig(level=logging.INFO)

    context_builder = ContextBuilder(logger)
    aggregator = Aggregator(logger)

    trend = TrendEngine(logger)
    momentum = MomentumEngine(logger)
    volume = VolumeEngine(logger)
    volatility = VolatilityEngine(logger)
    structure = StructureEngine(logger)
    price_action = PriceAction(logger)

    engines = [
        {"name": "trend", "analyze": trend.analyze},
        {"name": "momentum", "analyze": momentum.analyze},
        {"name": "volume", "analyze": volume.analyze},
        {"name": "volatility", "analyze": volatility.analyze},
        {"name": "structure", "analyze": structure.analyze},
        {"name": "price_action", "analyze": price_action.analyze},
    ]

    insight_engine = InsightEngine(logger)
    scenario_engine = ScenarioEngine(logger)
    risk_engine = RiskEngine(logger)

    # ======================================================
    # EXECUTION LAYER (SAFE MOCK / READY FOR EXCHANGE API)
    # ======================================================
    class ExecutionLayer:
        async def execute(self, signal):
            logger.info(f"[EXECUTION] {signal.symbol} | {signal.signal}")
            return True

    execution_layer = ExecutionLayer()

    router = ExecutionRouter(logger, risk_engine, execution_layer)

    return {
        "logger": logger,
        "context_builder": context_builder,
        "aggregator": aggregator,
        "engines": engines,
        "insight_engine": insight_engine,
        "scenario_engine": scenario_engine,
        "risk_engine": risk_engine,
        "router": router
    }


# ======================================================
# MARKET DATA HANDLER (FROM WS)
# ======================================================
def on_market_data(data):
    global latest_market_data
    latest_market_data = data


# ======================================================
# LIVE ENGINE LOOP
# ======================================================
async def run_live():

    global latest_market_data

    system = setup_system()

    while True:

        if not latest_market_data:
            await asyncio.sleep(1)
            continue

        market_data = latest_market_data

        # ==================================================
        # CONTEXT BUILD
        # ==================================================
        context = system["context_builder"].build(market_data)

        # ==================================================
        # ENGINE RUN
        # ==================================================
        results = {}

        for engine in system["engines"]:
            try:
                results[engine["name"]] = engine["analyze"](context)
            except Exception as e:
                system["logger"].error(f"Engine error {engine['name']}: {e}")

        # ==================================================
        # AGGREGATION
        # ==================================================
        aggregated = system["aggregator"].merge(results)

        # ==================================================
        # INSIGHT
        # ==================================================
        insight = system["insight_engine"].build_insight(aggregated)

        # ==================================================
        # SCENARIOS
        # ==================================================
        scenarios = system["scenario_engine"].build_scenarios(aggregated)

        # ==================================================
        # SIGNAL
        # ==================================================
        class Signal:
            def __init__(self):
                self.symbol = market_data.get("symbol", "UNKNOWN")
                self.signal = aggregated.get("market_bias", "NEUTRAL")
                self.confidence_score = insight.get("confidence", 0)

        signal = Signal()

        # ==================================================
        # PORTFOLIO MOCK
        # ==================================================
        portfolio = type("Portfolio", (), {
            "cash": 10000,
            "exposure": 0.05
        })()

        # ==================================================
        # EXECUTION ROUTER
        # ==================================================
        execution_result = await system["router"].route(portfolio, signal)

        # ==================================================
        # OUTPUT
        # ==================================================
        print("\n================ LIVE UPDATE ================\n")

        print("Market Data:", market_data)
        print("\nAggregated:", aggregated)
        print("\nInsight:", insight)
        print("\nScenarios:", scenarios)
        print("\nExecution:", execution_result)

        await asyncio.sleep(5)


# ======================================================
# ENTRY POINT
# ======================================================
if __name__ == "__main__":
    asyncio.run(run_live())
