import datetime

from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

from get_flight_data import FlightSearch

flight_info = FlightSearch()
month_dict = {1: "January", 2: "February", 3: "March", 4: "April", 5: "May", 6: "June", \
    7: "July", 8: "August", 9: "September", 10: "October", 11: "November", 12: "December"}

path ='chromedriver.exe'
driver = webdriver.Chrome(service=path)

driver.get('https://www.cathaypacific.com/cx/en_HK/book-a-trip.html')

start_port = driver.find_element(By.XPATH, '//*[@id="depart-label"]')  # departure airport choice
start_port.send_keys(flight_info.start)
start_port.send_keys(Keys.ENTER)

end_port = driver.find_element(By.XPATH, '//*[@id="destination-label"]')  # destination airport choice
end_port.send_keys(flight_info.dest)
end_port.send_keys(Keys.ENTER)

dep_date = driver.find_element(By.XPATH, '//*[@id="dpuxzabv"]/span[2]/span[3]')  #departure date choice
dep_date.click()

# first_month = driver.find_element(By.XPATH, '//*[@id="dp1668851740859"]/div/div[1]/table/caption/span[1]')  # calender front part month
# second_month = driver.find_element(By.XPATH, '//*[@id="dp1668851740859"]/div/div[2]/table/caption/span[1]')  #calender last part month


# if first_month.text == month_dict[ flight_info.date.month]:  # departure date in first month choice

calendar_dep_day = driver.find_elements(By.CLASS_NAME, 'ui-state-default')[::-1] # inverse to make sure it's valid even when it go to second month
departure_day = flight_info.date.day
for ele in calendar_dep_day:
    if ele.text == departure_day:
        ele.click()




re_day = driver.find_element(By.XPATH, '//*[@id="dppdvs3"]/span[2]/span[3]')  # return date choice
re_day.click()

calendar_re_day = driver.find_elements(By.CLASS_NAME, 'ui-state-default')[::-1] # inverse to make sure it's valid even when it go to second month
play_duration = datetime.timedelta(days=3)
return_day = (flight_info.date + play_duration).day
for ele in calendar_re_day:
    if ele.text == return_day:
        ele.click()



