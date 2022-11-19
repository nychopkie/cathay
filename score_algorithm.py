
#https://en.wikipedia.org/wiki/Category:Tourist_attractions
# We determine the duration of staying in each destination by its category (destination_type), 
# we reference these data from wikipedia, but we only use some of them in our prototype
category_duration = {"Museums":2, "Entertainment districts":6, "Entertainment events":2, "Shopping malls":3, "Scenic viewpoints":2}
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
#assumptions:
#only 3 types of travellers: Friends, Family, Couples
#Only 4 natures of destination: Play, Shopping, Nature, Culture
disney = destinations(name="Tokyo Disneyland", out_or_in="out", popular_or_local="popular",people_going_with_type= ["Friends","Family","Couples"],
                        budget_used= 500, destination_type="Entertainment districts")

aqua_city = destinations(name="Aqua City Odaiba", out_or_in="out", popular_or_local="popular",people_going_with_type= ["Family","Couples"],
                        budget_used= 300, destination_type="Shopping malls")

universal_studios = destinations(name="Tokyo Universal Studios", out_or_in="out", popular_or_local="popular",people_going_with_type= ["Friends","Family","Couples"],
                        budget_used= 500, destination_type="Entertainment districts")

mount_fuji = destinations(name="Mount Fuji", out_or_in="out", popular_or_local="popular",people_going_with_type= ["Couples"],
                         budget_used= 100, destination_type="Scenic viewpoints")

funabashi_andersen_park = destinations(name="Funabashi Andersen Park", out_or_in="out", popular_or_local="local",people_going_with_type= ["Couples","Family"],
                        budget_used= 50, destination_type="Scenic viewpoints")

edo_museum = destinations(name="Edo-Tokyo Open Air Architectural Museum", out_or_in="in", popular_or_local="local",people_going_with_type= ["Couples","Family"],
                        budget_used= 100, destination_type="Museums")

tokyo_museum = destinations(name="Tokyo National Museum", out_or_in="in", popular_or_local="popular",people_going_with_type= ["Couples","Family"],
                        budget_used= 100, destination_type="Museums")

ginza = destinations(name="Ginza", out_or_in="in", popular_or_local="popular",people_going_with_type= ["Couples","Friends","Family"],
                        budget_used= 500, destination_type="Shopping malls")

akihabara = destinations(name="Akihabara", out_or_in="in", popular_or_local="popular",people_going_with_type= ["Friends"],
                        budget_used= 500, destination_type="Shopping malls")

Mannen_onsen = destinations(name="Mannen-yu onsen", out_or_in="in", popular_or_local="local",people_going_with_type= ["Couples"],
                        budget_used= 200, destination_type="Entertainment events")

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

    # #Sample input
    # sample = travel_input(know_destination=True, destination="Tokyo", duration=3,budget_per_day=2000, 
    #         people_going_with="Family", indoor=6, popular_locations= 8,trip_focus= {"Shopping":4,"Entertainment":3,"Nature":2,"Culture":1})

    def generate_itinerary(self):
        
        all_destinations = [disney, universal_studios, mount_fuji, aqua_city, funabashi_andersen_park, edo_museum, tokyo_museum, ginza, akihabara, Mannen_onsen]
        #score calulation
        changing_budget = self.total_budget
        DURATION_EACH_DAY = 10
        MAX_DESTINATION_PER_DAY = 2
        num_destinations = self.duration*MAX_DESTINATION_PER_DAY #two destinations per day
        destination_points = {}

        for i in range(len(all_destinations)):
            if (all_destinations[i].budget_used > changing_budget):
                continue
            else:
                if (all_destinations[i].people_going_with_type == self.people_going_with): #people going with
                    people_going_with_score = 10
                else:
                    people_going_with_score = 3 #because 0.4*3 - 1.2 > 1 (minimum sum of three other factors)

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
                
                total_score =  0.4 * people_going_with_score + 0.3 * (2.5*trip_focus_score) + 0.15 * out_or_in_score + 0.15 * popular_or_local_score

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


        for i in range(1,self.duration+1):
            this_day_duration = 0
            destination_count = 0
            varying_len_confirmed_destination = len(copy_of_confirmed_destination)
            itinerary_destinations["day" + str(i)] = []

            for j in range(varying_len_confirmed_destination):
                if (this_day_duration >= DURATION_EACH_DAY or destination_count >= 2):
                    break

            # assign attractions for every day 
            for i in range(1,self.duration+1):
                itinerary_destinations["day" + str(i)]=[]
                for j in range(MAX_DESTINATION_PER_DAY):
                    if i==1 and j==0:
                        itinerary_destinations["day" + str(i)].append(copy_of_confirmed_destination[0])
                    else:    
                        itinerary_destinations["day" + str(i)].append(copy_of_confirmed_destination[i+j*2])

        return itinerary_destinations






#run 
#disney vs universal
#distance formula

sample = travel_input(know_destination=True, destination="Tokyo", duration=3,budget_per_day=2000, 
                    people_going_with="Family", indoor=6, popular_locations= 8,trip_focus= {"Shopping":4,"Entertainment":3,"Nature":2,"Culture":1})
            
itinerary = sample.generate_itinerary()
print(itinerary)


                

                




        




                        
                    
                    
                    

                            

                




