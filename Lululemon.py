from random import seed
import matplotlib.pyplot as plt
import matplotlib.image as mpim
import pandas as pd
from IPython.display import Image, HTML
import time
from bs4 import BeautifulSoup
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
import re

url = "https://shop.lululemon.com/c/men/_/N-7qr"
#url = "https://shop.lululemon.com/c/women/_/N-7z5"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#driver.get("https://www.google.com")
driver.get(url)

#get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

y = 50
b = 0
scroll_pause_time = 0.1
while True:
    while True:
        # Scroll down to bottom
        driver.execute_script("window.scroll(0, "+str(y)+");")

        # Wait to load page
        time.sleep(scroll_pause_time)

        # Calculate new scroll height and compare with last scroll height
        new_height = driver.execute_script("return document.body.scrollHeight")
        if y >= last_height: #if we scroll past the bottom, stop scrolling
            break
        last_height = new_height
        y = y + 100
    y = y-1500
    try:
        if b == y:
            break
        b = y
        loadMoreButton = driver.find_element(By.CSS_SELECTOR, 'div.iconButtonContent-29UhU')
        time.sleep(2)
    except:
        break
    else:
        time.sleep(0.5)
        loadMoreButton.click()

html = driver.page_source
#session_obj = requests.Session()
#response = session_obj.get(url, headers={"User-Agent": "Mozilla/5.0"}) #I don't know if this will be useful later
#soup = BeautifulSoup(response.content,'html.parser')
soup = BeautifulSoup(html, "html.parser")

#things to find
####################

###item names
item_tiles = soup.findAll('a',class_='link lll-font-weight-medium')
item_names = []
for items in item_tiles:
    item_names.append(items.contents[0])
print(item_names)
print('# of items = ' ,len(item_names))
###

###item pics
"""
item_pics = []
#item_pictures = re.findall("(srcset=\".+\s320w)",str(soup.findAll('span', class_='lazyImageContainer-2KFMN')[0].contents))[0][7:-4]
item_pictures = soup.findAll('span', class_='lazyImageContainer-2KFMN')

for items in item_pictures:
    item_pics.append('0')
print('# of pics = ' ,len(item_pics))
"""
###

###item prices
temp = []
item_prices_container = soup.findAll('span',class_='price-1jnQj price')
item_prices = []
for items in item_prices_container:
    price_box = items.contents[0].contents
    try:
        a = str(items.contents[0].contents[1])
    except:
        a = "error"
    if len(price_box) > 1 and a =='<span aria-label="to"> - </span>':
        combined = price_box[0]+"-"+price_box[2]
        item_prices.append(combined)
    #item_prices.append(price_box[0]+price_box[2])
    elif price_box[0] == 'Sale Price\xa0':
        sale_box = items.contents#.contents
        item_prices.append(re.findall(r'[$]\d+',str(items.contents[1]))[0] + '<' + re.findall(r'[$]\d+',str(items.contents[3]))[0])
    else:
        item_prices.append(price_box[0])
print(item_prices)
print('# of prices = ' ,len(item_prices))
####################

###Item availablility
links = []
item_link_container = soup.findAll('a',class_='link product-tile__image-link')

for items in item_link_container:
    links.append(url[:-14] + items.attrs['href'])

print(links)
print('# of links = ' ,len(links))
####################

###Item type
types = []
item_type_container = soup.findAll('a',class_='link product-tile__image-link')

for items in item_type_container:
    types.append(items.attrs['data-categoryunifiedid'])

print(types)
print('# of types = ' ,len(types))
####################

pd.set_option('display.max_columns', None)
"""print(soup.find('product-tile-image').attrs['base'])"""
df = pd.DataFrame()
df['Name'] = item_names
df['Price'] = item_prices
df['Links'] = links
df['Types'] = types

print(df)
#print(response.status_code)
