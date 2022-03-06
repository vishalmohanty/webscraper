from BingWebSearch import *
from util import *
import json
from pprint import pprint
import csv

def load_website_scores():
    scores = {}
    with open('data/scores/bias_scores.csv', newline='') as csvfile:
        my_reader = csv.reader(csvfile, delimiter=',')
        header = next(my_reader)
        for row in my_reader:
            scores[row[0]] = float(row[1])
    return scores

# bing_results_json = make_bing_query('us president', 'en-US', 'San Francisco, CA')

# for search_type in bing_results_json:
#     if search_type == 'webPages':
#         for result in bing_results_json[search_type]['value']:
#             print(result['url'])
# results_json = make_bing_autosuggest_query('pizza')
# pprint(results_json)
# queries = get_queries_from_autosuggest(results_json)
# print(queries)
keywords = "data/keywords/test_keywords.csv"
get_overall_bing_bias_autosuggest(
	keywords = get_keywords(keywords),
	locations = get_bing_locations("data/location_data/bing_test.csv"),
	bias_scores = load_website_scores(),
	weighted=True,
	max_results=10
)

# pprint(bing_results_json)
