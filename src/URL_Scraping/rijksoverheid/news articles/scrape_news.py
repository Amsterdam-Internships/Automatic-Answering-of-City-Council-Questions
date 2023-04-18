import requests
from bs4 import BeautifulSoup

def get_pages(number_pages):
    """
    Input: Number of pages to be scraped
    Output: URLs of pages
    """
    pages_l = []
    for page in range(1, number_pages + 1):
        page_url = 'https://www.rijksoverheid.nl/actueel/nieuws?pagina=' + str(page)
        pages_l.append(page_url)
    return pages_l

def get_document_urls(page_url):
    """
    Input: URL of page in https://www.rijksoverheid.nl/actueel/nieuws
    Output: A list of the news document URLs on this page of len 10
    """
    response = requests.get(page_url)
    document_urls = []
    if response.status_code == 200:
        soup = BeautifulSoup(response.content, "html.parser")
        links = soup.find_all("a")

        for link in links:
                href = link.get("href")
                if href.startswith('/actueel/nieuws'):
                    document_urls.append('https://www.rijksoverheid.nl'+ href)
                    
    return document_urls

# Example 
# get_document_urls('https://www.rijksoverheid.nl/actueel/nieuws?pagina=5')

def get_html_content(url):
    """
    Input: URL 
    Output: HTML content of URL
    """
    response = requests.get(url)

    if response.status_code == 200:
        html_content = response.content.decode('utf-8')
        return html_content
    else:
        return (f'Request failed with status code {response.status_code}')
    

def get_article_html(html_content):
    """
    Selects only the HTML content from 'class': 'article content'
    """
    soup = BeautifulSoup(test, 'html.parser')
    div_element = soup.find('div', {'class': 'article content'})

    html_content = div_element.decode_contents()

    return html_content


def remove_documenten(article_html):
    """
    Removes everything after '<div class="block docs-pubs results">'
    """
    substring = '<div class="block docs-pubs results">'
    new_content = article_html.split(substring, 1)[0]
    
    return new_content


def split_paragraphs(html_content):
    """
    Input: HTML content 
    Output: A List of type(list) of HTML textual content splitted in paragraphs
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # find all <p> tags and extract their text contents
    paragraphs = [p.get_text() for p in soup.find_all('p')]

    return paragraphs


# Example
# example = remove_documenten(get_article_html(test))
# example
# split_paragraphs(example)


def collect_news_content(num_pages=5, clean_documenten = True, split_par = True):
    """
    Input: num_pages = 5 (by default): set the num. of pages to scrape
           clean_documenten = True (by default): set if <div class="block docs-pubs results"> should be removed
           split_par = True (by default): set if HTML content should be cleaned and slip into paragraphs
           
    Return: Dictionary type(dict) where key is article URL and value is its content 
    """
    url_content = {}
    
    pages = get_pages(num_pages)
    
    for page in pages: # iterate over pages
        document_urls = get_document_urls(page)
        
        for doc_url in document_urls: # iterate over docs
            content = get_html_content(doc_url) # collect HTML content
            if clean_documenten:
                content = remove_documenten(content)
            if split_par:
                content = split_paragraphs(content)
            url_content[doc_url] = content
    return url_content
            

# Test
# collect_news_content(2)