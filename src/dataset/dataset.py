import requests
from bs4 import BeautifulSoup
import time 
import random
import PyPDF2
import io
import pandas as pd

class QuestionAnswer:
    def __init__(self, year, month, question, answer, document, urls):
        self. year = year
        self.month = month
        self.question = question
        self.answer = answer
        self.document = document 
        self.urls = urls.split('\n')
    
    def filter_by_domains(self, domains = ['www.amsterdam.nl, www.rijksoverheid.nl, www.rivm.nl, www.ggd.amsterdam.nl']):
        self.urls = [url if url in domains else '' for url in self.urls]
    
    def filer_factual(self, words_to_filter):
        self.question = [question if question in  words_to_filter else '' for question in self.questions]
    

class ReferenceURL:
    def __init__(self, url, text_content=None, html_content=None):
        self.url = url
        self.text = text_content
        self.html_content = html_content
        self.response = None
        
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
        if self.html_content is None:
            try:
                if self.response is None:
                    self.get_response()
                self.html_content = BeautifulSoup(self.response.content, 'html.parser')
                #return self.html_content
            except requests.exceptions.RequestException as e:
                raise ConnectionError(f"Error fetching URL: {e}") from None
            except Exception as e:
                raise ValueError(f"Error parsing HTML: {e}") from None

    def get_text(self):
        if self.text is None:
            try:
                if self.html_content is None:
                    self.get_html()
                self.text = self.html_content.get_text()
                #return self.text
            except Exception as e:
                raise ValueError(f"Error extracting text content: {e}") from None

    def get_pdf_content(self):
        if self.pdf_content is None:
            self.pdf_content = self.response.content
            #return self.pdf_content
    
    def get_pdf_text(self):
        if self.text is None:
            try:
                if self.pdf_content is None:
                    self.get_pdf_content()
                pdf_text = io.BytesIO(self.pdf_content)
                pdf_reader = PyPDF2.PdfReader(pdf_text)

                self.text = ""
                for page_num in range(len(pdf_reader.pages)):
                    page = pdf_reader.pages[page_num]
                    self.text += page.extract_text()
                
                #return self.text
            except Exception as e:
                raise ValueError(f"Error extracting text content: {e}") from None
    
    def fetch_url(self, timeout=None):
        self.get_response(timeout)
        self.update_url()
        self.get_response_code()
        
        if self.url.endswith(".pdf"): # check if pdf
            self.get_pdf_content()
            self.get_pdf_text()

        else:
            self.get_html()
            self.get_text()
        
        #return (self.url, self.html_content, self.text)




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


