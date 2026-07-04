import asyncio
import logging
import time

from analysis.core.context_builder import ContextBuilder
from analysis.core.aggregator import Aggregator

from analysis.engines.trend_engine import TrendEngine
from analysis.engines.momentum_engine import MomentumEngine
from analysis.engines.volume_engine import VolumeEngine
from analysis.engines.volatility_engine import VolatilityEngine
from analysis.engines.structure_engine import StructureEngine
from analysis.price_action import PriceAction

from analysis.ai.insight_engine import InsightEngine
from analysis.ai.scenario_engine import ScenarioEngine
from analysis.ai.risk_engine import RiskEngine

from analysis.execution.execution_router import ExecutionRouter


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
        trend, momentum, volume,
        volatility, structure, price_action
    ]

    insight_engine = InsightEngine(logger)
    scenario_engine = ScenarioEngine(logger)
    risk_engine = RiskEngine(logger)

    # ======================================================
    # EXECUTION LAYER (READY FOR EXCHANGE API)
    # ======================================================
    class ExecutionLayer:
        async def execute(self, signal):
            logging.info(f"[EXECUTION] {signal.symbol} | {signal.signal}")
            return True  # placeholder for real exchange order

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
# MOCK MARKET DATA (REPLACE WITH COINEX API)
# ======================================================
async def fetch_market_data():

    return {
        "symbol": "BTCUSDT",
        "timeframe": "5m",
        "timestamp": time.time(),
        "candles": [
            {"open": 100, "high": 110, "low": 95, "close": 108, "volume": 1200},
            {"open": 108, "high": 115, "low": 107, "close": 112, "volume": 1300},
            {"open": 112, "high": 118, "low": 110, "close": 117, "volume": 1500},
        ]
    }


# ======================================================
# LIVE ENGINE LOOP
# ======================================================
async def run_live():

    system = setup_system()

    while True:

        # 1. GET MARKET DATA
        market_data = await fetch_market_data()

        # 2. BUILD CONTEXT
        context = system["context_builder"].build(market_data)

        # 3. RUN ALL ENGINES
        results = {}

        for engine in system["engines"]:
            try:
                results[type(engine).__name__] = engine.analyze(context)
            except Exception:
                continue

        # 4. AGGREGATION
        aggregated = system["aggregator"].merge(results)

        # 5. AI INSIGHT
        insight = system["insight_engine"].build_insight(aggregated)

        # 6. SCENARIO ENGINE
        scenarios = system["scenario_engine"].build_scenarios(aggregated)

        # 7. SIGNAL OBJECT
        class Signal:
            def __init__(self):
                self.symbol = market_data["symbol"]
                self.signal = aggregated.get("market_bias", "NEUTRAL")
                self.confidence_score = insight["confidence"]

        signal = Signal()

        # 8. PORTFOLIO MOCK
        portfolio = type("Portfolio", (), {
            "cash": 10000,
            "exposure": 0.05
        })()

        # 9. EXECUTION ROUTING
        execution_result = await system["router"].route(portfolio, signal)

        # 10. OUTPUT
        print("\n================ LIVE SYSTEM UPDATE ================\n")

        print("AGGREGATED:")
        print(aggregated)

        print("\nINSIGHT:")
        print(insight)

        print("\nSCENARIOS:")
        print(scenarios)

        print("\nEXECUTION:")
        print(execution_result)

        # delay (live cycle)
        await asyncio.sleep(5)


# ======================================================
# ENTRY POINT
# ======================================================
if __name__ == "__main__":
    asyncio.run(run_live())
