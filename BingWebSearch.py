"""
Module for bing search
"""
import json
import os
from bs4 import BeautifulSoup
from pprint import pprint
import requests
from geopy.geocoders import Nominatim
from util import get_cumulative_bias

BING_AUTOSUGGEST_ENDPOINT = 'https://api.bing.microsoft.com/v7.0/suggestions'
BING_WEB_SEARCH_ENDPOINT  = 'https://api.bing.microsoft.com/v7.0/search'

def get_location(location="Columbus, OH"):
    geolocator = Nominatim(user_agent="CS356-proj")
    geolocation = geolocator.geocode(location)
    return geolocation


def make_bing_autosuggest_query(query, location="Columbus, OH"):
    '''
    returns a JSON object representing autosuggestions given a query keyword.
    '''
    subscription_key = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
    geolocation = get_location(location)
    search_location =  f"lat:{geolocation.latitude};long:{geolocation.longitude};re:5000"
    endpoint = BING_AUTOSUGGEST_ENDPOINT
    print(f"Getting autosuggestions for {query} from location: {location}")

    params = {
        'q' : query,
    }

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'X-Search-Location': search_location,
    }

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


def make_bing_query(query, location="Columbus, OH", max_results=10):
    # Add API key and endpoint from environment variables
    subscription_key = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
    endpoint = BING_WEB_SEARCH_ENDPOINT

    # Construct request
    # view = '47.6421,-122.13715,5000' # need to test if this is being used for more than Maps
    # test search location header: Columbus, OH
    # search_location = 'lat:39.9612;long:82.9988;re:5000;disp:Columbus%2C%20Ohio'
    geolocation = get_location(location)
    search_location = f"lat:{geolocation.latitude};long:{geolocation.longitude};re:5000"
    print(f"Searching from location {location}")

    params = {
        'q': query,
        'num': max_results,
        # 'localCircularView': view
    }
    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'X-Search-Location': search_location,
        # 'X-MSEdge-Client-IP': '18.118.156.85'
    }

    # call API
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()

        print("\nResponse Headers:\n")
        print(response.headers)

        print("\nJSON Response:\n")
        pprint(response.json())
        return response.json()
    except Exception as ex:
        raise ex


def get_queries_from_autosuggest(bing_autosuggest_results_json):
    '''
    Returns an array of search queries from an autosuggest JSON result
    '''
    queries = []
    results = bing_autosuggest_results_json['suggestionGroups'][0]['searchSuggestions']
    for suggestion in results:
        queries.append(suggestion['query'])
    # print(queries)
    return queries

def get_urls_from_query(bing_results_json):
    urls = []
    for search_type in bing_results_json:
        if search_type == 'webPages':
            for result in bing_results_json[search_type]['value']:
                urls.append(result['url'])


def parse_results(raw_json):
    urls = []
    webpages = raw_json['webPages']
    for webpage in webpages['value']:
        urls.append(webpage['url'])
    return urls


def bing_search(query, location="Columbus, OH", max_results=10):
    raw_json = make_bing_query(
        query=query,
        location=location,
        max_results=max_results
    )
    return parse_results(raw_json)


def get_bing_results(keyword, location='New York, NY', max_results=10):
    return bing_search(query=keyword, location=location, max_results=max_results)


def bing_keywords_search(keywords, location, max_results=10):
    keyword_to_websites = {}
    for keyword in keywords:
        keyword_to_websites[keyword] = get_bing_results(
            keyword=keyword,
            location=location,
            max_results=max_results
        )
    return keyword_to_websites


def get_overall_bing_bias(keywords, locations, bias_scores, weighted=False, max_results=10):
    location_to_bias = {}
    for location in locations:
        keyword_to_websites = bing_keywords_search(
            keywords=keywords,
            location=location,
            max_results=max_results
        )
        bias = 0.0
        for keyword, websites in keyword_to_websites.items():
            bias += get_cumulative_bias(
                websites=websites,
                bias_scores=bias_scores,
                weighted=weighted
            )
        location_to_bias[location] = bias / len(keyword_to_websites)
        print("Bias for %s: %f" % (location, location_to_bias[location]))
    return location_to_bias


def get_overall_bing_bias_autosuggest(keywords, locations, bias_scores, weighted=False, max_results=10):
    location_to_bias = {}
    for location in locations:
        for keyword in keywords:
            json_autosuggested = make_bing_autosuggest_query(keyword, location)
            queries = get_queries_from_autosuggest(json_autosuggested)
            print(queries)
            keyword_to_websites = bing_keywords_search(
                keywords=queries,
                location=location,
                max_results=max_results
            )
            bias = 0.0
            for keyword, websites in keyword_to_websites.items():
                bias += get_cumulative_bias(
                    websites=websites,
                    bias_scores=bias_scores,
                    weighted=weighted
                )
            location_to_bias[location] = bias / len(keyword_to_websites)
        print(f"Bias for {location}: {location_to_bias[location]}")

    return location_to_bias




def main():
    results_json = make_bing_autosuggest_query('pizza')
    print(results_json)
    queries = get_queries_from_autosuggest(results_json)
    print(queries)

if __name__ == '__main__':
    main()
