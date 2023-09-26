import json
import pandas as pd

def get_config(path="./config.json"):
    config = None
    with open(path, "r") as f:
        config = json.load(f)
    return config

def sorting(data, config):
    products = []
    keys = sorted(data.keys())
    for key in keys:
        products += data[key]
    del products[-(len(products) - config["search_products"]):]
    return products

def join_data(products, descriptions):
    for index, product in enumerate(products):
        product["description"] = descriptions[index]
    return products

def create_df(products):
    for product in products:
        if product["price"] == '-':
            continue
        else:
            prices = ''
            for price in product["price"]:
                prices += f'{price}; '
            prices = prices[:-2]
            product["price"] = prices
    df = pd.DataFrame(products)
    df.to_excel('Products.xlsx', index=False)