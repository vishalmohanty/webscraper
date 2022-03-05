import json
import os
from pprint import pprint
import requests
from geopy.geocoders import Nominatim
from WebSearcher import locations
import re

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


def remove_tags_from_phrase(str):
    return re.sub(r'<.*?>', '', str)


def get_google_auto_complete_suggestions(
        search_term,
        location="Boston,Massachusetts,United States",
        language_code="en"
):
    char_count = len(search_term)
    escaped_search_term = search_term.replace(' ', '%20')
    loc_id = locations.get_location_id(location)
    usr_agent = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 ('
                      'KHTML, like Gecko) '
                      'Chrome/61.0.3163.100 Safari/537.36'}
    google_url = 'https://www.google.com/complete/search?q=%s&cp=%s&uule=%s&hl=%s' \
                 '&client=gws-wiz' \
                 % (escaped_search_term, char_count, loc_id, language_code)

    print("URL: %s" % google_url)

    response = requests.get(google_url, headers=usr_agent)
    response.raise_for_status()

    # Strip the window.google.ac.h( ... ) outer covering to get a json parsable object
    json_obj = re.sub(r'\)$', '', re.sub(r'^.*?\(', '', response.text))

    # The first element contains the suggestions
    suggestions = json.loads(json_obj)[0]

    # Create a list of suggestion to relevance mapping
    suggestion_and_relevance = \
        [tuple((remove_tags_from_phrase(x[0]), x[2][0])) for x in suggestions]

    return suggestion_and_relevance


def get_google_auto_complete_suggestions_bias(
        search_term,
        location="Boston,Massachusetts,United States",
        language_code="en"
):
    suggestions = get_google_auto_complete_suggestions(
        search_term=search_term,
        location=location,
        language_code=language_code
    )
    n_suggestions = len(suggestions)
    # Log the suggestions so that they can be used later if required
    print(suggestions)

    unweighted_democratic_count = 0
    weighted_democratic_count = 0.0
    democratic_relevance = 0
    unweighted_republican_count = 0
    weighted_republican_count = 0.0
    republican_relevance = 0

    for i in range(0, n_suggestions):
        if "democratic" in suggestions[i][0]:
            unweighted_democratic_count = unweighted_democratic_count + 1
            weighted_democratic_count = weighted_democratic_count + 1.0/(i+1)
            democratic_relevance += suggestions[i][1]
        if "republican" in suggestions[i][0]:
            unweighted_republican_count = unweighted_republican_count + 1
            weighted_republican_count = weighted_republican_count + 1.0/(i+1)
            republican_relevance += suggestions[i][1]

    # Logging the counts and relevance
    print("Unweighted democratic count: %d" % unweighted_democratic_count)
    print("Unweighted republican count: %d" % unweighted_republican_count)
    print("Weighted democratic count: %f" % weighted_democratic_count)
    print("Weighted republican count: %f" % weighted_republican_count)
    print("Total democratic relevance: %d" % democratic_relevance)
    print("Total republican relevance: %d" % republican_relevance)
    avg_democratic_relevance = (democratic_relevance*1.0/n_suggestions)
    avg_republican_relevance = (republican_relevance*1.0/n_suggestions)
    print("Average democratic relevance: %f" % avg_democratic_relevance)
    print("Average republican relevance: %f" % avg_republican_relevance)
    print("\n")
    return [unweighted_democratic_count, unweighted_republican_count,
            weighted_democratic_count, weighted_republican_count, democratic_relevance,
            republican_relevance, avg_democratic_relevance, avg_republican_relevance]


def get_full_word_google_auto_complete_suggestions_bias(
        keyword,
        location="Boston,Massachusetts,United States",
        language_code="en"
):
    n = len(keyword)
    search_term_to_scores = {}
    for i in range(1, n+1):
        search_term = keyword[:i]
        search_term_to_scores[search_term] = get_google_auto_complete_suggestions_bias(
            search_term=search_term,
            location=location,
            language_code=language_code
        )
    print(search_term_to_scores)
