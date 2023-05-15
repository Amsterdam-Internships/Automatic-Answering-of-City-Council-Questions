import sys
import os
src_dir = os.path.join('/Users/natalipeeva/Documents/GitHub/Automatic-Answering-of-City-Council-Questions/', 'src')
sys.path.append(src_dir)
from dataset.dataset import ReferenceURL


def apply_url_fetching(urls, timeout):
    fetched_urls = []
    for url in urls:
        url = ReferenceURL(url)
        try:
            url.fetch_url(timeout)
            fetched_urls.append(url) # set timeout
        except Exception as e:
            fetched_urls.append((url, e)) ################ check it
            ### store to check exceptions
    
    return fetched_urls