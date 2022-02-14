import csv
from urllib.parse import urlparse
from vm_ddgsearch import ddg
from vm_googlesearch import search
from BingWebSearch import make_bing_query

def load_website_scores():
    scores = {}
    with open('../bias_scores.csv', newline='') as csvfile:
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

def get_matching_domain(domain, bias_scores):
    while not domain in bias_scores:
        if '.' in domain:
            domain = domain.split('.', 1)[1]
        else:
            return ''
    if len(domain) > 0:
        return domain
    return ''

def get_cumulative_bias(websites, bias_scores, weighted=False):
    sum = 0.0
    n = 0
    rank = 0.0
    for website in websites:
        rank += 1.0
        domain = urlparse(website).netloc
        if 'wikipedia' not in domain:
            domain = get_matching_domain(domain, bias_scores)
            if len(domain) > 0:
                n += 1
                if weighted:
                    sum += bias_scores[domain]*(1.0/rank)
                else:
                    sum += bias_scores[domain]
    if n > 0:
        return sum/n
    return -1


def get_bing_results(keyword, mkt='en-US', location='New York, NY'):
    make_bing_query(keyword, mkt, location)

def main():
    scores = load_website_scores()
    keyword = 'us president'

    google_results = get_google_results(keyword=keyword, location="Boston,Massachusetts,United States", max_results=20)
    print("Cumulative bias: %s" % get_cumulative_bias(google_results, scores, weighted=True))

    get_ddg_results(keyword=keyword)
    get_bing_results(keyword=keyword)


keyword = 'pizza'
get_ddg_results(keyword=keyword)
get_google_results(keyword=keyword, location="Boston,Massachusetts,United States")
get_bing_results(keyword=keyword, mkt='en-US', location='Boston, MA')

if __name__=="__main__":
    main()

