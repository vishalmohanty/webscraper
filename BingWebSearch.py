import json
import os
from pprint import pprint
import requests

'''
Module for bing search
'''

def make_bing_query(query):
    # Add API key and endpoint from environment variables
    subscription_key = os.environ['BING_SEARCH_V7_SUBSCRIPTION_KEY']
    endpoint = os.environ['BING_SEARCH_V7_ENDPOINT'] + "/v7.0/search"

    # Construct request
    mkt = 'en-US'
    params = {'q': query, 'mkt': mkt}
    headers = {'Ocp-Apim-Subscription-Key': subscription_key }

    # call API
    try:
        response = requests.get(endpoint, headers=headers, params=params)
        response.raise_for_status()

        print("\nResponse Headers:\n")
        print(response.headers)

        print("\nJSON Response:\n")
        pprint(response.json())
    except Exception as ex:
        raise ex
