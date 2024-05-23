from binance.streams import ReconnectingWebsocket
from binance.streams import ThreadedWebsocketManager
from binance.streams import BinanceSocketManager
from binance.streams import BinanceSocketType
from typing import Optional, Dict, Any

class SmartReconectingWebsocket(ReconnectingWebsocket):

    def __init__(self, url: str, path: Optional[str] = None, prefix: str = 'ws/', is_binary: bool = False, exit_coro=None):
        SmartReconectingWebsocket.MAX_RECONNECTS = 20
        super().__init__(url, path, prefix, is_binary, exit_coro)

class SmartBinanceSocketManager(BinanceSocketManager):

    def _get_socket(
            self, path: str, stream_url: Optional[str] = None, prefix: str = 'ws/', is_binary: bool = False,
            socket_type: BinanceSocketType = BinanceSocketType.SPOT
    ) -> SmartReconectingWebsocket:
        conn_id = f'{socket_type}_{path}'
        if conn_id not in self._conns:
            self._conns[conn_id] = SmartReconectingWebsocket(
                path=path,
                url=self._get_stream_url(stream_url),
                prefix=prefix,
                exit_coro=lambda p: self._exit_socket(f'{socket_type}_{p}'),
                is_binary=is_binary,
            )

        return self._conns[conn_id]

class SmartThreadedWebsocketManager(ThreadedWebsocketManager):

    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None,
            requests_params: Optional[Dict[str, Any]] = None, tld: str = 'com',
            testnet: bool = False, session_params: Optional[Dict[str, Any]] = None
    ):
        super().__init__(api_key, api_secret, requests_params, tld, testnet, session_params)
        self._bsm: Optional[SmartBinanceSocketManager] = None

    async def _before_socket_listener_start(self):
        assert self._client
        self._bsm = SmartBinanceSocketManager(client=self._client)