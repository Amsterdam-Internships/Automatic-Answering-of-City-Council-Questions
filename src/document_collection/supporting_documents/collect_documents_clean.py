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

###################################################################################################
##################################### amsterdam.nl ################################################ 
###################################################################################################

def collect_subpages(base_url, paths):
    collected_urls = []

    base_url = ReferenceURL(base_url)
    base_url.fetch_url(random.uniform(1, 3))
    collected_urls.append(base_url)

    links = base_url.html_content.find_all("a", href=lambda href: href)

    for link in links:
        if any(path in link["href"] for path in paths):
            linked_url = ReferenceURL(urljoin(base_url.url, link["href"]))
            linked_url.fetch_url(random.uniform(2, 4))
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


base_url = 'https://www.amsterdam.nl/'

def collect_amsterdam(base_url = base_url, paths = paths):
    collect_subpages(base_url, paths)

###################################################################################################

