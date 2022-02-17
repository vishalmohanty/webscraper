import json
import os
from pprint import pprint
import requests

'''
Module for Google Custom Search API
'''

CUSTOM_SEARCH_INSTANCE='b05dc56a57121eb10'

def make_google_query(query):
    api_key = os.environ['GOOGLE_CUSTOM_SEARCH_API_KEY']
    cx = CUSTOM_SEARCH_INSTANCE

    endpoint = 'https://customsearch.googleapis.com/customsearch/v1'

    # Construct request
    params = {
        'key': api_key,
        'cx': cx,
        'q': query
    }
    headers = {
        'Accept': 'application/json'
    }
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()
        return response.json()
    except Exception as ex:
        raise ex

def main():
    pprint(make_google_query('pizza'))

if __name__ == '__main__':
    main()
