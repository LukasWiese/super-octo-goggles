from random import seed
import matplotlib.pyplot as plt
import matplotlib.image as mpim
import pandas as pd
from IPython.display import Image, HTML
from bs4 import BeautifulSoup
import requests
import re

url = "https://shop.lululemon.com/c/men/_/N-7qr"
session_obj = requests.Session()
response = session_obj.get(url, headers={"User-Agent": "Mozilla/5.0"})
soup = BeautifulSoup(response.content,'html.parser')

###item names
item_tiles = soup.findAll('a',class_='link lll-font-weight-medium')
item_names = []
for items in item_tiles:
    item_names.append(items.contents)
print(item_names)
###

###item link
item_links = []
for items in item_tiles:
    item_links.append(items.attrs['href'])
print(item_links)
###

###item prices
item_prices_container = soup.findAll('span',class_='price-1jnQj price')
item_prices = []
for items in item_prices_container:
    price_box = items.contents[0].contents
    item_prices.append(price_box[0]+price_box[2])
print(item_prices)

"""print(soup.find('product-tile-image').attrs['base'])"""


print(response.status_code)
