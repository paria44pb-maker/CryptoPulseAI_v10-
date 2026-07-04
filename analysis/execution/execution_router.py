class ExecutionRouter:

    def __init__(self, logger, risk_engine, execution_layer):
        self.logger = logger
        self.risk_engine = risk_engine
        self.execution_layer = execution_layer
        self.name = "execution_router"

    # ======================================================
    # MAIN ENTRY POINT
    # ======================================================
    async def route(self, portfolio, signal):

        if not signal:
            return {
                "status": "NO_SIGNAL"
            }

        # 1. Risk check
        risk_result = self.risk_engine.evaluate(portfolio, signal)

        if not risk_result["approved"]:
            self.logger.warning("Trade blocked by RiskEngine")
            return {
                "status": "REJECTED",
                "reason": "RISK_ENGINE_BLOCK"
            }

        # 2. Send to execution layer
        result = await self.execution_layer.execute(signal)

        return {
            "status": "EXECUTED" if result else "FAILED",
            "signal": signal.signal,
            "symbol": signal.symbol
        }
