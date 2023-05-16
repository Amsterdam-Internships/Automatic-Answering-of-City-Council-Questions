import requests
from bs4 import BeautifulSoup
import time 
import random
import PyPDF2
import io
import pandas as pd

class QuestionAnswer:
    def __init__(self, year, month, question, answer, document, urls):
        self.year = year
        self.month = month
        self.question = question
        self.answer = answer
        self.document = document 
        self.urls = urls
        self.collected_urls = None
    
    def get_urls_list(self):
        try:
            self.urls.split('\n')
            self.urls = self.urls.split('\n')
        except:
            self.urls = None

    def filter_by_domains(self, domains = ['www.amsterdam.nl, www.rijksoverheid.nl, www.rivm.nl, www.ggd.amsterdam.nl']):
        self.urls = [url for url in self.urls if url in domains]
    
    def filer_factual(self, words_to_filter):
        self.question = [question if question in  words_to_filter else '' for question in self.questions]
        pass
    
    def collect_urls(self, timeout, waiting_time=None):
        self.collected_urls = []

        for url in self.urls:
            url_obj = ReferenceURL(url)
            url_obj.fetch_url(timeout)
            self.collected_urls.append(url_obj)

            if waiting_time != None: 
                time.sleep(waiting_time)
            
    

class ReferenceURL:
    def __init__(self, url, text_content=None, content=None):
        self.url = url
        self.text = text_content
        self.content = content  # mayybe rename?
        self.response = None
        self.exception = None
        
    def get_response(self, timeout=None):
        try:
            self.response = requests.get(self.url, allow_redirects=True, timeout=timeout)
            self.response.raise_for_status()  # raise an exception if the response code is not 200
        except requests.exceptions.RequestException as e:
            raise ConnectionError(f"Error fetching URL: {e}") from None

    def update_url(self):
        try:
            self.url = self.response.url
        except AttributeError:
            raise ValueError("Response object not found. Please call 'get_response' first.") from None

    def get_response_code(self):
        try:
            self.response_code = self.response.status_code
        except AttributeError:
            raise ValueError("Response object not found. Please call 'get_response' first.") from None

    def get_html(self):
        if self.content is None:
            try:
                if self.response is None:
                    self.get_response()
                self.content = BeautifulSoup(self.response.content, 'html.parser')
                #return self.content
            except requests.exceptions.RequestException as e:
                raise ConnectionError(f"Error fetching URL: {e}") from None
            except Exception as e:
                raise ValueError(f"Error parsing HTML: {e}") from None

    def get_text(self):
        if self.text is None:
            try:
                if self.content is None:
                    self.get_html()
                self.text = self.content.get_text()
                #return self.text
            except Exception as e:
                raise ValueError(f"Error extracting text content: {e}") from None

    def get_pdf_content(self):
        if self.content is None:
            self.content = self.response.content
            #return self.content
    
    def get_pdf_text(self):
        if self.text is None:
            try:
                if self.content is None:
                    self.get_pdf_content()
                pdf_text = io.BytesIO(self.content)
                pdf_reader = PyPDF2.PdfReader(pdf_text)

                self.text = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    self.text += page.extract_text()
                
                #return self.text
            except Exception as e:
                raise ValueError(f"Error extracting text content: {e}") from None
    
    def fetch_url(self, timeout=None):
        try: 
            self.get_response(timeout)
            self.update_url()
            self.get_response_code()
            
            if self.url.endswith(".pdf"): # check if pdf
                self.get_pdf_content()
                self.get_pdf_text()

            else:
                self.get_html()
                self.get_text()
        except Exception as e:
            self.exception = e
        
        #return (self.url, self.content, self.text)



def create_dataset(data_path, filter_by_urls=False,
                    filter_by_domains=False, collect_urls=False):
    """
    Input: path to questions.csv
    Output: a list containing QuestionAnswer objects
    """
    questions = pd.read_csv(open(data_path, 'r'))

    questions_answers = []
    for i in range(len(questions) - 1):
        questions_obj = QuestionAnswer(month = questions['Month'][i],
                                    year=questions['Year'][i], 
                                    question=questions['Question'][i],
                                    answer=questions['Answer'][i],
                                    document=questions['Document'][i],
                                    urls=questions['URLs'][i])
        questions_obj.get_urls_list()

        if filter_by_domains:
            questions_obj.filter_by_domains()
        if filter_by_urls:
            if questions_obj.urls != None:
                questions_answers.append(questions_obj)
        else:
            questions_answers.append(questions_obj)
        
    return questions_answers



class Dataset:
    def __init__(self, data):
        self.data = data

    def with_urls(self):
        self.data_urls = []

        for sample in self.data:
            if sample.urls != None:
                self.data_urls.append(sample)
            
    def filter_by_domains(self):

    



######################################################################################


######## Old outline of classes follows ##############




######################################################################################
class SupportingDocuments:
    def __init__(self, url, html):
        self.url = url 
        self.html = html 

    def get_text(self):
        pass
    def clean_text(self):
        pass
    def clean_url(self):
        pass


class ReferenceDocuments:
    def __init__(self, question, answer, year, month, url):
        self.url = url 
        self.question = question
        self.answer = answer
        self.year = year
        self.month = month
        #self.html = html 

    def get_text(self):
        pass
    def clean_text(self):
        pass
    def clean_url(self):
        pass


class Question:
    def __init__(self, question, year, month, source_document):
        self.question = question 
        self.year = year
        self.month = month
        self.source_document = source_document

    def clean_question(self):
        pass

class Answer:
    def __init__(self, answer):
        self.answer = answer 
        self.year = year
        self.month = month
        self.source_document = source_document

    def clean_answer(self):
        pass


