from BingWebSearch import make_bing_query, make_bing_autosuggest_query, get_queries_from_autosuggest
import json
from pprint import pprint

# bing_results_json = make_bing_query('us president', 'en-US', 'San Francisco, CA')

# for search_type in bing_results_json:
#     if search_type == 'webPages':
#         for result in bing_results_json[search_type]['value']:
#             print(result['url'])
results_json = make_bing_autosuggest_query('pizza')
pprint(results_json)
queries = get_queries_from_autosuggest(results_json)
print(queries)

# pprint(bing_results_json)
