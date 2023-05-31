import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse, urljoin
import time
import random
import os
import sys
src_dir = os.path.join('/Users/natalipeeva/Documents/GitHub/Draft/', 'src')
sys.path.append(src_dir)
from dataset.dataset import ReferenceURL
import pandas as pd

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