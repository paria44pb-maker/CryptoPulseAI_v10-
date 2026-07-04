class ExecutionLayer:

    def __init__(self, coinex_executor, portfolio_manager, logger):
        self.executor = coinex_executor
        self.portfolio = portfolio_manager
        self.logger = logger

    async def execute(self, signal, portfolio=None):

        if signal.signal == "NEUTRAL":
            return {"status": "NO_TRADE"}

        side = "buy" if signal.signal == "BUY" else "sell"
        amount = 0.001

        # ============================
        # REAL ORDER
        # ============================
        result = self.executor.place_order(
            market=signal.symbol,
            side=side,
            amount=amount
        )

        # ============================
        # TRACK POSITION
        # ============================
        price = 0  # در نسخه بعد از WS واقعی میاد

        self.portfolio.open_position(
            signal.symbol,
            side.upper(),
            price=1,   # placeholder
            amount=amount
        )

        self.portfolio.set_risk(signal.symbol)

        self.logger.info(f"EXECUTED + TRACKED: {signal.symbol}")

        return result
