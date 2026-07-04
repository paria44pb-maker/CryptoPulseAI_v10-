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
# EXECUTION + PORTFOLIO
# ======================================================
from analysis.execution.coinex_execution import CoinExExecution
from analysis.execution.execution_layer import ExecutionLayer
from analysis.execution.portfolio_manager import PortfolioManager

# ======================================================
# DATA
# ======================================================
from analysis.data.coinex_connector import CoinExWebSocket, MarketAdapter


# ======================================================
# GLOBAL STATE
# ======================================================
latest_market_data = {}
adapter = MarketAdapter()


# ======================================================
# SYSTEM SETUP
# ======================================================
def setup_system():

    logger = logging.getLogger("LIVE_TRADING")
    logging.basicConfig(level=logging.INFO)

    # ==================================================
    # CORE
    # ==================================================
    context_builder = ContextBuilder(logger)
    aggregator = Aggregator(logger)

    # ==================================================
    # ENGINES
    # ==================================================
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

    # ==================================================
    # AI
    # ==================================================
    insight_engine = InsightEngine(logger)
    scenario_engine = ScenarioEngine(logger)
    risk_engine = RiskEngine(logger)

    # ==================================================
    # PORTFOLIO MANAGER
    # ==================================================
    portfolio_manager = PortfolioManager()

    # ==================================================
    # COINEX EXECUTOR
    # ==================================================
    coinex_executor = CoinExExecution(
        api_key="YOUR_API_KEY",
        secret_key="YOUR_SECRET_KEY"
    )

    # ==================================================
    # EXECUTION LAYER
    # ==================================================
    execution_layer = ExecutionLayer(
        coinex_executor,
        portfolio_manager,
        logger
    )

    # ==================================================
    # ROUTER
    # ==================================================
    class ExecutionRouter:
        def __init__(self, risk_engine, execution_layer):
            self.risk_engine = risk_engine
            self.execution_layer = execution_layer

        async def route(self, portfolio, signal):

            if not self.risk_engine.evaluate(signal, portfolio):
                return {"status": "REJECTED_BY_RISK"}

            return await self.execution_layer.execute(signal, portfolio)

    router = ExecutionRouter(risk_engine, execution_layer)

    return {
        "logger": logger,
        "context_builder": context_builder,
        "aggregator": aggregator,
        "engines": engines,
        "insight_engine": insight_engine,
        "scenario_engine": scenario_engine,
        "risk_engine": risk_engine,
        "router": router,
        "portfolio_manager": portfolio_manager
    }


# ======================================================
# MARKET DATA CALLBACK
# ======================================================
async def on_market_data(data):

    global latest_market_data

    latest_market_data = adapter.normalize(data)


# ======================================================
# LIVE ENGINE LOOP
# ======================================================
async def run_live():

    global latest_market_data

    system = setup_system()
    portfolio_manager = system["portfolio_manager"]

    while True:

        if not latest_market_data:
            await asyncio.sleep(1)
            continue

        market_data = latest_market_data

        # ==================================================
        # UPDATE PORTFOLIO PRICE (PnL LIVE)
        # ==================================================
        portfolio_manager.update_price(
            market_data["symbol"],
            market_data["price"]
        )

        # ==================================================
        # CONTEXT
        # ==================================================
        context = system["context_builder"].build(market_data)

        # ==================================================
        # ENGINES
        # ==================================================
        results = {}

        for engine in system["engines"]:
            try:
                results[engine["name"]] = engine["analyze"](context)
            except Exception as e:
                system["logger"].error(f"Engine error: {e}")

        # ==================================================
        # AGGREGATION
        # ==================================================
        aggregated = system["aggregator"].merge(results)

        # ==================================================
        # AI INSIGHT
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
        # MOCK PORTFOLIO STATE
        # ==================================================
        portfolio = type("Portfolio", (), {
            "cash": 10000,
            "exposure": 0.05
        })()

        # ==================================================
        # EXECUTION
        # ==================================================
        execution_result = await system["router"].route(portfolio, signal)

        # ==================================================
        # OUTPUT
        # ==================================================
        print("\n================ LIVE UPDATE ================\n")
        print("Market:", market_data)
        print("Aggregated:", aggregated)
        print("Insight:", insight)
        print("Scenarios:", scenarios)
        print("Execution:", execution_result)

        await asyncio.sleep(5)


# ======================================================
# WEBSOCKET START
# ======================================================
async def start_ws():

    ws = CoinExWebSocket("BTCUSDT")
    ws.subscribe(on_market_data)

    await ws.start()


# ======================================================
# MAIN
# ======================================================
async def main():

    await asyncio.gather(
        start_ws(),
        run_live()
    )


if __name__ == "__main__":
    asyncio.run(main())
