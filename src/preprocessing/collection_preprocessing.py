
import pandas as pd
import ast

def get_passages(df):
    df_filtered = df[df['Exception'].isnull()].copy()
    df_filtered['Passages'] = df_filtered['Textual_Content'].apply(lambda x: [passage for passage in x.split('\n') if passage.strip()])
    return df_filtered


def id_passages(df):
    passages = []

    for idx, passage in df['Passages'].iteritems():
        url = df.loc[idx, 'URL']
        for p in passage:
            passages.append({'id': url, 'content': p})
    
    return passages





def remove_null_questions(df1, df2):
    to_append = []
    for i in range(len(df1)):
        urls = list(ast.literal_eval(df1['URLs'][i]))
        cleaned_urls = []
        for url in urls:
            row = df2.loc[df2['URL'] == url]
            #print(row)
            if row['Exception'].isnull().any():
                cleaned_urls.append(url)

        to_append.append(cleaned_urls)

    df1['Cleaned_URLs'] = to_append
    # Remove rows with empty URLs list
    df1 = df1[df1['Cleaned_URLs'].map(len) > 0]
    df1.reset_index(drop=True, inplace=True)
    
    return df1


