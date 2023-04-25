from bs4 import BeautifulSoup


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
    

def split_paragraphs(html_content):
    """
    Input: HTML content 
    Output: A List of type(list) of HTML textual content splitted in paragraphs
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # find all <p> tags and extract their text contents
    paragraphs = [p.get_text() for p in soup.find_all('p')]

    return paragraphs


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