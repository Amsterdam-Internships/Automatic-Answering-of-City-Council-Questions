import sys
import os

# absolute path of the current directory
current_dir = os.path.dirname(os.path.abspath(__file__))

# add the relative path to the source directory
src_dir = os.path.join(current_dir, 'src')
sys.path.append(src_dir)

import pandas as pd
from preprocessing import collection_preprocessing

def read_urls_questions(collected_urls_path, questions_path, clean_url_nan=False):
    """
    Input: paths to the .csv files of the collected pages and the collected questions
    Output: two daframes with the data
    """
    collected = pd.read_csv(collected_urls_path)
    questions = pd.read_csv(questions_path)

    if clean_url_nan:
        collected = collected[collected['Exception'].isnull()]
        questions = collection_preprocessing.remove_null_questions(questions, collected)

    return collected, questions


def get_questions(questions_dataframe):
    """
    Returns a list of questions from the read question data which is stored into a dataframe
    """
    return list(questions_dataframe['Question'])

def get_url_content_tuples(collection_dataframe):
    """
    Input: dataframe with columns URL, Content, Textual_Content, Exception
    Returns: a list of tuples (url, textual_content)
    """
    document_list = []

    for index, row in collection_dataframe.iterrows():
        document_id = row['URL']
        document_content = row['Textual_Content']
        document_tuple = (document_id, document_content)
        document_list.append(document_tuple)
    
    return document_list



import ast

def get_relevant_docs(df):
    """
    Convert a DataFrame with questions and URLs into a dictionary.
    Input:
        df: a pandas DataFrame with columns 'question' and 'urls'
    Output: a dictionary where the key is the question and the value is a list of URLs
    """
    question_urls_dict = {}

    for _, row in df.iterrows():
        question = row['Question']
        urls = row['Cleaned_URLs']

        if isinstance(urls, str):
            # Convert the string to a list
            urls = ast.literal_eval(urls)

        question_urls_dict[question] = urls

    return question_urls_dict


