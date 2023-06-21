import pandas as pd
import nltk 
nltk.download('punkt')
def create_passages_dataframe_1(collection):
    all_passages_df = pd.DataFrame(columns=['URL', 'Textual_Content'])

    for index, row in collection.iterrows():
        url = row['URL']
        content = str(row['Textual_Content'])

        sentences = nltk.sent_tokenize(content, language='dutch')  # tokenize to sentences

        passages = []
        passage_words = []
        word_count = 0
        for sentence in sentences:
            sentence_words = nltk.word_tokenize(sentence, language='dutch')
            if word_count + len(sentence_words) <= 100:
                passage_words.extend(sentence_words)
                word_count += len(sentence_words)
            else:
                passages.append(' '.join(passage_words))
                passage_words = sentence_words
                word_count = len(sentence_words)

        if passage_words:
            passages.append(' '.join(passage_words))

        passage_df = pd.DataFrame({'URL': url, 'Textual_Content': passages})  # store passages

        all_passages_df = pd.concat([all_passages_df, passage_df], ignore_index=True)  # combine all

    return all_passages_df


def create_passages_dataframe_2(collection):
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
