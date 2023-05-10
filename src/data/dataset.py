

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


