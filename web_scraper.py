import requests
import time, random
import re

class CoinMarketCapScraper:
    """Scraper for CoinMarketCap"""
    def __init__(self, pages):
        self.base_url = "https://coinmarketcap.com/"
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Referer": "https://www.google.com/",
        }
        self.pages = pages
        self.coins = []

    def __fetch_page(self, page):
        """Fetch the HTML content of a CoinMarketCap page."""
        
        url = f"{self.base_url}?page={page}"
        try:
            response = requests.get(url, headers=self.headers)
            response.raise_for_status()
            return response.text
        except requests.exceptions.RequestException as e:
            print(f"Error fetching page {page}: {e}")
            return None

    def __get_fields(self, current_data):
        """Finds all the data for each field using regex and returns a list of a list"""
        ret_data = []
        
        names = []
        coin_sym = [] 
        price = [] 
        circulating_supply = []

        for data in current_data:
            names.append(re.findall(r'coin-item-name">.*?</', data))
            coin_sym.append(re.findall(r'coin-item-symbol">.*?</', data))
            price.append(re.findall(r'an>\$.*?</spa',data))
            circulating_supply.append(re.findall(r'class="circulating-supply-value"><span>.*?</sp', data))

        ret_data.append(names)
        ret_data.append(coin_sym)
        ret_data.append(price)
        # ret_data.append()
        # ret_data.append()
        ret_data.append(circulating_supply)
        
         #the index will be the same for the same rec
        return ret_data

    def __cut_down_html(self, html):
        """Cuts down large html down to the html for the crypto-coins"""
        
        cut_data = re.findall(r'<tr style=\"cursor:pointer\">.*?</tr>', html)
    
        return cut_data

    def __fix_circ_supply(self, current_data):
        """Fix for Circulating Supply Field to get the data"""
        
        temp = current_data[-1]

        for i in range(len(temp)):
            for j in range(len(temp[i])):
                temp[i][j] = temp[i][j].split('<span>')[1]
                temp[i][j] = temp[i][j].split('<')[0]
        
        current_data[-1] = temp
        return current_data

    def __sanatize_data(self,current_data): 
        """Takes a list of lists, and breaks it down to the main information"""
        
        for i in range(len(current_data)-1):
            for j in range(len(current_data[i])):
                for q in range(len(current_data[i][j])):
                    try:
                        item = current_data[i][j][q]

                        # If '>' exists, get everything after it
                        if '>' in item:
                            item = item.split('>', 1)[-1]

                        # If '<' exists, get everything before it
                        if '<' in item:
                            item = item.split('<', 1)[0]

                        # Trim whitespace
                        current_data[i][j][q] = item.strip()

                    except Exception as e:
                        print(f"ERROR FOUND IN San' Data: {e}")
        current_data = self.__fix_circ_supply(current_data)
        return current_data

    def __data_resolve(self, current_data):
        """Cleans up data given"""
        cleaned_up_data = [[item[0] for item in category] for category in current_data]

        coin_lst = []

        
        for i in range(len(cleaned_up_data[0])):
            str_coin = []
            for j in range(len(cleaned_up_data)):
                    str_coin.append(cleaned_up_data[j][i])

            #str_coin = str_coin.rstrip(',')
            coin_lst.append(str_coin)
    
        return coin_lst

    def __parse_page(self, html):
        """Series of functions to clean data, step by step"""
        data = self.__cut_down_html(html)
        data = self.__get_fields(data)
        data = self.__sanatize_data(data)
        data = self.__data_resolve(data)

        return data

    def scrape(self):
        """Run the scraping process for multiple pages."""
        
        for page in range(1, self.pages + 1):
            print(f"Scraping page {page}...")
            html = self.__fetch_page(page)

            if html:
                self.coins = self.__parse_page(html)
            
            time.sleep(random.uniform(3, 6))  # Avoid getting blocked

        return self.coins