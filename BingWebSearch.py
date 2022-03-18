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
import csv
from tqdm import tqdm

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
    # print(f"Getting autosuggestions for {query} from location: {location}")

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
    # what data type for granular CSV? array to use in DictWriter
    granular_bias_scores = []
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
                bias_score = get_cumulative_bias(
                    websites=websites,
                    bias_scores=bias_scores,
                    weighted=weighted
                )
                bias += bias_score
                # write to CSV array here: <location>, <keyword>, <bias score>, <queries array>
                granular_bias_scores.append([location, keyword, bias_score, queries])
            location_to_bias[location] = bias / len(keyword_to_websites)
        print(f"Bias for {location}: {location_to_bias[location]}")
        # write to another CSV dictionary here as well: <location>, <cumulative bias score>\
    granular_bias_to_csv(granular_bias_scores, 'granular_bing_bias_1.0.csv')
    cumulative_bias_to_csv(location_to_bias, 'cumulative_bing_bias_1.0.csv')
    return location_to_bias

def granular_bias_to_csv(granular_bias_arr, filename):
    with open(filename, 'w') as csvoutput:
        fields = ['location', 'keyword', 'bias_score', 'queries']
        writer = csv.DictWriter(csvoutput, fieldnames=fields)
        for elem in granular_bias_arr:
            writer.writerow({
                'location': elem[0],
                'keyword': elem[1],
                'bias_score': elem[2],
                'queries': elem[3]
            })

def cumulative_bias_to_csv(location_to_bias, filename):
    with open(filename, 'w') as csvoutput:
        fields = ['location', 'bias']
        writer = csv.DictWriter(csvoutput, fieldnames=fields)
        for loc, bias in location_to_bias.items():
            writer.writerow({
                'location': loc,
                'bias': bias
            })


def get_bing_auto_complete_suggestions_bias(
        search_term,
        location="Boston,Massachusetts,United States"
):
    queries = make_bing_autosuggest_query(
        query=search_term,
        location=location
    )
    suggestions = get_queries_from_autosuggest(queries)
    n_suggestions = len(suggestions)
    # Log the suggestions so that they can be used later if required
    # print(suggestions)

    unweighted_democratic_count = 0
    weighted_democratic_count = 0.0
   # democratic_relevance = 0
    unweighted_republican_count = 0
    weighted_republican_count = 0.0
    #republican_relevance = 0

    for i in range(0, n_suggestions):
        # print('nth suggestion:', suggestions[i].lower())
        if "democrat" in suggestions[i].lower():
            unweighted_democratic_count = unweighted_democratic_count + 1
            weighted_democratic_count = weighted_democratic_count + 1.0/(i+1)
           # democratic_relevance += suggestions[i][1]
        if "republican" in suggestions[i].lower():
            unweighted_republican_count = unweighted_republican_count + 1
            weighted_republican_count = weighted_republican_count + 1.0/(i+1)
            #republican_relevance += suggestions[i][1]

    # Logging the counts and relevance
    #print("Unweighted democratic count: %d" % unweighted_democratic_count)
    #print("Unweighted republican count: %d" % unweighted_republican_count)
    #print("Weighted democratic count: %f" % weighted_democratic_count)
    #print("Weighted republican count: %f" % weighted_republican_count)
    #print("Total democratic relevance: %d" % democratic_relevance)
    #print("Total republican relevance: %d" % republican_relevance)
    #avg_democratic_relevance = (democratic_relevance*1.0/n_suggestions)
    #avg_republican_relevance = (republican_relevance*1.0/n_suggestions)
    #print("Average democratic relevance: %f" % avg_democratic_relevance)
    #print("Average republican relevance: %f" % avg_republican_relevance)
    #print("\n")
    return [unweighted_democratic_count, unweighted_republican_count,
            weighted_democratic_count, weighted_republican_count 
            #democratic_relevance,republican_relevance, avg_democratic_relevance, avg_republican_relevance
            ]

def get_full_word_bing_auto_complete_suggestions_bias(
        keyword,
        location="Boston,Massachusetts,United States"
):
    n = len(keyword)
    search_term_to_scores = {}
    for i in range(1, n+1):
        search_term = keyword[:i]
        search_term_to_scores[search_term] = get_bing_auto_complete_suggestions_bias(
            search_term=search_term,
            location=location
        )
    # print(search_term_to_scores)
    return search_term_to_scores

def get_auto_complete_biases(locations, keywords):
    with open('demo-output.csv', 'w') as csvoutput:
        fields = [
            'Location',
            'Search Term', 
            'Democratic Count', 
            'Republican Count', 
            'Weighted Democractic Count', 
            'Weighted Republican Count'
        ]
        writer = csv.DictWriter(csvoutput, fieldnames=fields)
        for location in tqdm(locations):
            for keyword in keywords:
                term_to_scores = get_full_word_bing_auto_complete_suggestions_bias(keyword, location)
                for key, value in term_to_scores.items():
                    writer.writerow( {
                        'Location': location,
                        'Search Term': key, 
                        'Democratic Count': value[0], 
                        'Republican Count': value[1], 
                        'Weighted Democractic Count': value[2], 
                        'Weighted Republican Count': value[3]
                    }
                    )

def main():
    #results_json = make_bing_autosuggest_query('pizza')
    #print(results_json)
    #queries = get_queries_from_autosuggest(results_json)
    #print(queries)
    
    get_full_word_bing_auto_complete_suggestions_bias('US Senators Democratic')

if __name__ == '__main__':
    main()
