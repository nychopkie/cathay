from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import datetime

district = ''
monthDict={1:'Jan', 2:'Feb', 3:'Mar', 4:'Apr', 5:'May', 6:'Jun', 7:'Jul', 8:'Aug', 9:'Sep', 10:'Oct', 11:'Nov', 12:'Dec'}


go_date = datetime.datetime(year=2022, month=11, day=21)
back_date = datetime.datetime(year=2022, month=11, day=23)


path = Service('chromedriver.exe')
driver = webdriver.Chrome(service=path)

driver.get('https://www.agoda.com/?cid=1841704')

# search for hotels in this district
search = driver.find_element(By.XPATH, '//*[@id="SearchBoxContainer"]/div[1]/div/div[2]/div/div/div[1]/div/div/input')
search.send_keys(district)

# tell them do it their own
