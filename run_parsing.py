from data_parsing.get_request import Get_Request
from data_parsing.utils import get_config, sorting, join_data, create_df
from data_parsing.tasks import Tasks
from data_parsing.data_parsing import Data_Parsing_Main

import asyncio

async def main():
    try:    
        config = get_config()
        task_main = Tasks(config)

        tasks = []
        for i in range(1, config["search_products"] // 16 + 2):
            task = task_main.parsing_main(config["url"], i)
            tasks.append(task)

        await asyncio.gather(*tasks)
        await task_main.close()

        data = task_main.get_products()
        products = sorting(data, config)

        tasks = []
        task_description = Tasks(config)

        for index, product in enumerate(products):
            task = task_description.parsing_product(url = product["link"], index=index)
            tasks.append(task)
        
        await asyncio.gather(*tasks)
        await task_description.close()

        descriptions = task_description.get_descriptions()
        products = join_data(products=products, descriptions=descriptions)
        if products == []:
            print('<Response [503]> Amazon не готов обработать данные, нужно попробовать позже или еще раз')
        else:
            create_df(products=products)
    except Exception:
        print('Что то пошло не так, попробуйте перезапустить программу')


if __name__ == '__main__':
    asyncio.run(main())
    print('THE END!!')
