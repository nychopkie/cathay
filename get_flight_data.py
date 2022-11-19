import requests
import datetime

# current_port = 'HKG'
# dest_port = 'NRT'
utc_time = datetime.datetime.now(datetime.timezone.utc)

url_head = 'https://cathayhackathon'
url = f'{url_head}/operation/flightInformation/v3/next24hraircraftstatus'

header = {
    "X-applicationName": 'CUSS',
    'trace_id': 'abcdefg',
    'apikey': 'PGWzTIo4jAVwYioHCJL5F3ysiw8wLEDL'
}

para = {
    'aircraftType': '',
    'selectedAircraftType': '',
    'aircraftRegistration': '',
    'station': '',
    'currentDateTimeUTC': str(utc_time).split()[1].split('.')[0],
}
class FlightSearch:
    def __init__(self, current_port, dest_port):
        self.flight = {}
        self.dept_time = {}
        self.arri_time = {}
        self.start = current_port
        self.dest = dest_port
#        self.go_re = go_or_re # 0 go only day,  1 return only day
        self.date = utc_time.date()
        self.get_flight()

    def get_flight(self):
        response = requests.get(url=url, headers=header, params=para)
        response = response.json()
        i = 0
        for ele in response['flights']:  #extract various attributes from the json file and put it in attribute for future operatoin

                if ele['scheduleDepartureAirport'] == self.start and ele['scheduleArrivalAirport'] == self.dest:
                    self.flight[i] = f"{ele['airline']}{ele['flightNumber']}"
                    self.dept_time[i] = ele['takeoffTimeActualLocal'].split()[1]
                    self.arri_time[i] = ele['touchdownTimeActualLocal'].split()[1]
                    i += 1
