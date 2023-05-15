import sys
import os
src_dir = os.path.join('/Users/natalipeeva/Documents/GitHub/Draft/', 'src')
sys.path.append(src_dir)
from dataset.dataset import ReferenceURL


def apply_url_fetching(urls):
    fetched_urls = []
    for url in urls:
        url = ReferenceURL(url)
        try:
            fetched_urls.append(url.fetch_url()) # set timeout
        except Exception as e:
            fetched_urls.append(url, e) ################ check it
            ### store to check exceptions