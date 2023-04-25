from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def get_top_k_docs(query, docs, k=5):

    """
    Input: query and a list of documents. k=2 by default.
    Output: sorted top documents according to cosine similarity score.
    """
    
    vectorizer = TfidfVectorizer() # initialize vectorizer

    query_and_docs = [query] + docs # corpus of query and documents
    
    query_and_docs = [par.lower() for par in query_and_docs] # lower characters
    
    matrix = vectorizer.fit_transform(query_and_docs)

    scores = [] # cosine similarity scores

    for i in range(1, len(query_and_docs)):
        scores.append(cosine_similarity(matrix[0], matrix[i])[0][0]) 

    
    sorted_list = sorted(enumerate(scores), key=lambda x: x[1], reverse=True) # sort
    top_doc_indices = [x[0] for x in sorted_list[:k]]
    top_docs = [docs[x] for x in top_doc_indices] # return top k 

    return top_docs