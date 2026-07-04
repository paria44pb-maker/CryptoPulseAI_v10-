import asyncio
import json
import websockets
import logging


class CoinExWebSocket:

    def __init__(self, logger, symbol="BTCUSDT"):
        self.logger = logger
        self.symbol = symbol.lower()
        self.url = "wss://socket.coinex.com/v2/market"

        self.callbacks = []

    # ======================================================
    # SUBSCRIBE CALLBACK
    # ======================================================
    def subscribe(self, callback):

        self.callbacks.append(callback)

    # ======================================================
    # HANDLE MESSAGE
    # ======================================================
    async def handle_message(self, message):

        try:
            data = json.loads(message)

            if "data" in data:

                for cb in self.callbacks:
                    await cb(data["data"])

        except Exception as e:
            self.logger.error(f"WS Parse Error: {e}")

    # ======================================================
    # START STREAM
    # ======================================================
    async def start(self):

        self.logger.info(f"Connecting to CoinEx WebSocket... {self.symbol}")

        async with websockets.connect(self.url) as ws:

            # subscribe request
            sub_msg = {
                "method": "state.subscribe",
                "params": [self.symbol]
            }

            await ws.send(json.dumps(sub_msg))

            self.logger.info("Subscribed successfully")

            while True:

                message = await ws.recv()
                await self.handle_message(message)

          
