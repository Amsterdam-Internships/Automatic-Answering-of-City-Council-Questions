import nltk
import pandas as pd
nltk.download('punkt')
import ast

def create_passages_dataframe(collection):
    all_passages_df = pd.DataFrame(columns=['URL', 'Textual_Content'])

    for index, row in collection.iterrows():
        url = row['URL']
        content = str(row['Textual_Content'])

        sentences = nltk.sent_tokenize(content, language='dutch')

        passages = []
        passage_words = []
        word_count = 0

        for sentence in sentences:
            sentence_words = nltk.word_tokenize(sentence, language='dutch')

            while len(sentence_words) > 0:
                if word_count + len(sentence_words) <= 100:
                    passage_words.extend(sentence_words)
                    word_count += len(sentence_words)
                    sentence_words = []
                else:
                    remaining_words = 100 - word_count
                    passage_words.extend(sentence_words[:remaining_words])
                    passages.append(' '.join(passage_words))
                    passage_words = []
                    word_count = 0
                    sentence_words = sentence_words[remaining_words:]

        if passage_words:
            passages.append(' '.join(passage_words))

        passage_df = pd.DataFrame({'URL': url, 'Textual_Content': passages})
        all_passages_df = pd.concat([all_passages_df, passage_df], ignore_index=True)

    return all_passages_df


def add_passages_ids(questions_for_ranking, passages_df):
    matching_ids_column = []
    for index, row in questions_for_ranking.iterrows():
        matching_ids = []
        for url in ast.literal_eval(row['URLs']):
            for index2, row2 in passages_df.iterrows():
                if url == row2['URL']:
                    matching_ids.append(row2['id'])
        if matching_ids:
            matching_ids_column.append(matching_ids)
        else:
            matching_ids_column.append(None)
    questions_for_ranking['passages_ids'] = matching_ids_column
    return questions_for_ranking
