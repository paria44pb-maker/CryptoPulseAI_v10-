import asyncio
import json
import time
import hmac
import hashlib
import requests
import websockets


# ======================================================
# COINEX REST API (ORDER EXECUTION)
# ======================================================
class CoinExREST:

    def __init__(self, api_key, secret_key, base_url="https://api.coinex.com"):
        self.api_key = api_key
        self.secret_key = secret_key
        self.base_url = base_url

    # --------------------------------------------------
    # SIGNATURE
    # --------------------------------------------------
    def sign(self, params):

        query = "&".join([f"{k}={params[k]}" for k in sorted(params)])
        return hmac.new(
            self.secret_key.encode(),
            query.encode(),
            hashlib.sha256
        ).hexdigest()

    # --------------------------------------------------
    # PLACE ORDER
    # --------------------------------------------------
    def place_order(self, market, side, amount, price=None):

        endpoint = "/v1/order/limit"

        params = {
            "access_id": self.api_key,
            "market": market,
            "type": side,
            "amount": amount,
            "tonce": int(time.time() * 1000)
        }

        if price:
            params["price"] = price

        params["sign"] = self.sign(params)

        response = requests.post(self.base_url + endpoint, data=params)

        return response.json()


# ======================================================
# COINEX WEBSOCKET (LIVE MARKET DATA)
# ======================================================
class CoinExWebSocket:

    def __init__(self, symbol="BTCUSDT"):
        self.symbol = symbol.lower()
        self.url = "wss://socket.coinex.com/v2/market"
        self.callbacks = []

    # --------------------------------------------------
    def subscribe(self, callback):
        self.callbacks.append(callback)

    # --------------------------------------------------
    async def handle(self, msg):

        try:
            data = json.loads(msg)

            if "data" in data:
                for cb in self.callbacks:
                    await cb(data["data"])

        except Exception:
            pass

    # --------------------------------------------------
    async def start(self):

        async with websockets.connect(self.url) as ws:

            sub_msg = {
                "method": "state.subscribe",
                "params": [self.symbol]
            }

            await ws.send(json.dumps(sub_msg))

            while True:
                msg = await ws.recv()
                await self.handle(msg)


# ======================================================
# MARKET DATA ADAPTER (NORMALIZER)
# ======================================================
class MarketAdapter:

    def normalize(self, raw):

        return {
            "symbol": raw.get("symbol", "BTCUSDT"),
            "price": raw.get("last", 0),
            "volume": raw.get("volume", 0),
            "timestamp": raw.get("ts", 0)
        }
