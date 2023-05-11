import requests
from bs4 import BeautifulSoup
import time 
import random
import PyPDF2
import io




########### Class ###############???

def collect_document(url):
    """
    Collects the content of a document. 
    Input: url 
    Output: (updated_url, page_html, page_text)
    """
    updated_urls = []
    page_text = []
    page_html = []
    try:
        response = requests.get(url, allow_redirects=True)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')   ##### check if it could be PDF ######
            text = soup.get_text()
            updated_url = response.url
            
            page_text.append(text)
            page_html.append(soup)
            updated_urls.append(updated_url)
        else:
            # Handle any errors
            page_text.append(f"Error fetching {url}: {response.status_code}")
            page_html.append(f"Error fetching {url}: {response.status_code}")
            updated_urls.append(f"Error fetching {url}: {response.status_code}")
    except:
        page_text.append(f"Error fetching {url}")
        page_html.append(f"Error fetching {url}")
        updated_urls.append(f"Error fetching {url}")
        
    return (updated_urls, page_html, page_text)


def collect_html_document(url_response):
    soup = BeautifulSoup(url_response.content, 'html.parser')   ##### check if it could be PDF ######
    text = soup.get_text()
    updated_url = url_response.url

    return (soup, text, updated_url)


def get_pdf_text(pdf_url):
    """
    Input: PDF URL
    Output: PDF textual content
    """
    pdf = requests.get(pdf_url)
    pdf_content = pdf.content 
    pdf_text = io.BytesIO(pdf_content)
    pdf_reader = PyPDF2.PdfReader(pdf_text)
    text = ""
    for page_num in range(len(pdf_reader.pages)):
        page = pdf_reader.pages[page_num]
        text += page.extract_text()
    
    return text



def collect_all_documents(url_list):
    """
    Input: List of urls
    Output: (updated_url, page_html, page_text) per each url in the given list in a list.
    """

    all_documents = []
    for url in url_list:
        all_documents.append(collect_document(url))
        time.sleep(random.uniform(2, 4)) # time out 2-4 seconds
    
    return all_documents
    


def clean_ending(wrong_url):
    pass


def check_nonsense(url_collection):
    pass

#def preprocess_content()


###### Check the Error Fetching if ). and . are removed if they are still Errors #######


