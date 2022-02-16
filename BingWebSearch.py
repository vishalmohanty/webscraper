import json
import os
from pprint import pprint
import requests
from geopy.geocoders import Nominatim

'''
Module for bing search
'''

def get_location(location = "Columbus, OH"):
    geolocator = Nominatim(user_agent = "CS356-proj")
    geolocation = geolocator.geocode(location)
    return geolocation



def make_bing_query(query, mkt = 'en-US', location = "Columbus, OH"):
    # Add API key and endpoint from environment variables
    subscription_key = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
    endpoint = os.environ['BING_SEARCH_V7_ENDPOINT'] + "/v7.0/search"

    # Construct request
    #view = '47.6421,-122.13715,5000' # need to test if this is being used for more than Maps
    # test search location header: Columbus, OH
    # search_location = 'lat:39.9612;long:82.9988;re:5000;disp:Columbus%2C%20Ohio'
    geolocation = get_location(location)
    search_location = f"lat:{geolocation.latitude};long:{geolocation.longitude};re:5000"

    params = {
        'q': query,
        #'localCircularView': view
    }
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'X-Search-Location': search_location,
        #'X-MSEdge-Client-IP': '18.118.156.85'
    }

    # call API
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()

        # print("\nResponse Headers:\n")
        # print(response.headers)

        # print("\nJSON Response:\n")
        # pprint(response.json())
        return response.json()
    except Exception as ex:
        raise ex


def get_urls_from_query(bing_results_json):
    urls = []
    for search_type in bing_results_json:
        if search_type == 'webPages':
            for result in bing_results_json[search_type]['value']:
                urls.append(result['url'])

