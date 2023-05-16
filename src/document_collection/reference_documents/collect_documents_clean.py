import sys
import os
src_dir = os.path.join('/Users/natalipeeva/Documents/GitHub/Automatic-Answering-of-City-Council-Questions/', 'src')
sys.path.append(src_dir)
from dataset.dataset import ReferenceURL
import time

def apply_url_fetching(urls, timeout, waiting_time=None):
    fetched_urls = []
    for url in urls:
        url = ReferenceURL(url)
        try:
            url.fetch_url(timeout)
            fetched_urls.append(url)
        except Exception as e:
            fetched_urls.append((url, e)) ################ check it
            ### store to check exceptions
        
        time.sleep(waiting_time) # waiting time before next request
    
    return fetched_urls



########################## collection ###################


def collect_all(data):
    for sample in data:
        sample.collect_urls(timeout=5, waiting_time=2)