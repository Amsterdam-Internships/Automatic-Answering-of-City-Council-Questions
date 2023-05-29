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

from sklearn.feature_extraction.text import TfidfVectorizer


def tfidf_search(query, collection):
    """
    Perform a search over all documents with the given query using tf-idf.
    Input:
        query - a (unprocessed) query
        collection: a list of tuples (document_id, document_content)
    Output: a list of (document_id, score), sorted in descending relevance to the given query
    """
    # Convert the collection into a dictionary to remove duplicate tuples
    unique_collection = {doc[0]: doc[1].lower().replace('\n', '') for doc in collection}

    # Preprocess the query
    preprocessed_query = query.lower().replace('\n', '')

    # Extract document contents from the unique_collection
    document_contents = list(unique_collection.values())

    # Initialize and fit the TfidfVectorizer
    vectorizer = TfidfVectorizer()
    matrix = vectorizer.fit_transform(document_contents)

    # Transform the query using the fitted vectorizer
    query_vector = vectorizer.transform([preprocessed_query])

    # Calculate the cosine similarity between the query and document vectors
    cosine_similarities = matrix.dot(query_vector.T).toarray().flatten()

    # Create a list of (document_id, score) tuples
    results = [(doc_id, cosine_similarities[i]) for i, doc_id in enumerate(unique_collection.keys())]

    # Sort the results in descending order of relevance (score)
    results.sort(key=lambda x: x[1], reverse=True)

    return results


def perform_tfidf_search(queries, collection):
    """
    Perform TF-IDF search for each query in a list of queries.
    Input:
        queries - a list of queries
        collection: a list of tuples (document_id, document_content)
    Output: a dictionary where the key is the query and the value is a list of (document_id, score) tuples
    """
    search_results = {}

    for query in queries:
        results = tfidf_search(query, collection)
        search_results[query] = results

    return search_results