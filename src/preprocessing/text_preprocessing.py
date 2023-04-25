import string 
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import *

stop = stopwords.words('dutch')

def tokenize(text):
    """
        Tokenizes the input text.
        Input: text - type(str)
        Output: a list of tokens - type(list)
    """
    tokens = word_tokenize(text, language='dutch')
    return tokens

def stem_token(token): # Doesn't work rn, should check how to do for Dutch
    """
        Stems the given token using the PorterStemmer from the nltk library
        Input: a single token
        Output: the stem of the token
    """
    stemmer = PorterStemmer()
    return stemmer.stem(token)


def process_text(text, stop_words, stem=False, remove_stopwords=False, lowercase_text=False, remove_punct=False):
    """
    Given a string, the function tokenizes
    it and processes it according to the set requirements.
    """
    tokens = []
    for token in tokenize(text):
        if remove_stopwords and token.lower() in stop_words:
            continue
        if remove_punct and token.isdigit():
            continue
        if token in string.punctuation:
            continue
        if len(token) < 2:
            continue
        if stem:
            token = stem_token(token)
        if lowercase_text:
            token = token.lower()
        tokens.append(token)

    return tokens