import requests

# API without key that is used to generate all the destinations in a city
class Spot:
    '''this object returns the dictionary with format {place:[lat,lng]} which place stands for tourist spot name and
    lat and lng stands for its actual position in map'''
    def __init__(self):     #initialized and returned things
        self.spot_dict = {}
        self.city = 'Tokyo'
        self.get_spot()

    def get_spot(self):
        version = '1.2'
        language = 'uk'
        url_base = f'https://api.sygictravelapi.com/{version}/{language}'

        header = {
            'x-api-key': 'KEY_FOR_API' # future application needed to get key
        }

        template_para = {
            'parent_place_id': 'country:75'     # japan.id = 75
        }
        #access japan template
        url_template = f'{url_base}/trips/templates'
        response = requests.get(url=url_template, params=template_para, headers=header).json()

        trips = response['data']['trips']
        trips_id = []
        # trips id for futher finding places on different trips
        for this_trip in trips:
            this_trip_id = this_trip['id']
            trips_id.append(this_trip_id)

        # place id
        place_id = []
        for this_id in trips_id:
            url_trip = f'{url_base}/trips/{this_id}'
            trip_para = {
                'id': this_id
            }
            trips_response = requests.get(url=url_trip, headers=header, params=trip_para).json()
            this_itinerary = trips_response['data']['trip']['days']['itinerary:']
            for one_itinerary in this_itinerary:
                place_id.append(one_itinerary['place_id'])

        # get place parameter
        for thiss_id in place_id:
            url_place = f'{url_base}/places/{thiss_id}'
            place_param = thiss_id
            place_response = requests.get(url=url_place, headers=header, params=place_param).json()
            spot_list = place_response['data']['place']
            for spot in spot_list:
                if spot['address_details']['city'] == self.city:
                    self.spot_dict[spot['name']] = [spot['location']['lat'], spot['location']['lng']]
                else:
                    continue




