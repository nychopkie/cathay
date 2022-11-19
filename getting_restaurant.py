import requests
import json
from geopy.geocoders import Nominatim

# This file is getting the site restaurant using Google Map API
class get_restaurant():
    def __init__(self,lat,long):
        self.lat=str(lat)
        self.long=str(long)
        self.url1="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="
        self.url2="%2C"
        self.url3="&radius=3000&type=restaurant&key="
        self.api="AIzaSyAL0Uvqhy2_xYiSyjmOEvID784e67a60Gs"
        
        #generate the url
        self.url=self.url1+self.lat+self.url2+self.long+self.url3+self.api

    def find_restaurant(self):
        result_list=[]
        response = requests.get(self.url)
        data = response.json()
        for i in data['results']:
            
            # filter the restaurant with rating < 3.5
            if(i['rating']>3.5):
                # name of the restaurant
                result_list.append(i['name'])
                # latitude of the restaurant
                result_list.append(i['geometry']['location']['lat'])
                # longtitude of the restaurant
                result_list.append(i['geometry']['location']['lng'])
                # rating of the restaurant
                result_list.append(i['rating'])
        return result_list
        

# sample output e.g. Aqua City
# x = get_restaurant(35.627948, 139.773834,).find_restaurant()
# print(x)