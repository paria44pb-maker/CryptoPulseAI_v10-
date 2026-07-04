class RiskEngine:

    def __init__(self, logger, max_risk_per_trade=0.02, max_exposure=0.1):
        self.logger = logger
        self.name = "risk_engine"

        # تنظیمات ریسک
        self.max_risk_per_trade = max_risk_per_trade  # 2%
        self.max_exposure = max_exposure              # 10%

    # ======================================================
    # MAIN RISK EVALUATION
    # ======================================================
    def evaluate(self, portfolio, signal):

        if not portfolio or not signal:
            return {
                "approved": False,
                "reason": "Missing portfolio or signal"
            }

        risk_ok = self.check_trade_risk(portfolio)
        exposure_ok = self.check_exposure(portfolio)
        confidence_ok = self.check_confidence(signal)

        approved = risk_ok and exposure_ok and confidence_ok

        return {
            "approved": approved,
            "risk_ok": risk_ok,
            "exposure_ok": exposure_ok,
            "confidence_ok": confidence_ok
        }

    # ======================================================
    # TRADE RISK CHECK
    # ======================================================
    def check_trade_risk(self, portfolio):

        cash = getattr(portfolio, "cash", 0)
        risk_amount = cash * self.max_risk_per_trade

        # جلوگیری از ریسک صفر یا منفی
        if risk_amount <= 0:
            return False

        # کنترل حد ریسک غیرعادی
        if risk_amount > cash * 0.05:
            return False

        return True

    # ======================================================
    # EXPOSURE CHECK
    # ======================================================
    def check_exposure(self, portfolio):

        exposure = getattr(portfolio, "exposure", 0)

        if exposure >= self.max_exposure:
            return False

        return True

    # ======================================================
    # SIGNAL CONFIDENCE CHECK
    # ======================================================
    def check_confidence(self, signal):

        confidence = getattr(signal, "confidence_score", 0)

        if confidence < 65:
            return False

        return True
