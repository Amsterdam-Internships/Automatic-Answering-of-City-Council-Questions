import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time
import random
import os
import sys
# absolute path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# add the relative path to the source directory
src_dir = os.path.join(current_dir, 'src')
sys.path.append(src_dir)

from dataset.dataset import ReferenceURL
import pandas as pd
import pickle


def collect_subpages(base_url, visited_urls = None, collection = None, urls_to_visit = None):
    collection = [] # store collected
    if visited_urls is None and urls_to_visit is None:
        visited_urls = []  # store visited to avoid visiting again
        start_url = base_url
        urls_to_visit = [start_url] # urls left to visit

    try:
        while urls_to_visit:

            # take a url to visit and remove from urls_to_visit
            url = urls_to_visit.pop(0)

            # skip if already visited
            if url in visited_urls:
                continue
            
            visited_urls.append(url)

            if check_correct_base(str(url), base_url): # check base_url
                reference_url = ReferenceURL(url)
                reference_url.fetch_url()

                visited_urls.append(str(reference_url.url)) if str(reference_url.url) not in visited_urls else None

                # check base_url as a redirect might cause the url to change
                if check_correct_base(str(url), base_url):
                    collection.append(reference_url)

                    if reference_url.content is not None:
                        links = reference_url.content.find_all("a", href=lambda href: href)

                        for link in links:
                            linked_url = urljoin(str(base_url), link["href"])

                            # Make sure it STARTS with base_url
                            if check_correct_base(str(url), base_url) and not any(pattern in linked_url for pattern in ['#Content', '#mainmenu', '#megamenu', '?mode=hide', '#PagCls', 'tel:', '?print=true']):
                                urls_to_visit.append(linked_url)

                        time.sleep(random.uniform(1, 3))


    except (KeyboardInterrupt, Exception) as e:
        print("An exception occurred:", str(e),
         "The collected urls and the urls left to visit are stores in a tuple (collection, urls_to_visit).")
        return (collection, urls_to_visit)
    

    return collection


def is_special_case(url):
    special_cases = ['afval-en-hergebruik', 'afval-hergebruik',
                    'bestuur-en-organisatie', 'bestuur-organisatie', 
                     'burgerzaken', 'diversiteit']
    # check if the url is part of a special case
    return any(url.startswith('https://www.amsterdam.nl/' + case) for case in special_cases)

def check_correct_base(url, base_url):
    if not is_special_case(url):
        return url.startswith(base_url)
    
    if url.startswith('https://www.amsterdam.nl/afval') and base_url == 'https://www.amsterdam.nl/afval-en-hergebruik/':
        return url.startswith('https://www.amsterdam.nl/afval-en-hergebruik/') or url.startswith('https://www.amsterdam.nl/afval-hergebruik/')
    
    if url.startswith('https://www.amsterdam.nl/bestuur') and base_url == 'https://www.amsterdam.nl/bestuur-en-organisatie/':
        return url.startswith('https://www.amsterdam.nl/bestuur-en-organisatie/') or url.startswith('https://www.amsterdam.nl/bestuur-organisatie/')
    
    if url.startswith('https://www.amsterdam.nl/burgerzaken') and base_url =='https://www.amsterdam.nl/burgerzaken/':
        return url.startswith('https://www.amsterdam.nl/burgerzaken/') and 'trouwlocaties-gemeente-amsterdam' not in url
    
    if url.startswith('https://www.amsterdam.nl/diversiteit') and base_url == 'https://www.amsterdam.nl/diversiteit/':
        return url.startswith('https://www.amsterdam.nl/diversiteit/') and 'nationaal-slavernijmuseum/kalender/' not in url
    
    if url.startswith('https://www.amsterdam.nl/stadsdelen') and base_url == 'https://www.amsterdam.nl/stadsdelen/':
        return url.startswith('https://www.amsterdam.nl/stadsdelen/') and '?embed=fotoslide' not in url
    
    return False

    
def get_collected(csv_path, pickle_path):
    collected = pd.read_csv(csv_path)
    visited = list(collected['URL'])
    with open (pickle_path, 'rb') as f:
        to_visit = pickle.load(f)
    
    return (visited, to_visit)


def collect_and_save_urls(url, path):
    filepath = os.path.join(path, (url.split('/')[-2] + '.csv'))
    subpages = collect_subpages(url)
    try:
        save_collected_urls(subpages, filepath)
    except:
        save_collected_urls(subpages[0], filepath)
        left_to_collect = subpages[1]
        left_to_collect_filepath = os.path.join(path, ('left_to_collect_' + filepath.split('/')[-1].split('.')[0] + '.pickle'))
        with open(left_to_collect_filepath, 'wb') as f:
            pickle.dump(left_to_collect, f)


def collect_multiple_subpages(base_url, subpages_list):
    collected_full = []

    for subpage in subpages_list:
        try:
            collected = collect_subpages(base_url+subpage+'/')
            collected_full.append(collected)
        
        except KeyboardInterrupt:
            print("Execution interrupted!")
            break
    collected_combined = [item for sublist in collected_full for item in sublist]

    return collected_combined





def save_collected_urls(data, csv_name):
    """
    Input: collected urls of type ReferenceURL()
    Output: csv containing (url, content, textual content, exception)
    """
    url_tuples = []

    for url in data:
        url_tuples.append((url.url, url.content, url.text, url.exception))
    
    df = pd.DataFrame(url_tuples, columns=['URL', 'Content', 'Textual_Content', 'Exception'])

    df.to_csv(csv_name)