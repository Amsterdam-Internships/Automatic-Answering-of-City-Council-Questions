import requests
import time
import random
from bs4 import BeautifulSoup
from urllib.parse import urljoin

import os
import sys
src_dir = os.path.join('/Users/natalipeeva/Documents/GitHub/Draft/', 'src')
sys.path.append(src_dir)
from dataset.dataset import ReferenceURL


def collect_subpages(base_url, paths):
    collected_urls = []

    base_url = ReferenceURL(base_url)
    base_url.fetch_url(random.uniform(1, 3))
    collected_urls.append(base_url)

    links = base_url.content.find_all("a", href=lambda href: href)

    for link in links:
        if any(path in link["href"] for path in paths):
            linked_url = ReferenceURL(urljoin(base_url.url, link["href"]))
            linked_url.fetch_url(random.uniform(1, 3))
            collected_urls.append(linked_url)
            # Recursively follow links that contain paths
            if any(path in linked_url.url for path in paths):
                subpages = collect_subpages(linked_url.url, paths)
                collected_urls.extend(subpages)

    return collected_urls

paths = ['afval-en-hergebruik', 'afval-hergebruik', 'belastingen-heffingen', 'bestuur-en-organisatie',
         'bestuur-organisatie', 'projecten', 'burgerzaken', 'diversiteit', 'kunst-cultuur', 
         'ondernemen', 'onderwijs-jeugd', 'parkeren', 'sport', 'stadsdelen', 'subsidies', 
         'verkeer-vervoer', 'toerisme-vrije-tijd', 'werk-inkomen', 'wonen-leefomgeving', 
         'zorg-ondersteuning']


def collect_subpages(base_url):
    """
    Input: base url like https://amsterdam.nl/parkeren
    Output: a scraped collection of all nested urls under the base one
    """
    visited_urls = set()
    collection = []
    urls_to_visit = [base_url]
    
    try:
        while urls_to_visit:
            url = ReferenceURL(url = urls_to_visit.pop(0))
            
            # Skip if already visited
            if url.url in visited_urls:
                continue

            # Add to visited URLs
            visited_urls.add(url.url)
            url.fetch_url(timeout=5)

            # Add check collection???

            time.sleep(random.uniform(1, 3))
            try:
                url.fetch_url()
                collection.append(url)
                # Extract all anchor tags
                if url.content is None:
                    pass
                else:
                    for anchor_tag in url.content.find_all('a'):
                        href = anchor_tag.get('href')
                        if href:
                            # Construct absolute URL
                            absolute_url = urljoin(url.url, href)
                            absolute_url = ReferenceURL(absolute_url)
                        
                            # Check if the URL contains the base URL and exclude specified patterns
                            if base_url in absolute_url.url and \
                                    not any(pattern in absolute_url.url for pattern in ['#Content', '#mainmenu', '#megamenu', '?mode=hide', '#PagCls', 'tel:', '?print=true']):
                                
                                # Add the URL to the list of URLs to visit
                                urls_to_visit.append(absolute_url.url)

            except KeyboardInterrupt:
                # Handle interruption
                print("Execution interrupted!")
                break
            except:
                pass
    
    except:
        pass
    
    return collection




def collect_multiple_subpages(base_url, subpages_list):
    collected_full = []
    for subpage in subpages_list:
        collected = collect_subpages(base_url+subpage+'/')
        collected_full.append(collected)
    
    collected_combined = [item for sublist in collected_full for item in sublist]

    return collected_combined


base_url = 'https://www.amsterdam.nl/'

def collect_amsterdam(base_url = base_url, paths = paths):
    collect_subpages(base_url, paths)







collected_urls = []

