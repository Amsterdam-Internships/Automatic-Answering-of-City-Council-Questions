
import PyPDF2
import requests
import io

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