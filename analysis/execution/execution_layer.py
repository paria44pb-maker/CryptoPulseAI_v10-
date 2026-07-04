class ExecutionLayer:

    def __init__(self, coinex_executor, logger):
        self.executor = coinex_executor
        self.logger = logger

    # ======================================================
    # EXECUTE SIGNAL
    # ======================================================
    async def execute(self, signal, portfolio=None):

        if signal.signal == "NEUTRAL":
            return {"status": "NO_TRADE"}

        # مقدار فرضی معامله (بعداً مدیریت سرمایه واقعی می‌ذاریم)
        amount = 0.001

        side = "buy" if signal.signal == "BUY" else "sell"

        self.logger.info(f"EXECUTING REAL TRADE → {signal.symbol} {side}")

        result = self.executor.place_order(
            market=signal.symbol,
            side=side,
            amount=amount
        )

        return result
