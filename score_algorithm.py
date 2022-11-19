import requests
import json
import re
import geopandas
import geopy
from geopy.geocoders import Nominatim

class Getting_Best_Location():
    # initial url
    def __init__(self,origin_addresses,destination_addresses):
        self.apikey="AIzaSyCJP88gPak3FtJq-ooijGdOEMa_MuknkLU"
        self.url1="https://maps.googleapis.com/maps/api/distancematrix/json?origins="
        
        # getting latitude of the origin location
        geolocator = Nominatim(user_agent="my_request")
        location1 = geolocator.geocode(origin_addresses)
        self.origin_addresses=str(location1.latitude)+"%2C"+str(location1.longitude)
        
        # getting latitude of the destination location
        self.url2="&destinations="
        location2 = geolocator.geocode(destination_addresses)
        self.destination_addresses=str(location2.latitude)+"%2C"+str(location2.longitude)

        self.url3="&mode=driving&key="
        self.fullurl=""
        
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


#https://en.wikipedia.org/wiki/Category:Tourist_attractions
# We determine the duration of staying in each destination by its category (destination_type), 
# we reference these data from wikipedia, but we only use the relavent ones in our prototype
category_duration = {"Museums":2, "Entertainment districts":6, "Entertainment events":2, "Shopping malls":3, "Scenic viewpoints":2}

#class for destinations 
class destinations:
    def __init__(self, name,out_or_in, popular_or_local, people_going_with_type, budget_used, destination_type):
        self.name = name
        self.out_or_in = out_or_in
        self.popular_or_local = popular_or_local
        self.people_going_with_type = people_going_with_type
        self.budget_used = budget_used
        self.destination_type = destination_type
        self.duration = category_duration[destination_type]
 
#sample destinations
#assumptions in our prototype:
#only 3 types of travellers: Friends, Family, Couples, Individual
#Only 4 natures of destination: Play, Shopping, Nature, Culture
disney = destinations(name="Tokyo Disneyland", out_or_in="out", popular_or_local="popular",people_going_with_type= ["Friends","Family","Couples"],
                        budget_used= 500, destination_type="Entertainment districts")

aqua_city = destinations(name="Aqua City Odaiba", out_or_in="out", popular_or_local="popular",people_going_with_type= ["Family","Couples"],
                        budget_used= 300, destination_type="Shopping malls")

mount_fuji = destinations(name="Mount Fuji", out_or_in="out", popular_or_local="popular",people_going_with_type= ["Couples","Individual"],
                         budget_used= 100, destination_type="Scenic viewpoints")

funabashi_andersen_park = destinations(name="Funabashi Andersen Park", out_or_in="out", popular_or_local="local",people_going_with_type= ["Couples","Family"],
                        budget_used= 50, destination_type="Scenic viewpoints")

edo_museum = destinations(name="Edo-Tokyo Open Air Architectural Museum", out_or_in="in", popular_or_local="local",people_going_with_type= ["Couples","Family", "Individual"],
                        budget_used= 100, destination_type="Museums")

tokyo_museum = destinations(name="Tokyo National Museum", out_or_in="in", popular_or_local="popular",people_going_with_type= ["Couples","Family", "Individual"],
                        budget_used= 100, destination_type="Museums")

ginza = destinations(name="Ginza", out_or_in="in", popular_or_local="popular",people_going_with_type= ["Couples","Friends","Family"],
                        budget_used= 500, destination_type="Shopping malls")

akihabara = destinations(name="Akihabara", out_or_in="in", popular_or_local="popular",people_going_with_type= ["Friends", "Family", "Individual"],
                        budget_used= 400, destination_type="Shopping malls")

Mannen_onsen = destinations(name="Mannen-yu onsen", out_or_in="in", popular_or_local="local",people_going_with_type= ["Couples"],
                        budget_used= 200, destination_type="Entertainment events")

#class for travellers 
class travel_input:
    def __init__(self, know_destination, destination, duration, budget_per_day, people_going_with, indoor, popular_locations, trip_focus):
        self.know_destination = know_destination
        self.destination = destination
        self.duration = duration
        self.budget_per_day = budget_per_day
        self.people_going_with = people_going_with
        self.indoor = indoor
        self.popular_locations = popular_locations
        self.trip_focus = trip_focus
        self.total_budget = duration*budget_per_day

    #generating the itinerary by calculating scores and filtering
    def generate_itinerary(self):
        all_destinations = [disney, mount_fuji, aqua_city, funabashi_andersen_park, edo_museum, tokyo_museum, ginza, akihabara, Mannen_onsen]
        #score calulation
        changing_budget = self.total_budget
        DURATION_EACH_DAY = 10
        MAX_DESTINATION_PER_DAY = 2
        MAX_BUDGET_PER_DEST = 1000
        num_destinations = self.duration*MAX_DESTINATION_PER_DAY 
        destination_points = {}
        HOTEL = "Tokyo Bay Shiomi Prince Hotel, 2 Chome-8-16 潮見江東區東京都日本" #hotel based on users choice

        #We use the following algorithm to calculate the total score
        #
        for i in range(len(all_destinations)):
            if (all_destinations[i].budget_used > changing_budget #over-budget then swap to another location 
                and Getting_Best_Location(all_destinations[i].name, HOTEL).valid_location()): #make sure the time distance between the destination and hotel < 2 hours
                continue
            else:
                if (all_destinations[i].people_going_with_type == self.people_going_with): #types of travellers
                    people_going_with_score = 10 #for making the maximum total score be 10
                else:
                    people_going_with_score = 3 #because 0.4*3 - 1.2 > 1 (minimum sum of three other factors -> dominate other choices in the worst case)

                #trip focus
                if (all_destinations[i].destination_type == "Museums"):
                    trip_focus_score = self.trip_focus["Culture"] 
                elif (all_destinations[i].destination_type == "Entertainment districts" or all_destinations[i].destination_type == "Entertainment events"):
                    trip_focus_score = self.trip_focus["Entertainment"]
                elif (all_destinations[i].destination_type == "Shopping malls"):
                    trip_focus_score = self.trip_focus["Shopping"]
                elif (all_destinations[i].destination_type == "Scenic viewpoints"):
                    trip_focus_score = self.trip_focus["Nature"]
            
                if (all_destinations[i].out_or_in == "in"): #indoor or outdoor
                    out_or_in_score = self.indoor
                elif (all_destinations[i].out_or_in == "out"):
                    out_or_in_score = 10 - self.indoor

                if (all_destinations[i].popular_or_local == "popular"): #popular or local
                    popular_or_local_score = self.popular_locations
                elif (all_destinations[i].out_or_in == "local"):
                    popular_or_local_score = 10 - self.popular_locations
                
                budget_score = 10* (1- all_destinations[i].budget_used/MAX_BUDGET_PER_DEST) #the lower the budget used the better

                total_score =  0.4 * people_going_with_score + 0.3 * (2.5*trip_focus_score) + 0.1 * out_or_in_score + 0.1 * popular_or_local_score + 0.1* budget_score

                destination_points[all_destinations[i].name] = total_score

        confirmed_destination = []
        #confirm where are we going
        for i in range(num_destinations):
            for key in destination_points.keys():
                if destination_points[key] == max(destination_points.values()):
                    destination_points[key] = 0
                    confirmed_destination.append(key)
                    break
        


        itinerary_destinations = {}
        copy_of_confirmed_destination = confirmed_destination
        varying_len_confirmed_destination = len(copy_of_confirmed_destination)
        print(copy_of_confirmed_destination)

        for i in range(1,self.duration+1):
            this_day_duration = 0
            destination_count = 0
            itinerary_destinations["day" + str(i)] = []
     
            while (destination_count < MAX_DESTINATION_PER_DAY):
                # assign attractions for every day
                if (varying_len_confirmed_destination == 0):
                    break

                for k in range(len(all_destinations)):
                        assigned_location = copy_of_confirmed_destination[0]
                        if (all_destinations[k].name == assigned_location):
                            if (this_day_duration + all_destinations[k].duration) <= DURATION_EACH_DAY:
                                this_day_duration += all_destinations[k].duration
                                copy_of_confirmed_destination.remove(assigned_location)
                                itinerary_destinations["day" + str(i)].append(assigned_location)
                                varying_len_confirmed_destination -= 1
                                destination_count += 1
                                break
             
             
        return itinerary_destinations #return itinerary planned




#run with sample input
sample = travel_input(know_destination=True, destination="Tokyo", duration=3,budget_per_day=2000, 
                    people_going_with="Family", indoor=6, popular_locations= 8,trip_focus= {"Shopping":4,"Entertainment":3,"Nature":2,"Culture":1})
            
itinerary = sample.generate_itinerary()
print(itinerary)


                

                




        




                        
                    
                    
                    

                            

                




