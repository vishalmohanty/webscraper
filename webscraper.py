import keyword
from urllib.parse import urlencode, urlunparse
from urllib.request import urlopen, Request
from vm_ddgsearch import ddg
from vm_googlesearch import search
from BingWebSearch import make_bing_query

def get_ddg_results(keyword, max_results=10):
    results = ddg(keyword, region='wt-wt', safesearch='Moderate', time='y', max_results=max_results)
    for result in results:
        print(result['href'])

def get_google_results(keyword, location, max_results=10):
    g_results = search(keyword, num_results=max_results, location=location)
    for result in g_results:
        print(result)

def get_bing_results(keyword):
    make_bing_query(keyword)


keyword = 'pizza'
get_ddg_results(keyword=keyword)
get_google_results(keyword=keyword, location="Boston,Massachusetts,United States")
get_bing_results(keyword=keyword)
