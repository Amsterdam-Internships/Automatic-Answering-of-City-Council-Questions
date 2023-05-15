import pandas as pd

def filter_by_domains(df, domains):
    # remove empty
    df = df[df['URLs'].notnull()]

    # create a boolean mask for the rows that have URLs in the domain list
    mask = df['URLs'].apply(lambda x: any(domain in x for domain in domains))

    # apply the boolean mask to the dataframe
    filtered_df = df.loc[mask].copy()

    # filter the URLs column based on the domain list
    filtered_df.loc[:, 'URLs'] = filtered_df['URLs'].apply(lambda x: '\n'.join([url for url in x.split('\n') if any(domain in url for domain in domains)]))

    return filtered_df


def filter_factual(df):
    pass




def clean_wrong_url_ending(url):
     if url.endswith(")."):
         return url[:-2]
     elif url.endswith("."):
         return url[:-1]
     else:
         return url

def clean_urls(urls):
    clean_urls = []
    for url in urls:
        clean_urls.append(clean_wrong_url_ending(url))   
    return clean_urls
    