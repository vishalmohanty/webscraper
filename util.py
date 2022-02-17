"""Utility file to house common functions."""
from urllib.parse import urlparse
import pandas as pd


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
                    sum += bias_scores[domain] * (1.0 / rank)
                else:
                    sum += bias_scores[domain]
    if n > 0:
        return sum / n
    return -1


def get_canonical_names(csv_file):
    df = pd.read_csv(csv_file)
    canonical_names = df['Canonical Name']
    return canonical_names


def get_keywords(csv_file):
    df = pd.read_csv(csv_file)
    keywords = df['keywords']
    return keywords


def get_bing_locations(csv_file):
    df = pd.read_csv(csv_file)
    canonical_names = df['Capital and State']
    return canonical_names