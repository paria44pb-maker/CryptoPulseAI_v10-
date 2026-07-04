import asyncio
import logging

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
# SYSTEM SETUP
# ======================================================
def setup_system():

    logger = logging.getLogger("TradingSystem")
    logging.basicConfig(level=logging.INFO)

    # ---------------- CORE ----------------
    context_builder = ContextBuilder(logger)
    aggregator = Aggregator(logger)

    # ---------------- ENGINES ----------------
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

    # ---------------- AI ----------------
    insight_engine = InsightEngine(logger)
    scenario_engine = ScenarioEngine(logger)

    # ---------------- RISK ----------------
    risk_engine = RiskEngine(logger)

    # ---------------- EXECUTION ----------------
    class ExecutionLayer:
        async def execute(self, signal):
            logger.info(f"EXECUTING SIGNAL -> {signal.symbol} | {signal.signal}")
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
# MAIN RUNNER
# ======================================================
async def run_system():

    system = setup_system()

    # ======================================================
    # SAMPLE MARKET DATA
    # ======================================================
    market_data = {
        "symbol": "BTCUSDT",
        "timeframe": "5m",
        "timestamp": "2026-01-01T12:00:00",
        "candles": [
            {"open": 100, "high": 110, "low": 95, "close": 108, "volume": 1200},
            {"open": 108, "high": 115, "low": 107, "close": 112, "volume": 1300},
            {"open": 112, "high": 118, "low": 110, "close": 117, "volume": 1500},
            {"open": 117, "high": 120, "low": 114, "close": 116, "volume": 1400},
            {"open": 116, "high": 119, "low": 113, "close": 118, "volume": 1600},
        ]
    }

    # ======================================================
    # 1. BUILD CONTEXT
    # ======================================================
    context = system["context_builder"].build(market_data)

    # ======================================================
    # 2. RUN ALL ENGINES
    # ======================================================
    results = {}

    for engine in system["engines"]:
        try:
            results[engine["name"]] = engine["analyze"](context)
        except Exception as e:
            system["logger"].error(f"Engine error {engine['name']}: {e}")

    # ======================================================
    # 3. AGGREGATION
    # ======================================================
    aggregated = system["aggregator"].merge(results)

    # ======================================================
    # 4. AI INSIGHT
    # ======================================================
    insight = system["insight_engine"].build_insight(aggregated)

    # ======================================================
    # 5. SCENARIOS
    # ======================================================
    scenarios = system["scenario_engine"].build_scenarios(aggregated)

    # ======================================================
    # 6. SIGNAL OBJECT
    # ======================================================
    class Signal:
        def __init__(self):
            self.symbol = market_data["symbol"]
            self.signal = aggregated.get("market_bias", "NEUTRAL")
            self.confidence_score = insight["confidence"]

    signal = Signal()

    # ======================================================
    # 7. PORTFOLIO MOCK
    # ======================================================
    portfolio = type("Portfolio", (), {
        "cash": 10000,
        "exposure": 0.05
    })()

    # ======================================================
    # 8. EXECUTION ROUTE
    # ======================================================
    execution_result = await system["router"].route(portfolio, signal)

    # ======================================================
    # FINAL OUTPUT
    # ======================================================
    print("\n================ FINAL REPORT ================\n")

    print("AGGREGATED:")
    print(aggregated)

    print("\nINSIGHT:")
    print(insight)

    print("\nSCENARIOS:")
    print(scenarios)

    print("\nEXECUTION:")
    print(execution_result)


# ======================================================
# ENTRY POINT
# ======================================================
if __name__ == "__main__":
    asyncio.run(run_system())
