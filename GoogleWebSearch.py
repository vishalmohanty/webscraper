import json
import os
from pprint import pprint
import requests
from geopy.geocoders import Nominatim

'''
Module for Google Custom Search API
'''

CUSTOM_SEARCH_INSTANCE='b05dc56a57121eb10'
TEST_UULE='w+CAIQICImV2VzdCBOZXcgWW9yayxOZXcgSmVyc2V5LFVuaXRlZCBTdGF0ZXM%3D'

def get_location(location = "Columbus, OH"):
    geolocator = Nominatim(user_agent = "CS356-proj")
    geolocation = geolocator.geocode(location)
    return geolocation

def make_google_query(query,location):
    api_key = os.environ['GOOGLE_CUSTOM_SEARCH_API_KEY']
    cx = CUSTOM_SEARCH_INSTANCE

    endpoint = 'https://customsearch.googleapis.com/customsearch/v1'

    geolocation = get_location(location)
    search_location = f"lat:{geolocation.latitude};long:{geolocation.longitude};re:5000"
    # Construct request
    params = {
        'key': api_key,
        'cx': cx,
        'q': query,
        # 'uule': TEST_UULE
    }
    headers = {
        'Accept': 'application/json',
        'X-Search-Location': search_location
    }
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as ex:
        raise ex

def main():
    pprint(make_google_query('pizza', 'San Francisco, CA'))
    pprint(make_google_query('pizza', 'London, UK'))


if __name__ == '__main__':
    main()
