from bs4 import BeautifulSoup

class Data_Parsing:
    def __init__(self, responce) -> None:
        self.response = responce
        self.soup = BeautifulSoup(self.response, 'html.parser')

class Data_Parsing_Main(Data_Parsing):

    def _search_title(self, product):
        title = product.find("span",attrs={'class' : "a-size-medium a-color-base a-text-normal"})
        return title
    
    def _search_prices(self, product):
        soup_prices_int = product.find_all("span", attrs={'class': 'a-price-whole'})
        prices_int = [int(price.text.replace('.', '').replace(',','')) for price in soup_prices_int]
        soup_prices_fract = product.find_all("span", attrs={'class': 'a-price-fraction'})
        prices_fract = [float(price.text) / 100 for price in soup_prices_fract]
        prices = [prices_int[i] + prices_fract[i] for i in range(len(prices_int))]
        if prices == []:
            return '-'
        else:
            return prices
    
    def _search_links(self, product):
        link = product.find("a",attrs={'class' : "a-link-normal s-underline-text s-underline-link-text s-link-style a-text-normal"}).get('href')
        return link
    
    def _search_link_photo(self, product):
        link_photo = product.find("img",attrs={'class' : "s-image"}).get('src')
        return link_photo
    
    def search_data(self):
        soup_product = self.soup.find_all("div",attrs={'data-component-type':"s-search-result"})
        data_product = []
        for product in soup_product:
            title = self._search_title(product)
            prices = self._search_prices(product)
            link = self._search_links(product)
            link_photo = self._search_link_photo(product)
            data_product.append({"title":title.text, "price":prices, "link" : 'https://www.amazon.com/'+link, "link_photo": link_photo})
        return data_product
    
class Data_Parsing_Product(Data_Parsing):

    def search_description(self):
        descriptions = self.soup.find_all("div", id=lambda x: x and "escription" in x)
        
        if descriptions:
            text_list = [description.text for description in descriptions]
            result = ' '.join(text_list)
            result = result.replace('\n', '').replace('  ', '')
            if result == '':
                return 'Product description is either missing or not clearly defined'
            else:
                return result
        else: 
            return 'Product description is either missing or not clearly defined'
