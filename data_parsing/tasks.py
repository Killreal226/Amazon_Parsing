import asyncio
import aiohttp

from .get_request import Get_Request
from .data_parsing import Data_Parsing_Main, Data_Parsing_Product

class Tasks:
    def __init__(self, config):
        self.http_request = Get_Request(config)
        self.products = {}
        self.descriptions = {}
    
    async def parsing_main(self, url, index):
        response = await self.http_request.get_main_page(url, index, index)
        data_parsing_main = Data_Parsing_Main(response)
        product = data_parsing_main.search_data()
        self.products[index] = product 

    async def parsing_product(self, url, index):
        response = await self.http_request.get_product_page(url)
        data_parsing_product = Data_Parsing_Product(response)
        description = data_parsing_product.search_description()
        self.descriptions[index] = description

    async def close(self):
        await self.http_request.close_session()

    def get_products(self):
        return self.products
    
    def get_descriptions(self):
        return self.descriptions




