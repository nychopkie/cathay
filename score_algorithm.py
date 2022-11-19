# variable declaration
class destinations:
    def __init__(self, name,out_or_in, popular_or_local, people_going_with_type, budget_used, destination_type):
        self.name = name
        self.out_or_in = out_or_in
        self.popular_or_local = popular_or_local
        self.people_going_with_type = people_going_with_type
        self.budget_used = budget_used
        self.destination_type = destination_type
    
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



#sample destinations
#assumptions:
#only 3 types of travellers: Friends, Family, Couples
#Only 4 natures of destination: Play, Shopping, Nature, Culture

disney = destinations(name="Tokyo Disneyland", out_or_in="out", popular_or_local="popular",people_going_with_type= ["Friends","Family","Couples"],
                        budget_used= 500, destination_type="Play")

aqua_city = destinations(name="Aqua City Odaiba", out_or_in="out", popular_or_local="popular",people_going_with_type= ["Family","Couples"],
                        budget_used= 300, destination_type="Shopping")

universal_studios = destinations(name="Universal Studios", out_or_in="out", popular_or_local="popular",people_going_with_type= ["Friends","Family","Couples"],
                        budget_used= 500, destination_type="Play")

mount_fuji = destinations(name="Mount Fuji", out_or_in="out", popular_or_local="popular",people_going_with_type= ["Family","Couples"],
                        budget_used= 100, destination_type="Nature")

funabashi_andersen_park = destinations(name="Funabashi Andersen Park", out_or_in="out", popular_or_local="local",people_going_with_type= ["Couples","Family"],
                        budget_used= 50, destination_type="Nature")

edo_museum = destinations(name="Edo-Tokyo Open Air Architectural Museum", out_or_in="in", popular_or_local="local",people_going_with_type= ["Couples","Family"],
                        budget_used= 100, destination_type="Culture")

tokyo_museum = destinations(name="Tokyo National Museum", out_or_in="in", popular_or_local="popular",people_going_with_type= ["Couples","Family"],
                        budget_used= 100, destination_type="Culture")

ginza = destinations(name="Ginza", out_or_in="in", popular_or_local="popular",people_going_with_type= ["Couples","Friends","Family"],
                        budget_used= 500, destination_type="Shopping")

akihabara = destinations(name="Akihabara", out_or_in="in", popular_or_local="popular",people_going_with_type= ["Friends"],
                        budget_used= 500, destination_type="Shopping")

Mannen_onsen = destinations(name="Mannen-yu onsen", out_or_in="in", popular_or_local="local",people_going_with_type= ["Couples"],
                        budget_used= 200, destination_type="Play")

all_destinations = [disney, aqua_city, universal_studios, mount_fuji, funabashi_andersen_park, edo_museum, tokyo_museum, ginza, akihabara, Mannen_onsen]



#Sample input
sample = travel_input(know_destination=True, destination="Tokyo", duration=3,budget_per_day=2000, 
            people_going_with="Family", indoor=6, popular_locations= 8,trip_focus= {"Shopping":4,"Play":3,"Nature":2,"Culture":1})


#score calulation
changing_budget = sample.total_budget
num_destinations = sample.duration*2 #two destinations per day
destination_points = {}

for i in range(len(all_destinations)):
    if (all_destinations[i].budget_used > changing_budget):
        continue
    else:
        if (all_destinations[i].people_going_with_type == sample.people_going_with): #people going with
            people_going_with_score = 10
        else:
            people_going_with_score = 3 #because 0.4*3 - 1.2 > 1 (minimum sum of three other factors)

        trip_focus_score = sample.trip_focus[all_destinations[i].destination_type] #trip focus

        if (all_destinations[i].out_or_in == "in"): #indoor or outdoor
            out_or_in_score = sample.indoor
        elif (all_destinations[i].out_or_in == "out"):
            out_or_in_score = 10 - sample.indoor

        if (all_destinations[i].popular_or_local == "popular"): #popular or local
            popular_or_local_score = sample.popular_locations
        elif (all_destinations[i].out_or_in == "local"):
            popular_or_local_score = 10 - sample.popular_locations
        
        total_score =  0.4 * people_going_with_score + 0.3 * (2.5*trip_focus_score) + 0.15 * out_or_in_score + 0.15 * popular_or_local_score

        destination_points[all_destinations[i].name] = total_score

confirmed_destination = []

for i in range(num_destinations):
    for key in destination_points.keys():
        if destination_points[key] == max(destination_points.values()):
            destination_points[key] = 0
            confirmed_destination.append(key)
            break



    




                    
                
                
                

                        

            




