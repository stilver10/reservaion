import aiohttp
import asyncio
import time
from typing import Tuple

session = None

async def open_session():
    global session
    if session is None:
        session = aiohttp.ClientSession()

async def close_session():
    global session
    if session is not None:
        await session.close()
        session = None

async def get_server_time(url: str) -> Tuple[str, float]:
    global session
    if session is None:
        await open_session()
    start_time = time.time()
    async with session.head(url) as response:
        end_time = time.time()
        server_time = response.headers['Date']
        ping = end_time - start_time
        return server_time, ping

if __name__ == "__main__":
    url = 'https://app.catchtable.co.kr'
    async def main():
        await open_session()
        server_time, ping = await get_server_time(url)
        print("Catch Table 서버 시간:", server_time)
        print("핑:", ping)
        await close_session()
    asyncio.run(main())
