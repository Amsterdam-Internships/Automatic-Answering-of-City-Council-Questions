import pandas as pd
import pickle
import pyarrow as pa
from datasets import Dataset

def load_tfidf_results(file_path):
    with open(file_path, 'rb') as f:
        tfidf_results = pickle.load(f)
    return tfidf_results

def get_top_results(tfidf_results):
    top_1 = []
    top_5 = []
    top_10 = []
    for k in tfidf_results.keys():
        counter = 0
        to_append_5 = []
        to_append_10 = []
        for value in tfidf_results[k]:
            if counter == 0:
                top_1.append(value[0])
            elif counter <= 4:
                to_append_5.append(value[0])
            elif counter <= 9:
                to_append_10.append(value[0])
            else:
                break
            counter += 1
        top_5.append(to_append_5)
        top_10.append(to_append_10)
    return top_1, top_5, top_10

def load_reference_urls(file_path):
    urls = pd.read_csv(file_path)
    return urls

def get_content_list(top_1, urls):
    content_list = []
    for url in top_1:
        matching_row = urls[urls['URL'] == url]
        if not matching_row.empty:
            textual_content = matching_row['Text'].values[0]
            content_list.append((url, textual_content))
        else:
            content_list.append((url, 'Empty'))
    return content_list

def load_questions(file_path):
    questions = pd.read_csv(file_path)
    return questions

def get_answer_list(tfidf_results, questions):
    answer_list = []
    for question in tfidf_results.keys():
        matching_row = questions[questions['Question'] == question]
        if not matching_row.empty:
            answer = matching_row['Answer'].values[0]
            answer_list.append((question, answer))
    return answer_list

def create_text_summary_df(content_list, answer_list):
    textual_content_list = [textual_content for url, textual_content in content_list]
    answer_list = [answer for question, answer in answer_list]
    text_summary_df = pd.DataFrame({'summary': answer_list, 'text': textual_content_list})
    return text_summary_df

def convert_to_dataset(text_summary_df):
    arrow_table = pa.Table.from_pandas(text_summary_df)
    arrow_dict = arrow_table.to_pydict()
    text_summary = Dataset.from_dict(arrow_dict)
    return text_summary

