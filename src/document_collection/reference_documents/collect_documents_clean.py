import sys
import os
src_dir = os.path.join('/Users/natalipeeva/Documents/GitHub/Automatic-Answering-of-City-Council-Questions/', 'src')
sys.path.append(src_dir)
from dataset.dataset import ReferenceURL
import time
import pickle 
import pandas as pd 

########################## collection ###################


def collect_all(data, timeout, waiting_time):
    for sample in data:
        sample.collect_urls(timeout, waiting_time)



def save_data_question_answer(data):
    data_tuples = []
    #self.urls = urls
    #self.collected_urls = None
    for sample in data:
        urls = []
        for url in sample.collected_urls:
            urls.append(url.url) 
        
        data_tuples.append((sample.year, sample.month, sample.question, sample.answer, sample.document, urls))

    with open ('data_updated_urls.pickle', 'wb') as f:
        pickle.dump(data_tuples, f)


def save_collected_urls(data):
    url_tuples = []

    for sample in data:
        for url in sample.collected_urls:
            url_tuples.append((url.url, url.content, url.text, url.exception))
    
    df = pd.DataFrame(url_tuples, columns=['URL', 'Content', 'Textual_Content', 'Exception'])

    df.to_csv('urls_collected_16May.csv')


###################### older function: #################
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