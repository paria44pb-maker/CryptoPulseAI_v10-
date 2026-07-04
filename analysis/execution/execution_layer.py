class ExecutionLayer:

    def __init__(
        self,
        coinex_executor,
        portfolio_manager,
        logger,
        risk_manager,
        learner,
        advanced_risk
    ):
        self.executor = coinex_executor
        self.portfolio = portfolio_manager
        self.logger = logger
        self.risk = risk_manager
        self.learner = learner
        self.advanced_risk = advanced_risk

    # ======================================================
    # MAIN EXECUTION PIPELINE
    # ======================================================
    async def execute(self, signal, portfolio=None):

        # --------------------------------------------------
        # 1. BLOCK NEUTRAL
        # --------------------------------------------------
        if signal.signal == "NEUTRAL":
            return {"status": "NO_TRADE"}

        # --------------------------------------------------
        # 2. AI SELF ADJUST CONFIDENCE
        # --------------------------------------------------
        signal.confidence_score = self.learner.adjust_confidence(signal)

        self.logger.info(
            f"[AI ADJUSTED CONFIDENCE] {signal.symbol} → {signal.confidence_score:.2f}"
        )

        # --------------------------------------------------
        # 3. RISK CHECK (HARD FILTER)
        # --------------------------------------------------
        if not self.risk.evaluate(signal, portfolio):
            self.logger.info("TRADE REJECTED BY RISK ENGINE")
            return {"status": "REJECTED_BY_RISK"}

        # --------------------------------------------------
        # 4. POSITION SIZE
        # --------------------------------------------------
        amount = 0.001
        side = "buy" if signal.signal == "BUY" else "sell"

        # --------------------------------------------------
        # 5. EXECUTE ORDER (REAL COINEX)
        # --------------------------------------------------
        try:
            result = self.executor.place_order(
                market=signal.symbol,
                side=side,
                amount=amount
            )

        except Exception as e:
            self.logger.error(f"EXECUTION ERROR: {e}")
            return {"status": "EXECUTION_FAILED"}

        # --------------------------------------------------
        # 6. TRACK POSITION
        # --------------------------------------------------
        position = self.portfolio.open_position(
            signal.symbol,
            side.upper(),
            price=1,  # placeholder (live price from WS در آینده)
            amount=amount
        )

        self.portfolio.set_risk(signal.symbol)

        # --------------------------------------------------
        # 7. TRAILING STOP INIT
        # --------------------------------------------------
        position.trailing_stop = None

        self.logger.info(
            f"[POSITION OPENED] {signal.symbol} {side} amount={amount}"
        )

        return {
            "status": "EXECUTED",
            "order_result": result,
            "symbol": signal.symbol,
            "side": side,
            "confidence": signal.confidence_score
        }

    # ======================================================
    # LIVE POSITION UPDATE (HOOK FOR LOOP)
    # ======================================================
    def update_positions(self, price_data):

        symbol = price_data.get("symbol")
        price = price_data.get("price")

        pos = self.portfolio.positions.get(symbol)

        if not pos:
            return None

        # --------------------------------------------------
        # TRAILING STOP ENGINE
        # --------------------------------------------------
        result = self.advanced_risk.update_trailing_stop(
            pos,
            price
        )

        # --------------------------------------------------
        # AUTO CLOSE IF TRAIL HIT
        # --------------------------------------------------
        if result == "TRAIL_EXIT":

            self.portfolio.close_position(symbol, "TRAILING STOP HIT")

            self.logger.info(
                f"[TRAIL EXIT] {symbol} closed at price {price}"
            )

            return "CLOSED"

        return "OPEN"
