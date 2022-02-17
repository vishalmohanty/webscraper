from BingWebSearch import make_bing_query
import json
from pprint import pprint

bing_results_json = make_bing_query('us president', 'en-US', 'San Francisco, CA')

for search_type in bing_results_json:
    if search_type == 'webPages':
        for result in bing_results_json[search_type]['value']:
            print(result['url'])

# pprint(bing_results_json)
