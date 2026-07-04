import time
import hmac
import hashlib
import requests
import logging


class CoinExExecution:

    def __init__(self, api_key, secret_key, base_url="https://api.coinex.com"):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url
        self.logger = logging.getLogger("COINEX_EXECUTION")

    # ======================================================
    # SIGNATURE
    # ======================================================
    def sign(self, params):

        query = "&".join([f"{k}={params[k]}" for k in sorted(params)])
        return hmac.new(
            self.secret_key.encode(),
            query.encode(),
            hashlib.sha256
        ).hexdigest()

    # ======================================================
    # PLACE ORDER (REAL)
    # ======================================================
    def place_order(self, market, side, amount, price=None):

        endpoint = "/v1/order/limit"

        params = {
            "access_id": self.api_key,
            "market": market,
            "type": side,   # buy / sell
            "amount": str(amount),
            "tonce": str(int(time.time() * 1000))
        }

        if price:
            params["price"] = str(price)

        params["sign"] = self.sign(params)

        try:
            response = requests.post(
                self.base_url + endpoint,
                data=params,
                timeout=10
            )

            result = response.json()

            self.logger.info(f"ORDER SENT: {result}")

            return result

        except Exception as e:
            self.logger.error(f"ORDER ERROR: {e}")
            return {"status": "error", "message": str(e)}
