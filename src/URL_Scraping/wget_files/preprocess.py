import os
from bs4 import BeautifulSoup

def read_folders(root_path):
    """
    Reads HTML files from nested folders.
    Returns a list of type(list) of HTML files.
    """
    html_contents = []

    for dirpath, dirnames, filenames in os.walk(root_path):
        for filename in filenames:
            if filename.endswith('.html'):
                file_path = os.path.join(dirpath, filename)
                with open(file_path, 'r',  encoding='ISO-8859-1') as file:
                    html_contents.append(file.read())
    return html_contents


def split_paragraphs(html_content):
    """
    Input: HTML content 
    Output: A List of type(list) of HTML textual content splitted in paragraphs
    """
    soup = BeautifulSoup(html_content, 'html.parser')

    # find all <p> tags and extract their text contents
    paragraphs = [p.get_text() for p in soup.find_all('p')]

    return paragraphs