import requests
from bs4 import BeautifulSoup
import io
import PyPDF2

def get_pages(number_pages):
    """
    Input: Number of pages to be scraped
    Output: URLs of pages
    """
    pages_l = []
    for page in range(1, number_pages + 1):
        page_url = 'https://www.rijksoverheid.nl/documenten?pagina=' + str(page)
        pages_l.append(page_url)
    return pages_l


def get_document_urls(page_url):
    """
    Input: URL of page in https://www.rijksoverheid.nl/documenten
    Output: A list of the document URLs on this page of len 10
    """
    response = requests.get(page_url)
    document_urls = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.find_all("a")

        for link in links:
                href = link.get("href")
                if href.startswith('/documenten'):
                    document_urls.append('https://www.rijksoverheid.nl'+ href)
                    
    return document_urls


def get_pdf_url(url):
    """
    Input: A document URL from https://www.rijksoverheid.nl/documenten
    Output: The URLs of the PDFs referenced in the document URL
    """
    response = requests.get(url)
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.find_all("a")

        #pdf_urls = []

        for link in links:
            href = link.get("href")
            if href.endswith(".pdf"):
                pdf_url = 'https://www.rijksoverheid.nl'+ href
                
                #pdf_urls.append(pdf_url)
        return pdf_url


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


def scrape_documents(num_pages = 5):
    """
    Input: Number of pages to be scraped; default = 5
    Output: Dictionary url: pdf text
    """
    url_pdf = {}
    
    pages = get_pages(num_pages)
    
    for page in pages:
        document_urls = get_document_urls(page)
        
        for doc_url in document_urls:
            pdf_url = get_pdf_url(doc_url)
            pdf_text = get_pdf_text(pdf_url)
            
            url_pdf[doc_url] = pdf_text
    
    return url_pdf
