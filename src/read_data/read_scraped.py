import os
from bs4 import BeautifulSoup


def read_html(root_dir):
    """
    Reads all HTML documents from all nested folders.
    Returns a list of tuples (URL, HTML_content)
    """

    html_contents = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.html'):
                file_path = os.path.join(dirpath, filename)
                relative_path = file_path.replace(root_dir, '') # Remove root_dir substring
                with open(file_path, 'r', encoding='ISO-8859-1') as file:
                    file_contents = file.read()
                    html_contents.append((relative_path, file_contents))
    
    return html_contents


def read_pdf(root_dir):
    """
    Reads all PDF documents from all nested folders.
    Returns a list of tuples (URL, PDF_content)
    """

    pdf_contents = []

    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.endswith('.pdf'):
                file_path = os.path.join(dirpath, filename)
                relative_path = file_path.replace(root_dir, '') # Remove root_dir substring
                with open(file_path, 'r', encoding='ISO-8859-1') as file:
                    file_contents = file.read()
                    pdf_contents.append((relative_path, file_contents))
    
    return pdf_contents