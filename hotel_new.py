from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import datetime
import time


district = 'Akihabara'
first_click = False

path = Service('chromedriver.exe')
driver = webdriver.Chrome(service=path)

driver.get('https://www.agoda.com/?cid=1841704')

# search for hotels in this district
search = driver.find_element(By.XPATH, '//*[@id="SearchBoxContainer"]/div[1]/div/div[2]/div/div/div[1]/div/div/input')
search.send_keys(district)

dates = driver.find_element(By.XPATH, '//*[@id="SearchBoxContainer"]/div[1]/div/div[2]/div/div/div[2]/div/div/div/div[1]')
dates.click()

dep_date = datetime.datetime(year=2022,month=11,day=21)
return_date = datetime.datetime(year=2022,month=11,day=23)

dates_list = driver.find_elements(By.CLASS_NAME, 'DayPicker-Day__label')
for this_date in dates_list:
    if this_date.text == dep_date.day and first_click == False:
        this_date.click()
        first_click = True
    elif this_date.text == return_date.day and first_click == True:
        this_date.click()

search_btm = driver.find_element(By.XPATH, '//*[@id="SearchBoxContainer"]/div[2]/button')
search_btm.click()
time.sleep(5)

most_stars = driver.find_element(By.CLASS_NAME, 'filter-item-react')  #first element
most_stars.click()
time.sleep(3)

recommand = driver.find_element(By.CLASS_NAME, 'PropertyCard__HotelName') #first hotel
recommand.click()


# tell them do it their own