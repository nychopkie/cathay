import requests
import json
import re
import geopandas
import geopy
from geopy.geocoders import Nominatim

#our own modules
from Getting_best_location import *
from getting_restaurant import *


# https://en.wikipedia.org/wiki/Category:Tourist_attractions
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
 
# sample destinations
# assumptions in our prototype:
# Only 3 types of travellers: Friends, Family, Couples, Individual
# Only 4 natures of destination: Play, Shopping, Nature, Culture
# These should be stored in a DBMS in future development
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

Mannen_onsen = destinations(name="Mannenyu", out_or_in="in", popular_or_local="local",people_going_with_type= ["Couples"],
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

        #based on our area searching algorithm 
        #Find the centre of the location
        centre_lat = 0
        centre_long = 0
        cannot_search = 0

        #there may exists some destinations that cannot be searched on the google map, we exclude those destinations
        for i in all_destinations:
            try:
                loc = Getting_Best_Location(i.name)
                cur_lat_long = loc.get_lat_long()
                centre_lat += cur_lat_long[0]
                centre_long += cur_lat_long[1]
            except:
                cannot_search += 1
        
        centre_lat /= (len(all_destinations)-cannot_search)
        centre_long /= (len(all_destinations)-cannot_search)

        #Since we do not have access to the key of the API, the algorithm cannot be run
        # ---------------- Running algo --------------------"
        # Return HOTEL

        #In this sample case, we select a hotel manually to replace the return value of the algorithm
        HOTEL = "Tokyo Bay Shiomi Prince Hotel, 2 Chome-8-16 潮見江東區東京都日本" 

        #We use the following algorithm to calculate the total score
        #we rank the importance of the scoring factors as 
        #traveller type > focus of the trip > indoor/outdoor = popular/local = cost effective
        #hence we decided to allocate the weight as 0.4, 0.3, 0.1, 0.1, 0.1 respectively
        for i in range(len(all_destinations)):
            if (all_destinations[i].budget_used > changing_budget #over-budget then swap to another location 
                and Getting_Best_Location(all_destinations[i].name, HOTEL).valid_location()): #make sure the time distance between the destination and hotel < 2 hours
                continue
            else:
                if (all_destinations[i].people_going_with_type == self.people_going_with): #types of travellers
                    people_going_with_score = 10 #for making the maximum total score be 10
                else:
                    people_going_with_score = 3 
                    #should not be too low because some places may attract their non-target group of travellers

                #calculating trip_focus score
                if (all_destinations[i].destination_type == "Museums"):
                    trip_focus_score = self.trip_focus["Culture"] 
                elif (all_destinations[i].destination_type == "Entertainment districts" or all_destinations[i].destination_type == "Entertainment events"):
                    trip_focus_score = self.trip_focus["Entertainment"]
                elif (all_destinations[i].destination_type == "Shopping malls"):
                    trip_focus_score = self.trip_focus["Shopping"]
                elif (all_destinations[i].destination_type == "Scenic viewpoints"):
                    trip_focus_score = self.trip_focus["Nature"]
            
                if (all_destinations[i].out_or_in == "in"): #indoor or outdoor score
                    out_or_in_score = self.indoor
                elif (all_destinations[i].out_or_in == "out"):
                    out_or_in_score = 10 - self.indoor

                if (all_destinations[i].popular_or_local == "popular"): #popular or local destinations score
                    popular_or_local_score = self.popular_locations
                elif (all_destinations[i].out_or_in == "local"):
                    popular_or_local_score = 10 - self.popular_locations
                
                budget_score = 10* (1- all_destinations[i].budget_used/MAX_BUDGET_PER_DEST) #the lower the budget used the better

                # our formula to calculate the total_score for a destination
                # we multiply trip_focus_score by 2.5 because the range of trip_focus_score is [1,4], and we would like to scale it up to [2.5,10]
                # the maximum value of total score is 10
                # the minimum value of total score is 2.2
                total_score =  0.4 * people_going_with_score + 0.3 * (2.5*trip_focus_score) + 0.1 * out_or_in_score + 0.1 * popular_or_local_score + 0.1* budget_score
                
                destination_points[all_destinations[i].name] = total_score

        confirmed_destination = []
        #confirm where are we going, sorted by total scores of destination in descending order
        for i in range(num_destinations):
            for key in destination_points.keys():
                if destination_points[key] == max(destination_points.values()):
                    destination_points[key] = 0
                    confirmed_destination.append(key)
                    break
        

        #create the dictionary story the destination we are going to each day, collected from the confirmed_destination list
        itinerary_destinations = {}
        copy_of_confirmed_destination = confirmed_destination
        varying_len_confirmed_destination = len(copy_of_confirmed_destination)

        for i in range(1,self.duration+1):
            this_day_duration = 0
            destination_count = 0
            itinerary_destinations["day" + str(i)] = []
     
            while (destination_count < MAX_DESTINATION_PER_DAY):
                # assign attractions for every day
                if (varying_len_confirmed_destination == 0):
                    break
                
                # we always append the first value of the list first because the score is the highest
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
             
        return itinerary_destinations



#run with sample input
sample = travel_input(know_destination=True, destination="Tokyo", duration=3,budget_per_day=2000, 
        people_going_with="Family", indoor=6, popular_locations= 8,trip_focus= {"Shopping":4,"Entertainment":3,"Nature":2,"Culture":1})

itinerary = sample.generate_itinerary()
print(itinerary)


                

                




        




                        
                    
                    
                    

                            

                




