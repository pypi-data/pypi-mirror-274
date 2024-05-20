import base64
import hmac
import logging
import time
from contextlib import asynccontextmanager

import trio
import orjson
import trio_websocket
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.serialization import load_pem_private_key
from trio_websocket import open_websocket_url, ConnectionClosed

from trio_bybit.exceptions import BybitWebsocketOpError


class BybitSocketManager:
    URLS = {
        "main": {
            "spot": "wss://stream.bybit.com/v5/public/spot",
            "linear": "wss://stream.bybit.com/v5/public/linear",
            "inverse": "wss://stream.bybit.com/v5/public/inverse",
            "private": "wss://stream.bybit.com/v5/private",
        },
        "test": {
            "spot": "wss://stream-testnet.bybit.com/v5/public/spot",
            "linear": "wss://stream-testnet.bybit.com/v5/public/linear",
            "inverse": "wss://stream-testnet.bybit.com/v5/public/inverse",
            "private": "wss://stream-testnet.bybit.com/v5/private",
        },
        "demo": {
            "private": "wss://stream-demo.bybit.com",
        },
    }

    def __init__(
        self,
        endpoint: str = "spot",
        api_key: str | None = None,
        api_secret: str | None = None,
        alternative_net: str = "",
        sign_style: str = "HMAC",
    ):
        self.ws: trio_websocket.WebSocketConnection | None = None
        self.endpoint: str = endpoint
        self.alternative_net: str = alternative_net if alternative_net else "main"
        if self.endpoint == "private" and (api_key is None or api_secret is None):
            raise ValueError("api_key and api_secret must be provided for private streams")
        self.api_key = api_key
        self.api_secret = api_secret
        self.conn_id: str | None = None
        if sign_style != "HMAC":
            with open(api_secret, "rb") as f:
                self.api_secret = load_pem_private_key(f.read(), password=None)
        else:
            self.api_secret = api_secret
        self.sign_style = sign_style
        self.ping_scope: trio.CancelScope | None = None
        self.subscribed = set()

    @asynccontextmanager
    async def connect(self):
        try:
            url = self.URLS[self.alternative_net][self.endpoint]
        except KeyError:
            raise ValueError(f"endpoint {self.endpoint} with net {self.alternative_net} not supported")
        async with open_websocket_url(url) as ws:
            self.ws = ws
            async with trio.open_nursery() as nursery:
                self.ping_scope = await nursery.start(self.heartbeat)
                if self.endpoint == "private":
                    await self._send_signature()
                yield self.ws
                nursery.cancel_scope.cancel()

    async def _reconnect(self):
        self.ping_scope.cancel()
        url = self.URLS[self.alternative_net][self.endpoint]
        async with open_websocket_url(url) as ws:
            self.ws = ws
            async with trio.open_nursery() as nursery:
                self.ping_scope = await nursery.start(self.heartbeat)
                if self.endpoint == "private":
                    await self._send_signature()
                await self.subscribe({"op": "subscribe", "args": list(self.subscribed)})

    async def heartbeat(self, *, task_status=trio.TASK_STATUS_IGNORED):
        with trio.CancelScope() as ping_scope:
            task_status.started(ping_scope)
            while True:
                with trio.fail_after(5):
                    await self.ws.send_message('{"op": "ping"}')
                await trio.sleep(20)

    async def _send_signature(self):
        expires = int((time.time() + 1) * 1000)
        if self.sign_style == "HMAC":
            signature = str(
                hmac.new(
                    self.api_secret.encode("utf-8"), f"GET/realtime{expires}".encode("utf-8"), digestmod="sha256"
                ).hexdigest()
            )
        else:  # RSA
            signature = self.api_secret.sign(
                f"GET/realtime{expires}".encode("utf-8"), padding.PKCS1v15(), hashes.SHA256()
            )
            signature = base64.b64encode(signature).decode()
        await self.ws.send_message(orjson.dumps({"op": "auth", "args": [self.api_key, expires, signature]}))
        auth_ret = orjson.loads(await self.ws.get_message())
        if auth_ret["op"] == "auth":
            try:
                assert auth_ret["success"]
            except AssertionError:
                raise BybitWebsocketOpError(auth_ret)
            self.conn_id = auth_ret["conn_id"]

    async def subscribe(self, subscription: dict):
        """
        Subscribe or unsubscribe to a websocket stream.
        :param subscription: (un)subscription message, e.g. {"op": "subscribe", "args": ["publicTrade.BTCUSDT"]}
        """
        if subscription["op"] == "subscribe":
            for topic in subscription["args"]:
                self.subscribed.add(topic)
        elif subscription["op"] == "unsubscribe":
            for topic in subscription["args"]:
                if topic in self.subscribed:
                    self.subscribed.remove(topic)
        else:
            raise ValueError(f"op {subscription['op']} not supported")
        await self.ws.send_message(orjson.dumps(subscription))

    async def get_next_message(self):
        while True:
            try:
                raw_message = await self.ws.get_message()
            except ConnectionClosed as e:
                logging.error("Connection closed: %s", e)
                await self._reconnect()
                continue
            message = orjson.loads(raw_message)
            if "topic" in message and "data" in message:
                yield message
            elif "op" in message:
                if message["op"] == "pong":
                    continue
                if not message.get("success"):  # probably a subscription error
                    raise BybitWebsocketOpError(raw_message)
