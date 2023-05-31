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
    question_url = []
    #self.urls = urls
    #self.collected_urls = None
    for sample in data:
        urls = []
        for url in sample.collected_urls:
            urls.append(url.url) 
            question_url.append((sample.question, url.url, url.exception))

        data_tuples.append((sample.year, sample.month, sample.question, sample.answer, sample.document, urls))

    df = pd.DataFrame(data_tuples, columns=['Year', 'Month', 'Question', 'Answer', 'Document', 'URLs'])
    df2 = pd.DataFrame(question_url, columns=['Question', 'URL', 'Exception'])
                                             
    df.to_csv('questions_updated_urls.csv')
    df2.to_csv('question_url.csv')


def save_collected_urls(data):
    url_tuples = []

    for sample in data:
        for url in sample.collected_urls:
            url_tuples.append((url.url, url.content, url.text, url.exception))
    
    df = pd.DataFrame(url_tuples, columns=['URL', 'Content', 'Textual_Content', 'Exception'])

    df.to_csv('reference_urls_collected.csv')
