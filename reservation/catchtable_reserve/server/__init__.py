from typing import Tuple
from catchtable_reserve.server.request import get_server_time, open_session, close_session
from catchtable_reserve.server.translate_datetime import translate_to_kst

class Server:
    def __init__(self, url):
        self.url = url

    async def open_session(self):
        await open_session()

    async def close_session(self):
        await close_session()

    async def get_server_time(self) -> Tuple[str, float]:
        server_time, ping = await get_server_time(self.url)
        return server_time, ping

    def translate_to_kst(self, server_time_str):
        server_time_kst = translate_to_kst(server_time_str)
        return server_time_kst