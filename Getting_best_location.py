import requests
import json
import re
import geopandas
import geopy
from geopy.geocoders import Nominatim

class Getting_Best_Location():
    # initial url
    # setting the default destination address as mount fuji just to increase readibility of the get_lat_long() function,
    # it has no effect on the function
    def __init__(self,origin_addresses,destination_addresses="Mount Fuji"): 
        self.apikey="AIzaSyCJP88gPak3FtJq-ooijGdOEMa_MuknkLU"
        self.url1="https://maps.googleapis.com/maps/api/distancematrix/json?origins="
        
        # getting latitude of the origin location
        geolocator = Nominatim(user_agent="my_request")
        self.location1 = geolocator.geocode(origin_addresses)
        self.origin_addresses=str(self.location1.latitude)+"%2C"+str(self.location1.longitude)
        
        # getting latitude of the destination location
        self.url2="&destinations="
        self.location2 = geolocator.geocode(destination_addresses)
        self.destination_addresses=str(self.location2.latitude)+"%2C"+str(self.location2.longitude)

        self.url3="&mode=driving&key="
        self.fullurl=""
    
    # function for getting places latitude and longtitude, return by a list
    def get_lat_long(self):
        lat_long_list=[]
        geolocator = Nominatim(user_agent="my_request")
        lat_long_list.append(self.location1.latitude)
        lat_long_list.append(self.location1.longitude)
        return lat_long_list
        
    def valid_location(self):
        self.fullurl=self.url1+self.origin_addresses+self.url2+self.destination_addresses+self.url3+self.apikey
        # getting distance adn durationg bewteen 2 places using API
        output= requests.get(self.fullurl).json()
        print(output)
        
        for obj in output["rows"]:
            for data in obj["elements"]:
                    # getting the distance and driving duration bewteen the 2 places
                    dis= data["distance"]["text"]
                    new_dis = int(re.sub("\skm", "", dis))
                    dur =(data["duration"]["text"])
                    new_dur = re.split("\s", dur)
                    compare_dur=0
                    # converting hr to mins
                    if len(new_dur) ==4:
                        compare_dur=int(new_dur[0])*60+int(new_dur[2])
                    elif len(new_dur)==2:
                        compare_dur=int(new_dur[0])
                    # if the driving time >120 mins , it is considered as to far, it is not a feasible destination
                    if compare_dur < 120:
                        print(str(new_dis)+"km")
                        print(str(compare_dur)+"mins")
                        return True
                    else:
                        print(str(new_dis)+"km")
                        print(str(compare_dur)+"mins")
                        return False
