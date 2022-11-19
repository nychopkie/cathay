import requests

version = 'some_version'
url = f'https://api.test.hotelbeds.com/hotel-content-api/{version}/hotels'

header ={
    'Apikey': 'some_key',
    'Xsignature': 'some sign',
    'Accept': 'application/json',
    'Accept-Encoding': 'gzip'
}

param = {
    'destinationCode': 'PMI',
    'countryCode': 'JP',
    'code': '10',
    'fields': 'all',
    'language': 'all',
}

class hotel_info:
    def __init__(self):
        self.lat = ''
        self.long = ''
        self.comment = ''
        self.photo_path = ''
        self.fee = ''


    def retrieve(self):

        response = requests.get(url=url, headers=header, params=param).json()
        self.lat = response['hotels'][0]['coordinates']['latitude']
        self.long = response['hotels'][0]['coordinates']['longitude']

        self.comment = response['hotels'][0]['description']['content']

        self.photo_path = response['hotels'][0]['images']['path']

        self.fee = response['hotels'][0]['facilities'][0]['indFee']
