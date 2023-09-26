import aiohttp
import asyncio

class Get_Request:
    def __init__(self, config) -> None:
        self.headers = {'User-Agent': config["user-agent"], 'Accept-Language':'en-US, en;q=0.5'}
        self.session = aiohttp.ClientSession()
    
    async def get_main_page(self, url, page, sr_pg):
        url = url + f'&page={page}&qid=1695639878&ref=sr_pg_{sr_pg}'
        async with self.session.get(url=url, headers=self.headers) as response:
            return await response.text()
        
    async def get_product_page(self, url):
        async with self.session.get(url=url, headers=self.headers) as response:
            return await response.text()
        
    async def close_session(self):
        if not self.session.closed:
            await self.session.close()