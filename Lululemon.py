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

url = "https://shop.lululemon.com/c/men/_/N-7qr"
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
#driver.get("https://www.google.com")
driver.get(url)


#get scroll height
last_height = driver.execute_script("return document.body.scrollHeight")

y = 50
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
        loadMoreButton = driver.find_element(By.CSS_SELECTOR, 'div.iconButtonContent-29UhU')
        time.sleep(2)
    except:
        break
    else:
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
###

###item links
item_links = []
for items in item_tiles:
    item_links.append(url+items.attrs['href'])
print(item_links)
###

###item prices
item_prices_container = soup.findAll('span',class_='price-1jnQj price')
item_prices = []
for items in item_prices_container:
    price_box = items.contents[0].contents
    if len(price_box) > 1:
        combined = price_box[0]+"-"+price_box[2]
        item_prices.append(combined)
    #item_prices.append(price_box[0]+price_box[2])
    if price_box[0] == 'Sale Price\xa0':
        sale_box = items.contents[2].contents
        item_prices.append(sale_box)
    else:
        item_prices.append(price_box[0])
print(item_prices)
####################



"""print(soup.find('product-tile-image').attrs['base'])"""


#print(response.status_code)
