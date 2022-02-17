import csv
from vm_ddgsearch import ddg
from vm_googlesearch import search
from util import get_cumulative_bias, get_keywords, get_canonical_names, get_bing_locations
from BingWebSearch import bing_search, get_overall_bing_bias
import pandas as pd


def load_website_scores():
    scores = {}
    with open('data/scores/bias_scores.csv', newline='') as csvfile:
        my_reader = csv.reader(csvfile, delimiter=',')
        header = next(my_reader)
        for row in my_reader:
            scores[row[0]] = float(row[1])
    return scores


def get_ddg_results(keyword, max_results=10):
    results = ddg(keyword, region='wt-wt', safesearch='Moderate', time='y', max_results=max_results)
    for result in results:
        print(result['href'])


def get_google_results(keyword, location, max_results=10):
    g_results = search(keyword, num_results=max_results, location=location)
    for result in g_results:
        print(result)
    return g_results


def google_keywords_search(keywords, location, max_results=10):
    keyword_to_websites = {}
    for keyword in keywords:
        keyword_to_websites[keyword] = get_google_results(
            keyword=keyword,
            location=location,
            max_results=max_results
        )
    return keyword_to_websites


def get_overall_google_bias(keywords, locations, bias_scores, weighted=False, max_results=10):
    location_to_bias = {}
    for location in locations:
        keyword_to_websites = google_keywords_search(
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


def main():
    scores = load_website_scores()
    keywords = get_keywords("data/keywords/keywords.csv")
    keyword = 'us president'

    # google_results = get_google_results(keyword=keyword, location="Boston,Massachusetts,United States", max_results=20)
    # print("Cumulative bias: %s" % get_cumulative_bias(google_results, scores, weighted=True))

    # get_ddg_results(keyword=keyword)
    # get_bing_results(keyword=keyword)


    # google_locations = get_canonical_names("data/location_data/state_capitals.csv")
    bing_locations = get_bing_locations("data/location_data/bing_capitals.csv")
    # location_to_bias = get_overall_google_bias(
    #     keywords=keywords,
    #     locations=locations,
    #     bias_scores=scores,
    #     weighted=True,
    #     max_results=10)
    # print(location_to_bias)

    bing_location_to_bias = get_overall_bing_bias(
        keywords=keywords,
        locations=bing_locations,
        bias_scores=scores,
        weighted=True,
        max_results=10
    )
    print(bing_location_to_bias)


if __name__ == "__main__":
    main()
